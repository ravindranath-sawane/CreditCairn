"""
Streamlit chat interface for CreditCairn.
An AI-powered Canadian credit card rewards assistant.
SaveSage-inspired clean, professional design.
"""

import streamlit as st
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agent_engine import CreditCairnAgent
from data_ingestion import DataIngestion


# Page configuration
st.set_page_config(
    page_title="CreditCairn - Credit Card Rewards Assistant",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/CreditCairn',
        'Report a bug': "https://github.com/yourusername/CreditCairn/issues",
        'About': "# CreditCairn\nAI-powered credit card assistant."
    }
)

# SaveSage-Inspired Clean Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary: #10B981;
        --primary-dark: #059669;
        --primary-light: #D1FAE5;
        --secondary: #6366F1;
        --bg-white: #FFFFFF;
        --bg-light: #F8FAFC;
        --bg-cream: #FFFBF5;
        --text-dark: #1E293B;
        --text-medium: #475569;
        --text-light: #94A3B8;
        --border: #E2E8F0;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
        --radius: 16px;
        --radius-sm: 8px;
        --radius-lg: 24px;
    }
    
    /* Hide Streamlit chrome */
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Base styles */
    .stApp {
        background: linear-gradient(180deg, var(--bg-cream) 0%, var(--bg-light) 50%, var(--bg-white) 100%);
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container {
        padding: 2rem 1rem;
        max-width: 1200px;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    h1, h2, h3 { color: var(--text-dark) !important; }
    p { color: var(--text-medium) !important; }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #ECFDF5 0%, #F0FDF4 50%, #FFFBEB 100%);
        border-radius: var(--radius-lg);
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(16, 185, 129, 0.1);
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--bg-white);
        border: 1px solid var(--primary);
        border-radius: 50px;
        padding: 6px 16px;
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--primary-dark);
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-sm);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: var(--text-dark) !important;
        margin-bottom: 1rem;
        line-height: 1.2;
        position: relative;
        z-index: 1;
    }
    
    .hero-title span {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        color: var(--text-medium) !important;
        max-width: 600px;
        margin: 0 auto 2rem auto;
        line-height: 1.7;
        position: relative;
        z-index: 1;
    }
    
    /* Stats Bar */
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 3rem;
        flex-wrap: wrap;
        padding: 1.5rem 0;
        position: relative;
        z-index: 1;
    }
    
    .stat-item { text-align: center; }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary-dark) !important;
        display: block;
        line-height: 1.2;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: var(--text-light) !important;
        font-weight: 500;
    }
    
    /* Feature Cards */
    .feature-card {
        background: var(--bg-white);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
    }
    
    .feature-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-icon.green { background: var(--primary-light); }
    .feature-icon.purple { background: #EDE9FE; }
    .feature-icon.orange { background: #FEF3C7; }
    .feature-icon.blue { background: #DBEAFE; }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-dark) !important;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: var(--text-medium) !important;
        line-height: 1.6;
    }
    
    /* Section Headers */
    .section-header {
        text-align: center;
        margin: 3rem 0 2rem 0;
    }
    
    .section-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-dark) !important;
        margin-bottom: 0.5rem;
    }
    
    .section-subtitle {
        font-size: 1rem;
        color: var(--text-light) !important;
    }
    
    /* Testimonial Cards */
    .testimonial-card {
        background: var(--bg-white);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    .testimonial-card:hover { box-shadow: var(--shadow-md); }
    
    .testimonial-quote {
        font-size: 0.95rem;
        color: var(--text-medium) !important;
        font-style: italic;
        line-height: 1.7;
        margin-bottom: 1rem;
    }
    
    .testimonial-author {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .author-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
        color: white;
    }
    
    .author-name {
        font-weight: 600;
        font-size: 0.9rem;
        color: var(--text-dark) !important;
    }
    
    .author-role {
        font-size: 0.8rem;
        color: var(--text-light) !important;
    }
    
    /* Trust Badges */
    .trust-bar {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        padding: 1.5rem;
        background: var(--bg-white);
        border-radius: var(--radius);
        border: 1px solid var(--border);
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .trust-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        color: var(--text-medium);
        font-weight: 500;
    }
    
    .trust-badge .icon { font-size: 1.2rem; }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        border: none;
        color: white !important;
        border-radius: var(--radius-sm);
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.75rem 1.5rem;
        height: auto;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg), 0 0 20px rgba(16, 185, 129, 0.3);
    }
    
    /* Chat Messages */
    div[data-testid="stChatMessage"] {
        background: var(--bg-white);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        box-shadow: var(--shadow-sm);
    }
    
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, #F0FDF4, #ECFDF5);
        border-color: rgba(16, 185, 129, 0.2);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: var(--bg-white);
        border-right: 1px solid var(--border);
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        background: var(--bg-white) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-dark) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
    }
    
    .stChatInputContainer textarea {
        background: var(--bg-white) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
    }
    
    /* Metrics */
    div[data-testid="metric-container"] {
        background: var(--bg-white);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 1rem;
        box-shadow: var(--shadow-sm);
    }
    
    div[data-testid="metric-container"] label { color: var(--text-light) !important; }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: var(--primary-dark) !important;
        font-weight: 700;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-light) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: var(--border);
        margin: 1.5rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-light); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-light); }
