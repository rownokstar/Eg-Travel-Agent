# আগের উত্তরের সম্পূর্ণ app.py কোডটি এখানে পেস্ট করুন
# আমি আপনার সুবিধার জন্য কোডটি নিচে আবার দিয়ে দিচ্ছি

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

# UI Styling
custom_css = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: linear-gradient(180deg, #e6f0ff, #ffffff);
}
[data-testid="stChatMessage"] {
    border-radius: 10px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.stButton>button {
    background-color: #ff4500; color: white; border-radius: 20px;
    border: none; padding: 8px 16px; transition: background-color 0.3s;
}
.stButton>button:hover { background-color: #e03e00; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("### 🌐 TravelBot")
with col2:
    st.markdown("#### Plan Your Perfect Trip with Confidence.")
st.markdown("---")
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1527631746610-b2225a206281?q=80&w=1887&auto=format&fit=crop", caption="Discover Your Next Adventure")

# API Keys & Tools
try:
    os.environ["GROQ_API_KEY"] = st.secrets["api_keys"]["GROQ_API_KEY"]
    os.environ["TAVILY_API_KEY"] = st.secrets["api_keys"]["TAVILY_API_KEY"]
except KeyError:
    st.error("API Keys পাওয়া যায়নি! অনুগ্রহ করে Streamlit Cloud-এর 'Secrets' অংশে সঠিকভাবে কী সেট করুন।")
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

web_search_tool = TavilySearchResults(max_results=3, description="A search engine for travel info.")
tools = [web_search_tool, get_weather_forecast, calculator]

# Agent Graph
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

# Chat UI
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

        final_prompt_instruction = SystemMessage(content="Now, synthesize all information into a final, comprehensive answer.")
        message_history.append(final_prompt_instruction)
        response_container = st.empty()
        full_response = response_container.write_stream(llm.stream(message_history))
        
        if full_response:
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.error("দুঃখিত, কোনো একটি সমস্যার কারণে আমি উত্তর তৈরি করতে পারিনি।")
    st.rerun()


st.markdown("<div style='text-align: center; color: grey;'>Helped 1,000+ travelers! | <a href='#'>Support</a> | <a href='#'>Terms of Service</a></div>", unsafe_allow_html=True)

