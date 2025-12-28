import uuid 
import streamlit as st 
from graph import graph
import os
import json
import time
from dotenv import load_dotenv
import asyncio

# Load Environment Variables
load_dotenv()

# Define the data directory and chat store file path
DATA_DIR = "app_data"
CHAT_STORE = os.path.join(DATA_DIR, "chat_store.json")
os.makedirs(DATA_DIR, exist_ok=True)

def run_graph_async(messages, thread_id):
    """
    Run the LangGraph graph asynchronously and return the result.
    
    """
    return asyncio.run(
        graph.ainvoke(
            {"messages": messages},
            config={"configurable": {"thread_id": thread_id}},
        )
    )

# Load chat history from JSON file
def load_chat_store():
    if os.path.exists(CHAT_STORE):
        with open(CHAT_STORE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Save chat history to JSON file
def save_chat_store(chats):
    with open(CHAT_STORE, "w", encoding="utf-8") as f:
        json.dump(chats, f, indent=2)
        



# Streamlit App Configuration
st.set_page_config(
    page_title="Agentic RAG Chatbot",
    page_icon="🤖",
    layout="centered",
)
# Streamlit App Title
st.title("🤖 Agentic RAG Assistant")
st.caption("Planner → Executor → Synthesizer | Local PDFs + Web Search")


# Initialize Session State
if "chats" not in st.session_state:
    st.session_state.chats = load_chat_store()

# Initialize a unique thread ID for the session
if "active_thread" not in st.session_state:
    thread_id = str(uuid.uuid4())
    st.session_state.active_thread = thread_id
    st.session_state.chats[thread_id] = {
        "title": "New Chat",
        "ui_messages": []
    }
    save_chat_store(st.session_state.chats)

with st.sidebar:
    st.header("💬 Conversations")

    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = {
            "title": "New Chat",
            "ui_messages": []
        }
        st.session_state.active_thread = new_id
        save_chat_store(st.session_state.chats)

    st.divider()

    for tid, chat in st.session_state.chats.items():
        if st.button(chat["title"], key=tid):
            st.session_state.active_thread = tid

    st.divider()
    st.caption("Chats persist locally")



thread_id = st.session_state.active_thread
chat = st.session_state.chats[thread_id]

# Render Chat History
for msg in chat["ui_messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# User Input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Set title from first message
    if chat["title"] == "New Chat":
        chat["title"] = user_input[:40]

    chat["ui_messages"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    
    # Assistant Response (Streaming)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed_text = ""

        
        
        result = run_graph_async(
            [{"role": "user", "content": user_input}],
            thread_id,
        )

        final_answer = result["messages"][-1].content

        # token streaming
        for token in final_answer.split():
            streamed_text += token + " "
            placeholder.markdown(streamed_text)
            time.sleep(0.02)

    chat["ui_messages"].append(
        {"role": "assistant", "content": final_answer}
    )

    save_chat_store(st.session_state.chats)