</style>
""", unsafe_allow_html=True)


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "agent_initialized" not in st.session_state:
        st.session_state.agent_initialized = False


def initialize_agent(api_key: str) -> bool:
    """Initialize the CreditCairn agent."""
    try:
        st.session_state.agent = CreditCairnAgent(api_key=api_key)
        st.session_state.agent_initialized = True
        return True
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return False


def display_welcome_message() -> None:
    """Display welcome message with SaveSage-inspired design."""
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">
            <span>🍁</span> Canada's #1 AI Credit Card Advisor
        </div>
        <h1 class="hero-title">
            Turn every spend into <span>savings</span>
        </h1>
        <p class="hero-subtitle">
            Effortlessly maximize your credit card rewards. Get personalized recommendations, 
            compare cards instantly, and never leave money on the table.
        </p>
        
        <div class="stats-bar">
            <div class="stat-item">
                <span class="stat-value">50+</span>
                <span class="stat-label">Cards Analyzed</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">$2,500+</span>
                <span class="stat-label">Avg. Annual Savings</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">24/7</span>
                <span class="stat-label">AI Assistant</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # What We Do - Feature Cards
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">What CreditCairn Does For You</h2>
        <p class="section-subtitle">Your complete credit card rewards optimization platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon green">🤖</div>
            <div class="feature-title">AI Assistant</div>
            <div class="feature-desc">Ask anything about credit cards and get instant, accurate answers.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon purple">💳</div>
            <div class="feature-title">Card Matching</div>
            <div class="feature-desc">Get personalized card recommendations based on your spending.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon orange">✈️</div>
            <div class="feature-title">Travel Free</div>
            <div class="feature-desc">Learn how to redeem points for flights and hotel stays.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon blue">📊</div>
            <div class="feature-title">Compare Cards</div>
            <div class="feature-desc">Side-by-side comparisons of fees, rewards, and perks.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Trust Badges
    st.markdown("""
    <div class="trust-bar">
        <div class="trust-badge"><span class="icon">🔒</span><span>Secure & Private</span></div>
        <div class="trust-badge"><span class="icon">🇨🇦</span><span>Canadian Data Only</span></div>
        <div class="trust-badge"><span class="icon">⚡</span><span>Instant Answers</span></div>
        <div class="trust-badge"><span class="icon">🆓</span><span>Free to Use</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Testimonials
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">What Our Users Say</h2>
        <p class="section-subtitle">Join thousands of Canadians maximizing their rewards</p>
    </div>
    """, unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    
    with t1:
        st.markdown("""
        <div class="testimonial-card">
            <p class="testimonial-quote">"CreditCairn helped me find a card that saves me $200/month on groceries. The AI recommendations are spot on!"</p>
            <div class="testimonial-author">
                <div class="author-avatar">SK</div>
                <div class="author-info">
                    <div class="author-name">Sarah K.</div>
                    <div class="author-role">Toronto, ON</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with t2:
        st.markdown("""
        <div class="testimonial-card">
            <p class="testimonial-quote">"I've earned enough points for a free trip to Vancouver just by optimizing my everyday spending. Game changer!"</p>
            <div class="testimonial-author">
                <div class="author-avatar">MR</div>
                <div class="author-info">
                    <div class="author-name">Michael R.</div>
                    <div class="author-role">Calgary, AB</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with t3:
        st.markdown("""
        <div class="testimonial-card">
            <p class="testimonial-quote">"Finally, an AI that understands Canadian credit cards. No more sifting through US-focused advice!"</p>
            <div class="testimonial-author">
                <div class="author-avatar">JP</div>
                <div class="author-info">
                    <div class="author-name">Jessica P.</div>
                    <div class="author-role">Vancouver, BC</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Action Buttons
    st.markdown("""
    <div class="section-header" style="margin-top: 1rem;">
        <h2 class="section-title">Start Saving Today</h2>
        <p class="section-subtitle">Click a question or type your own below</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🛒  Best Cards for Groceries", key="btn_grocery", use_container_width=True):
            handle_quick_prompt("What are the best credit cards for grocery shopping in Canada?")
    with col_b:
        if st.button("✈️  How to Travel for Free", key="btn_travel", use_container_width=True):
            handle_quick_prompt("How can I use credit card points to travel for free in Canada?")
            
    col_c, col_d = st.columns(2)
    with col_c:
        if st.button("💵  Best No-Fee Cards", key="btn_nofee", use_container_width=True):
            handle_quick_prompt("What are the best no annual fee credit cards in Canada?")
    with col_d:
        if st.button("🎁  Top Welcome Bonuses", key="btn_bonus", use_container_width=True):
            handle_quick_prompt("Which Canadian credit cards have the best welcome bonus right now?")


def handle_quick_prompt(prompt_text: str):
    """Handle a click on a quick prompt button."""
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    st.rerun()


def display_chat_history() -> None:
    """Display chat message history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_agent_response(user_input: str) -> str:
    """Get response from the agent."""
    try:
        response = st.session_state.agent.chat_completion(user_input)
        return response
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}\n\nPlease make sure your API key is valid and try again."


def display_sidebar() -> None:
    """Display sidebar with information and controls."""
    with st.sidebar:
        # Logo Area
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💳</div>
            <h1 style="margin: 0; font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, #10B981, #6366F1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">CreditCairn</h1>
            <p style="color: #94A3B8; font-size: 0.8rem; margin: 0.25rem 0 0 0;">AI Credit Card Advisor</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # API Connection
        with st.expander("🔑 API Connection", expanded=not bool(os.getenv("GOOGLE_API_KEY"))):
            env_api_key = os.getenv("GOOGLE_API_KEY", "")
            
            if env_api_key:
                st.success("✓ Connected", icon="🟢")
                api_key = env_api_key
                if not st.session_state.agent_initialized:
                    if initialize_agent(api_key):
                        st.rerun()
            else:
                api_key = st.text_input("Google API Key", type="password", placeholder="Enter your API key...")
                if api_key:
                    if st.button("Connect", type="primary", use_container_width=True):
                        if initialize_agent(api_key):
                            st.rerun()
                st.caption("[Get API Key →](https://makersuite.google.com/app/apikey)")
        
        st.divider()
        
        # Stats
        if st.session_state.agent_initialized:
            st.markdown("##### 📊 Session Stats")
            try:
                card_count = st.session_state.agent.retriever.collection.count()
                col1, col2 = st.columns(2)
                col1.metric("Cards", card_count)
                col2.metric("Messages", len(st.session_state.messages))
            except:
                pass
            st.divider()
        
        # Actions
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.agent:
                st.session_state.agent.start_chat()
            st.rerun()
        
        # Footer
        st.markdown("""
        <div style='margin-top: 2rem; text-align: center; padding: 1rem; background: #F8FAFC; border-radius: 8px;'>
            <p style="color: #94A3B8; font-size: 0.75rem; margin: 0;">Made with ❤️ for Canadians</p>
            <p style="color: #CBD5E1; font-size: 0.7rem; margin: 0.25rem 0 0 0;">v1.0 • Powered by Gemini AI</p>
        </div>
        """, unsafe_allow_html=True)


def main() -> None:
    """Main application function."""
    initialize_session_state()
    display_sidebar()
    
    # Show setup prompt if not initialized
    if not st.session_state.agent_initialized:
        st.markdown("""
        <div class="hero-container" style="max-width: 600px; margin: 4rem auto;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔑</div>
            <h2 style="color: #1E293B; margin-bottom: 0.5rem;">Connect to Get Started</h2>
            <p style="color: #64748B;">Enter your Google API key in the sidebar to unlock the AI assistant.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display welcome or chat
    if not st.session_state.messages:
        display_welcome_message()
    else:
        # Compact header when chatting
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1rem; padding: 0.75rem 1rem; background: white; border-radius: 12px; border: 1px solid #E2E8F0;">
            <span style="font-size: 1.5rem;">💳</span>
            <div>
                <div style="font-weight: 700; color: #1E293B; font-size: 1rem;">CreditCairn</div>
                <div style="font-size: 0.75rem; color: #10B981;">● Online</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    display_chat_history()
    
    # Process pending messages
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Finding the best advice for you..."):
                response = get_agent_response(st.session_state.messages[-1]["content"])
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about Canadian credit cards..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()


if __name__ == "__main__":
    main()
