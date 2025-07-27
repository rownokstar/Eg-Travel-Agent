
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
# 1. Custom CSS for UI Styling (Blue Theme)
# ------------------------------------------------------------------
custom_css = """
<style>
/* Blue gradient background */
[data-testid="stAppViewContainer"] > .main {
    background-image: linear-gradient(180deg, #d4e4ff, #ffffff);
}
/* Styling chat messages */
[data-testid="stChatMessage"] {
    border-radius: 10px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
/* Blue buttons */
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
/* Sidebar button style */
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
# 2. App Layout: Header, Sidebar, and Footer
# ------------------------------------------------------------------
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("### 🌐 TravelBot")
with col2:
    st.markdown("#### Plan Your Perfect Trip with Confidence.")
st.markdown("---")

# Sidebar with New Chat and History
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1633332755192-727a05c4013d?q=80&w=2080&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", caption="Discover Your Next Adventure")
    
    if st.button("➕ New Chat"):
        # Save the first user prompt of the old chat to history
        if "messages" in st.session_state and len(st.session_state.messages) > 1:
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            first_user_prompt = next((msg["content"] for msg in st.session_state.messages if msg["role"] == "user"), None)
            if first_user_prompt and first_user_prompt not in st.session_state.chat_history:
                st.session_state.chat_history.insert(0, first_user_prompt[:70] + "...") # Save a snippet

        # Reset the current chat
        st.session_state.messages = [{"role": "assistant", "content": "Hi! I’m TravelBot. Where are you headed?"}]
        st.rerun()

    if "chat_history" in st.session_state and st.session_state.chat_history:
        st.markdown("---")
        st.subheader("Recent Chats")
        for i, chat_prompt in enumerate(st.session_state.chat_history[:5]): # Show last 5 chats
            if st.button(chat_prompt, key=f"history_{i}"):
                st.session_state.messages = [{"role": "user", "content": chat_prompt}]
                st.rerun()

# ------------------------------------------------------------------
# 3. API Key Loading and Tool Definition (Unchanged)
# ------------------------------------------------------------------
try:
    os.environ["GROQ_API_KEY"] = st.secrets["api_keys"]["GROQ_API_KEY"]
    os.environ["TAVILY_API_KEY"] = st.secrets["api_keys"]["TAVILY_API_KEY"]
except KeyError:
    st.error("API Keys not found! Please set them correctly in the Streamlit Cloud 'Secrets' section.")
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
# 4. Agent Graph Creation (Unchanged)
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
# 5. Chat Interface (Converted to English)
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I’m TravelBot. Where are you headed?"}]

for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🌐"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

prompt_to_process = st.chat_input("Ask only about travel-related topics...")

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
                "You are a specialized AI travel agent 'TravelBot'. "
                "Your ONLY function is to assist with travel-related queries. This includes tourism, flight and hotel information, itineraries, budgets, weather for destinations, and visa information. "
                "If the user asks a question that is NOT related to travel (e.g., about politics, science, history, general trivia), you MUST politely refuse to answer. "
                "Your refusal message should be: 'I am a travel agent and can only assist with travel-related queries.' "
                "Follow these rules for travel questions: "
                "1. Think step-by-step. "
                "2. Call only one tool at a time. "
                "3. Respond in the same language as the user's last message."
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
            st.error("Sorry, I encountered an issue and couldn't generate a response. Please try rephrasing your question.")
    st.rerun()

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Programmed and Developed by <a href='https://www.linkedin.com/in/dm-shahriar-hossain/' target='_blank'>DM Shahriar Hossain</a></div>", unsafe_allow_html=True)
