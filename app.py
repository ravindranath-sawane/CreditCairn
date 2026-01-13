"""
Streamlit chat interface for CreditCairn.
An AI-powered Canadian credit card rewards assistant.
"""

import streamlit as st
import os
from typing import List, Dict, Any
from agent_engine import CreditCairnAgent
from data_ingestion import DataIngestion


# Page configuration
st.set_page_config(
    page_title="CreditCairn - Credit Card Rewards Assistant",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        st.session_state.agent = None
    
    if "agent_initialized" not in st.session_state:
        st.session_state.agent_initialized = False


def initialize_agent(api_key: str) -> bool:
    """
    Initialize the CreditCairn agent.
    
    Args:
        api_key: Google API key
        
    Returns:
        True if successful, False otherwise
    """
    try:
        st.session_state.agent = CreditCairnAgent(api_key=api_key)
        st.session_state.agent_initialized = True
        return True
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return False


def display_welcome_message() -> None:
    """Display welcome message in the chat."""
    welcome_msg = """👋 Welcome to **CreditCairn**!

I'm your AI-powered Canadian credit card rewards assistant. I can help you:

- 🎯 Find the best credit cards for your spending patterns
- 💰 Maximize your rewards and points
- 📊 Compare different credit cards
- 🎁 Learn about welcome bonuses and perks
- 💡 Optimize your credit card strategy

**How can I help you today?**

Try asking questions like:
- "What's the best no-fee card for groceries?"
- "Which card has the best travel rewards?"
- "Compare cash back cards for dining"
- "Show me cards with good welcome bonuses"
"""
    
    with st.chat_message("assistant"):
        st.markdown(welcome_msg)


def display_chat_history() -> None:
    """Display chat message history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_agent_response(user_input: str) -> str:
    """
    Get response from the agent.
    
    Args:
        user_input: User's message
        
    Returns:
        Agent's response
    """
    try:
        response = st.session_state.agent.chat_completion(user_input)
        return response
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}\n\nPlease make sure your API key is valid and try again."


def display_sidebar() -> None:
    """Display sidebar with information and controls."""
    with st.sidebar:
        st.title("💳 CreditCairn")
        st.markdown("---")
        
        # About section
        st.subheader("📖 About")
        st.markdown("""
**CreditCairn** is an AI-powered assistant that helps you optimize your credit card rewards strategy for Canadian credit cards.

Built with:
- 🧠 Google Gemini 1.5 Flash
- 📚 ChromaDB for RAG
- 🎨 Streamlit interface
        """)
        
        st.markdown("---")
        
        # API Key section
        st.subheader("🔑 API Configuration")
        
        # Check for API key in environment
        env_api_key = os.getenv("GOOGLE_API_KEY", "")
        
        if env_api_key:
            st.success("✅ API key found in environment")
            api_key = env_api_key
            
            if not st.session_state.agent_initialized:
                with st.spinner("Initializing agent..."):
                    if initialize_agent(api_key):
                        st.success("Agent initialized!")
                        st.rerun()
        else:
            st.warning("⚠️ No API key in environment")
            api_key = st.text_input(
                "Enter your Google API Key:",
                type="password",
                help="Get your API key from https://makersuite.google.com/app/apikey"
            )
            
            if api_key:
                if st.button("Initialize Agent"):
                    with st.spinner("Initializing agent..."):
                        if initialize_agent(api_key):
                            st.success("Agent initialized!")
                            st.rerun()
        
        st.markdown("---")
        
        # Statistics
        if st.session_state.agent_initialized:
            st.subheader("📊 Statistics")
            card_count = st.session_state.agent.retriever.collection.count()
            st.metric("Credit Cards in Database", card_count)
            st.metric("Chat Messages", len(st.session_state.messages))
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            if st.session_state.agent:
                st.session_state.agent.start_chat()
            st.rerun()
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
<p>Made with ❤️ using Streamlit</p>
<p>Data is for informational purposes only</p>
</div>
        """, unsafe_allow_html=True)


def main() -> None:
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Display sidebar
    display_sidebar()
    
    # Main content area
    st.title("💳 CreditCairn - Credit Card Rewards Assistant")
    st.markdown("Optimize your spending and maximize your rewards with AI-powered recommendations!")
    
    # Check if agent is initialized
    if not st.session_state.agent_initialized:
        st.info("👈 Please configure your Google API Key in the sidebar to get started.")
        
        # Show example without requiring API key
        with st.expander("ℹ️ About CreditCairn"):
            st.markdown("""
**CreditCairn** helps you navigate the world of Canadian credit cards using advanced AI technology.

### Features:
- **Smart Recommendations**: Get personalized card suggestions based on your spending habits
- **Rewards Optimization**: Learn how to maximize points, cash back, and benefits
- **Easy Comparison**: Compare cards side-by-side to make informed decisions
- **Welcome Bonuses**: Discover the best sign-up offers available
- **No-fee Options**: Find great cards without annual fees

### How it works:
1. Configure your Google API key in the sidebar
2. Ask questions about credit cards in natural language
3. Get AI-powered recommendations based on your needs
4. Make smarter decisions about your credit card portfolio

### Example Questions:
- "What's the best card for someone who spends a lot on groceries?"
- "Show me no-fee cards with good rewards"
- "Which card has the best travel benefits?"
- "Compare the Tangerine and Simplii cash back cards"
            """)
        
        return
    
    # Display welcome message if no messages yet
    if not st.session_state.messages:
        display_welcome_message()
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about Canadian credit cards..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_agent_response(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
