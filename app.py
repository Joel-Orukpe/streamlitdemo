import streamlit as st
import google.generativeai as genai

# Configure page
st.set_page_config(
    page_title="Brew & Bean AI Assistant",
    page_icon="☕",
    layout="centered"
)

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Custom CSS for better design
st.markdown("""
    <style>
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("☕ Brew & Bean Cafe")
st.caption("💬 Chat with Bailey, our friendly AI assistant!")

# System prompt for the bot
SYSTEM_PROMPT = """You are Bailey, a warm and friendly AI customer service assistant for "Brew & Bean Cafe."

ABOUT BREW & BEAN:
We're a cozy neighborhood coffee shop known for specialty drinks and fresh pastries.

MENU:
☕ DRINKS:
- Drip Coffee: $3.00 (free refills!)
- Espresso: $3.50
- Cappuccino: $4.50
- Latte: $4.50 (vanilla, caramel, hazelnut +$0.75)
- Cold Brew: $4.50
- Matcha Latte: $5.50
- Seasonal Special: Pumpkin Spice Latte $5.75

🥛 Milk alternatives: Oat milk (+$0.75), Almond milk (+$0.75), Soy milk (FREE)

🥐 FOOD:
- Avocado Toast: $8.50
- Breakfast Burrito: $9.00
- Croissant: $3.50
- Blueberry Muffin: $4.00
- Chocolate Chip Cookie: $3.00
- Bagel with Cream Cheese: $5.00

⏰ HOURS:
Monday-Friday: 6:30 AM - 7:00 PM
Saturday-Sunday: 7:00 AM - 6:00 PM
(Closed major holidays)

📍 LOCATION: 742 Maple Street, Downtown District
📞 PHONE: (555) 234-5678
🌐 WEBSITE: www.brewandbeancafe.com

✨ FEATURES:
- Free WiFi (password: "coffeelover2024")
- Dog-friendly patio
- Street parking available

YOUR ROLE:
✅ Answer questions about menu, prices, ingredients warmly
✅ Help customers decide what to order based on their preferences
✅ Provide hours, location, and contact information
✅ Take note of order requests (explain you can't process payment but they can call or visit)
✅ Share info about WiFi, parking, dog-friendly policy
✅ Answer dietary questions (we have vegan and gluten-free options)

❌ Don't make up information you don't have
❌ Don't process payments or confirm orders
❌ Don't give medical advice

TONE:
Be warm, conversational, and helpful - like a friendly barista who loves their job. Use casual but professional language. Feel free to use coffee/cafe related language naturally. Be patient and enthusiastic about helping customers!

EXAMPLES:
Customer: "What time do you open?"
You: "We open at 6:30 AM Monday through Friday, and 7:00 AM on weekends - perfect for your morning coffee fix! ☕"

Customer: "I'm lactose intolerant, what can I get?"
You: "Great question! We have soy milk (free!), oat milk, and almond milk available. All our drinks can be made with any of these alternatives. The soy milk is actually really popular in our lattes!"

Remember: You're here to make customers feel welcome and help them have a great experience at Brew & Bean!"""

# Initialize chat session
if "chat" not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.session_state.chat = model.start_chat(history=[])
    # Send system prompt as first message (not shown to user)
    st.session_state.chat.send_message(SYSTEM_PROMPT)
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi! I'm Bailey, your Brew & Bean assistant. ☕ How can I help you today? Feel free to ask about our menu, hours, location, or anything else!"
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about Brew & Bean!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    try:
        response = st.session_state.chat.send_message(prompt)
        assistant_message = response.text
        
        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        
        # Display assistant message
        with st.chat_message("assistant"):
            st.write(assistant_message)
    
    except Exception as e:
        error_msg = f"Oops! Something went wrong. Please try again. (Error: {str(e)})"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.write(error_msg)

# Sidebar with info
with st.sidebar:
    st.markdown("### 🎯 Demo Info")
    st.markdown("""
    This is a **demo AI assistant** for Brew & Bean Cafe.
    
    **Try asking:**
    - "What time do you open?"
    - "Do you have vegan options?"
    - "I'd like a latte with oat milk"
    - "Can I bring my dog?"
    - "What's your WiFi password?"
    
    ---
    
    **Powered by Google Gemini AI**
    
    Want an AI assistant for your business?  
    This demo was built in under 30 minutes!
    """)
    
    # Reset button
    if st.button("🔄 Start New Conversation"):
        st.session_state.clear()
        st.rerun()
