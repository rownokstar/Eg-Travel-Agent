
import streamlit as st
import os
import requests
import json
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated, List
import operator

# ------------------------------------------------------------------
# 1. কাস্টম CSS (ব্লু থিম)
# ------------------------------------------------------------------
custom_css = """
<style>
/* ব্লু গ্রেডিয়েন্ট ব্যাকগ্রাউন্ড */
[data-testid="stAppViewContainer"] > .main {
    background-image: linear-gradient(180deg, #d4e4ff, #ffffff);
}
/* চ্যাট উইন্ডোকে সুন্দর করা */
[data-testid="stChatMessage"] {
    border-radius: 10px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
/* ব্লু রঙের বাটন */
.stButton>button {
    background-color: #0068c9;
    color: white;
    border-radius: 20px;
    border: none;
    padding: 8px 16px;
    transition: background-color 0.3s;
}
.stButton>button:hover {
    background-color: #00509e;
    border: 1px solid #00509e;
}
/* সাইডবারের বাটন স্টাইল */
[data-testid="stSidebar"] .stButton>button {
    background-color: transparent;
    color: #0068c9;
    border: 1px solid #0068c9;
    width: 100%;
}
[data-testid="stSidebar"] .stButton>button:hover {
    background-color: #d4e4ff;
    color: #00509e;
    border: 1px solid #00509e;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ------------------------------------------------------------------
# 2. অ্যাপের লেআউট: হেডার, সাইডবার এবং ফুটার
# ------------------------------------------------------------------
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("### 🌐 TravelBot")
with col2:
    st.markdown("#### Plan Your Perfect Trip with Confidence.")
st.markdown("---")

# সাইডবার (New Chat এবং History সহ)
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1527631746610-b2225a206281?q=80&w=1887&auto-format&fit=crop", caption="Discover Your Next Adventure")
    
    if st.button("➕ New Chat"):
        # পুরোনো চ্যাটের প্রথম প্রশ্নটি হিস্টোরিতে সেভ করা
        if "messages" in st.session_state and len(st.session_state.messages) > 1:
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            first_user_prompt = next((msg["content"] for msg in st.session_state.messages if msg["role"] == "user"), None)
            if first_user_prompt and first_user_prompt not in st.session_state.chat_history:
                st.session_state.chat_history.insert(0, first_user_prompt[:70] + "...") # Snippet

        # বর্তমান চ্যাট রিসেট করা
        st.session_state.messages = [{"role": "assistant", "content": "Hi! I’m TravelBot. Where are you headed?"}]
        st.rerun()

    if "chat_history" in st.session_state and st.session_state.chat_history:
        st.markdown("---")
        st.subheader("Recent Chats")
        for i, chat_prompt in enumerate(st.session_state.chat_history[:5]): # শেষ ৫টি চ্যাট
            if st.button(chat_prompt, key=f"history_{i}"):
                st.session_state.messages = [{"role": "user", "content": chat_prompt}]
                st.rerun()

# ------------------------------------------------------------------
# 3. API Key লোড এবং টুল ডিফাইন করা (অপরিবর্তিত)
# ------------------------------------------------------------------
try:
    os.environ["GROQ_API_KEY"] = st.secrets["api_keys"]["GROQ_API_KEY"]
    os.environ["TAVILY_API_KEY"] = st.secrets["api_keys"]["TAVILY_API_KEY"]
except KeyError:
    st.error("API Keys পাওয়া যায়নি!")
    st.stop()
@tool
def get_weather_forecast(latitude: float, longitude: float, start_date: str, end_date: str) -> str:
    """Fetches weather forecast."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto"
    try:
        r = requests.get(url); r.raise_for_status(); return json.dumps(r.json()['daily'])
    except Exception as e: return f"Error: {e}"
@tool
def calculator(expression: str) -> str:
    """Calculator for math expressions related to travel costs."""
    try:
        return f"{eval(expression)}"
    except Exception as e: return f"Error: {e}"
web_search_tool = TavilySearchResults(max_results=3)
tools = [web_search_tool, get_weather_forecast, calculator]

# ------------------------------------------------------------------
# 4. এজেন্ট গ্রাফ তৈরি এবং ক্যাশ করা (অপরিবর্তিত)
# ------------------------------------------------------------------
@st.cache_resource
def create_agent_graph():
    llm = ChatGroq(model="llama3-70b-8192", temperature=0)
    llm_with_tools = llm.bind_tools(tools)
    class TravelAgentState(TypedDict): messages: Annotated[List, operator.add]
    def agent_node(state): return {"messages": [llm_with_tools.invoke(state["messages"])]}
    tool_node = ToolNode(tools)
    def should_continue(state): return "end" if not isinstance(state["messages"][-1], AIMessage) or not state["messages"][-1].tool_calls else "continue"
    workflow = StateGraph(TravelAgentState)
    workflow.add_node("agent", agent_node); workflow.add_node("action", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"continue": "action", "end": END})
    workflow.add_edge("action", "agent")
    return workflow.compile(), llm
app, llm = create_agent_graph()

# ------------------------------------------------------------------
# 5. চ্যাট ইন্টারফেস
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I’m TravelBot. Where are you headed?"}]

for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🌐"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

prompt_to_process = st.chat_input("শুধুমাত্র ভ্রমণ বিষয়ে প্রশ্ন করুন...")

if prompt_to_process:
    st.session_state.messages.append({"role": "user", "content": prompt_to_process})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt_to_process)
    
    with st.chat_message("assistant", avatar="🌐"):
        with st.expander("🤔 TravelBot is thinking..."):
            thinking_container = st.container()
        
        message_history = [HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"]) for msg in st.session_state.messages]
        
        system_instruction = SystemMessage(
            content=(
                "You are a specialized AI travel agent 'TravelBot'. Your ONLY function is to assist with travel-related queries. If the user asks a question NOT related to travel, you MUST politely refuse. Your refusal message should be in the user's language. For travel questions, think step-by-step, call one tool at a time, and respond in the user's language."
            )
        )
        message_history.append(system_instruction)
        
        inputs = {"messages": message_history}
        
        for s in app.stream(inputs, stream_mode="values"):
            msg = s["messages"][-1]
            if isinstance(msg, AIMessage) and msg.tool_calls:
                thinking_container.info(f"🛠️ Using tool: {msg.tool_calls[0]['name']} with args: {msg.tool_calls[0]['args']}")
            elif isinstance(msg, ToolMessage):
                thinking_container.warning(f"⚙️ Tool Result ({msg.name}): {msg.content[:200]}...")

        final_prompt_instruction = SystemMessage(content="Now, synthesize all information into a final, comprehensive answer for the user.")
        message_history.append(final_prompt_instruction)
        
        response_container = st.empty()
        full_response = response_container.write_stream(llm.stream(message_history))
            
        if full_response:
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.error("দুঃখিত, কোনো একটি সমস্যার কারণে আমি উত্তর তৈরি করতে পারিনি।")
    st.rerun()

# ফুটার (আপনার তথ্য সহ)
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Programmed and Developed by <a href='https://www.linkedin.com/in/dmshahriarhossain/' target='_blank'>DM Shahriar Hossain</a></div>", unsafe_allow_html=True)
