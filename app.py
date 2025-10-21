import streamlit as st
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("☕ Brew & Bean AI Assistant")
st.caption("Chat with Bailey, our friendly AI barista!")

# System prompt
SYSTEM_PROMPT = """
You are Bailey, a friendly AI customer service assistant for "Brew & Bean Cafe."

MENU:
Drinks: Drip Coffee ($3), Espresso ($3.50), Latte ($4.50), Cold Brew ($4.50)
Food: Avocado Toast ($8.50), Breakfast Burrito ($9), Croissant ($3.50)

HOURS: Mon-Fri 6:30am-7pm, Sat-Sun 7am-6pm
LOCATION: 742 Maple Street
PHONE: (555) 234-5678

Answer questions warmly about menu, hours, location. Help customers decide what to order.
Be friendly and conversational.
"""

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.model = genai.GenerativeModel('gemini-1.5-flash')
    st.session_state.chat = st.session_state.model.start_chat(history=[])
    # Send system prompt
    st.session_state.chat.send_message(SYSTEM_PROMPT)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about Brew & Bean!"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    response = st.session_state.chat.send_message(prompt)
    assistant_message = response.text
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
