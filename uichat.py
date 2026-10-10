import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# --- Core logic (unchanged) ---
llm = ChatOllama(
    model="qwen3:1.7b",
    temperature=0
)

# Mood options (original mapping, unchanged)
mood_map = {
    1: "you are an angry AI, your name is Buddy, call me sir",
    2: "you are a happy AI, your name is Buddy, call me sir",
    3: "you are a sad AI, your name is Buddy, call me sir",
    4: "you are a surprised AI, your name is Buddy, call me sir"
}

# --- Streamlit state management ---
if "messages" not in st.session_state:
    st.session_state.messages = []      # LangChain message history
if "mood_set" not in st.session_state:
    st.session_state.mood_set = False

st.title("Buddy – Mood Chat")

# Mood selection (like the original input option)
mood_choice = st.selectbox(
    "Choose an option:",
    options=[1, 2, 3, 4],
    format_func=lambda x: {1: "1. angry", 2: "2. happy", 3: "3. sad", 4: "4. surprised"}[x]
)

if st.button("Apply Mood"):
    mode = mood_map[mood_choice]                            # original mode string
    st.session_state.messages = [SystemMessage(content=mode)]  # reset conversation
    st.session_state.mood_set = True
    st.rerun()

# --- Chat interface (only after mood is set) ---
if st.session_state.mood_set:
    # Display previous messages (skip the system prompt)
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        elif isinstance(msg, AIMessage):
            st.chat_message("assistant").write(msg.content)

    # User input (like the original "prompt = input()")
    prompt = st.chat_input("You:")
    if prompt:
        # Exit condition (same as typing "0")
        if prompt.strip() == "0":
            st.chat_message("assistant").write("Goodbye!")
            st.session_state.mood_set = False
            st.stop()

        # --- Core logic: exactly the original sequence ---
        st.session_state.messages.append(HumanMessage(content=prompt))

        response = llm.invoke(st.session_state.messages)    # LangChain invoke
        bot_response = response.content

        st.session_state.messages.append(AIMessage(content=bot_response))
        # ------------------------------------------------
        st.rerun()