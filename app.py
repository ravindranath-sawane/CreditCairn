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
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/yourusername/CreditCairn',
        'Report a bug': "https://github.com/yourusername/CreditCairn/issues",
        'About': "# CreditCairn\nAI-powered credit card assistant."
    }
)

# Premium Red, White & Blue Theme with Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary: #DC143C;
        --primary-dark: #8B0000;
        --primary-light: #FFE4E1;
        --secondary: #1E40AF;
        --secondary-light: #DBEAFE;
        --accent: #FFFFFF;
        --bg-white: #FFFFFF;
        --bg-light: #F0F9FF;
        --bg-gradient: linear-gradient(135deg, #FFE4E1 0%, #F0F9FF 50%, #FFFFFF 100%);
        --text-dark: #0F172A;
        --text-medium: #334155;
        --text-light: #64748B;
        --border: #CBD5E1;
        --shadow-sm: 0 2px 8px rgba(220, 20, 60, 0.1);
        --shadow-md: 0 8px 16px rgba(30, 64, 175, 0.15);
        --shadow-lg: 0 16px 32px rgba(220, 20, 60, 0.2);
        --shadow-xl: 0 20px 40px rgba(30, 64, 175, 0.25);
        --radius: 16px;
        --radius-sm: 8px;
        --radius-lg: 24px;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(220, 20, 60, 0.4); }
        50% { box-shadow: 0 0 0 10px rgba(220, 20, 60, 0); }
    }
    
    @keyframes bounce-in {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes rotate-gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hide Main Menu/Footer */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* 
       FLOATING CHAT OVERLAY & STATIC MAIN PAGE
       The critical part is detaching the sidebar from the flow entirely.
    */
    
    /* 1. Force sidebar to be a floating box on the right */
    section[data-testid="stSidebar"] {
        width: 400px !important;
        min-width: 400px !important; /* Force width */
        max-width: 400px !important; /* Prevent expansion */
        height: 600px !important;
        position: fixed !important;
        right: 30px !important;
        bottom: 30px !important;
        left: unset !important;
        top: auto !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2) !important;
        border-radius: 20px !important;
        border: 1px solid #e2e8f0;
        z-index: 1000000 !important;
        transform: none !important; /* Stop Streamlit from sliding it */
        transition: none !important;
    }
    
    /* Force inner content to match width */
    div[data-testid="stSidebarUserContent"] {
        width: 100% !important;
        padding: 0 !important;
    }

    /* 2. Style the "Toggle Button" (Collapsed Sidebar) */
    [data-testid="stSidebarCollapsedControl"] {
        background: linear-gradient(135deg, #00205B, #DC143C) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        position: fixed !important;
        right: 30px !important;
        bottom: 30px !important;
        left: unset !important;
        top: auto !important;
        z-index: 1000001 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        display: grid !important;
        place-items: center !important;
        border: 2px solid white !important;
        transform: none !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] svg {
        fill: white !important;
        width: 24px !important;
        height: 24px !important;
    }

    /* MINIMIZE BUTTON (Inside Open Chat) - Targeting the StSidebar close button */
    section[data-testid="stSidebar"] button[kind="header"] {
        display: block !important; /* Ensure it's not hidden */
        position: absolute !important;
        top: 15px !important;
        right: 15px !important;
        z-index: 1000002 !important;
        background: transparent !important;
        border: none !important;
        color: #64748B !important;
        transition: transform 0.2s ease !important;
    }
    
    section[data-testid="stSidebar"] button[kind="header"]:hover {
        transform: scale(1.1) !important;
        color: #DC143C !important;
        background: rgba(0,0,0,0.05) !important;
        border-radius: 50% !important;
    }
    
    section[data-testid="stSidebar"] button[kind="header"] svg {
        width: 20px !important;
        height: 20px !important;
    }

    /* 3. CRITICAL: Prevent Main Page from shrinking when Sidebar opens */
    .stApp > header { display: none !important; } /* Hide top header bar completely */
    
    section[data-testid="stSidebar"] + div {
        margin-left: 0 !important; /* Don't shift content */
        max-width: 100% !important;
    }
    
    .main .block-container {
        max-width: 1200px !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Header for the chat window */
    .floating-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: linear-gradient(135deg, #00205B, #DC143C);
        z-index: 999;
        display: flex;
        align-items: center;
        padding: 0 1.5rem;
        border-radius: 20px 20px 0 0;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
    }

    /* Custom Chat Input Adjustments */
    .stChatInputContainer {
        padding-bottom: 1rem !important;
    }

    /* Branding Header */
    .branding-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    
    .branding-logo {
        font-size: 2.2rem;
    }
    
    .branding-title {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00205B 0%, #DC143C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    /* Base styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container {
        padding: 2rem 1rem;
        max-width: 1200px;
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6, p, label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    h1, h2, h3 {
        color: var(--text-dark) !important;
        animation: fadeInDown 0.6s ease-out;
    }
    
    p {
        color: var(--text-medium) !important;
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Table Styling */
    table {
        color: var(--text-dark) !important;
        width: 100%;
        border-collapse: collapse;
    }
    
    th, td {
        color: var(--text-dark) !important;
        border-bottom: 1px solid #e9ecef !important;
        padding: 0.75rem !important;
    }
    
    th {
        background-color: transparent !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #DC143C !important;
    }
    
    div[data-testid="stMarkdownContainer"] table {
        color: var(--text-dark) !important;
    }
    
    div[data-testid="stMarkdownContainer"] th, 
    div[data-testid="stMarkdownContainer"] td {
        color: var(--text-dark) !important;
    }
    
    /* Hero Section - Clean & Modern */
    .hero-container {
        background: white;
        text-align: center;
        padding: 5rem 1rem 3rem 1rem;
        margin-bottom: 2rem;
    }
    
    .hero-container::before, .hero-container::after {
        display: none;
    }
    
    .hero-badge {
        display: inline-block;
        background: #F0F9FF;
        color: #00205B !important;
        border: 1px solid #DBEAFE;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .hero-title {
        font-size: 3.8rem;
        font-weight: 900;
        line-height: 1.1;
        margin: 0 0 1.5rem 0;
        color: #0F172A !important;
        letter-spacing: -1px;
    }
    
    .hero-title span {
        background: linear-gradient(135deg, #DC143C 0%, #00205B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #64748B !important;
        max-width: 650px;
        margin: 0 auto 2.5rem auto;
        line-height: 1.6;
        font-weight: 400;
    }
    
    /* Stats Bar */
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 3rem;
        flex-wrap: wrap;
        padding: 2rem 0;
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.8s ease-out 0.4s both;
    }
    
    .stat-item {
        text-align: center;
        animation: bounce-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) var(--delay, 0s);
        transition: all 0.3s ease;
    }
    
    .stat-item:nth-child(1) { --delay: 0.4s; }
    .stat-item:nth-child(2) { --delay: 0.5s; }
    .stat-item:nth-child(3) { --delay: 0.6s; }
    
    .stat-item:hover {
        transform: scale(1.1);
        filter: drop-shadow(0 10px 20px rgba(220, 20, 60, 0.3));
    }
    
    .stat-value {
        font-size: 2.8rem;
        font-weight: 950;
        color: #FFFFFF !important;
        display: block;
        line-height: 1;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    /* Feature Cards */
    .feature-card {
        background: #FFFFFF;
        border: 1px solid #e9ecef;
        border-radius: var(--radius);
        padding: 2rem;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #DC143C, #1E40AF);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
        border-color: rgba(220, 20, 60, 0.2);
    }
    
    .feature-icon {
        width: 56px;
        height: 56px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.75rem;
        margin-bottom: 1.25rem;
        transition: all 0.3s ease;
        animation: bounce-in 0.6s ease-out;
    }
    
    .feature-icon.red { background: linear-gradient(135deg, #fee2e2, #fecaca); color: #DC143C; }
    .feature-icon.blue { background: linear-gradient(135deg, #dbeafe, #bfdbfe); color: #1E40AF; }
    .feature-icon.white { background: linear-gradient(135deg, #f8fafc, #f1f5f9); color: #475569; }
    .feature-icon.gradient { background: linear-gradient(135deg, #fee2e2, #dbeafe); color: #DC143C; }
    
    .feature-card:hover .feature-icon {
        transform: translateY(-4px) scale(1.05);
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--text-dark) !important;
        margin-bottom: 0.75rem;
    }
    
    .feature-desc {
        font-size: 0.95rem;
        color: var(--text-medium) !important;
        line-height: 1.7;
    }
    
    /* Section Headers */
    .section-header {
        text-align: center;
        margin: 4rem 0 3rem 0;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .section-title {
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #DC143C, #1E40AF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.75rem;
    }
    
    .section-subtitle {
        font-size: 1.1rem;
        color: var(--text-light) !important;
        font-weight: 500;
    }
    
    /* Testimonial Cards */
    .testimonial-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFE4E1 100%);
        border: 2px solid #DC143C;
        border-radius: var(--radius);
        padding: 2rem;
        box-shadow: var(--shadow-lg);
        transition: all 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .testimonial-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(220, 20, 60, 0.3);
        border-color: #1E40AF;
    }
    
    .testimonial-quote {
        font-size: 1rem;
        color: var(--text-medium) !important;
        font-style: italic;
        line-height: 1.8;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    
    .testimonial-author {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .author-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #DC143C, #1E40AF);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 1rem;
        color: white;
        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.3);
        animation: bounce-in 0.6s ease-out;
    }
    
    .author-name {
        font-weight: 700;
        font-size: 0.95rem;
        color: var(--text-dark) !important;
    }
    
    .author-role {
        font-size: 0.85rem;
        color: var(--text-light) !important;
    }
    
    /* Trust Badges */
    .trust-bar {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2.5rem;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(220, 20, 60, 0.05), rgba(30, 64, 175, 0.05));
        border-radius: var(--radius);
        border: 2px dashed #DC143C;
        margin: 3rem 0;
        flex-wrap: wrap;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .trust-badge {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 0.9rem;
        color: var(--text-medium);
        font-weight: 700;
        animation: slideInLeft 0.6s ease-out;
    }
    
    .trust-badge .icon {
        font-size: 1.5rem;
        animation: bounce-in 0.6s ease-out;
    }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
        border: none;
        color: white !important;
        border-radius: var(--radius-sm);
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.85rem 2rem;
        height: auto;
        transition: all 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(220, 20, 60, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    div.stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        animation: shimmer 3s infinite;
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(220, 20, 60, 0.4), 0 0 30px rgba(30, 64, 175, 0.2);
    }
    
    div.stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 10px 20px rgba(220, 20, 60, 0.3);
    }
    
    /* Chat Messages */
    div[data-testid="stChatMessage"] {
        background: linear-gradient(135deg, #FFFFFF, #F0F9FF);
        border: 1px solid #CBD5E1;
        border-radius: var(--radius);
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-md);
        animation: fadeInUp 0.4s ease-out;
    }
    
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, #FFE4E1, #F0F9FF);
        border-color: rgba(220, 20, 60, 0.3);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF, #F0F9FF);
        border-right: 2px solid #DC143C;
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        background: var(--bg-white) !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-dark) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 0.85rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #DC143C !important;
        box-shadow: 0 0 0 4px rgba(220, 20, 60, 0.15) !important;
        outline: none !important;
    }
    
    .stChatInputContainer textarea {
        background: var(--bg-white) !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: var(--radius) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: #DC143C !important;
        box-shadow: 0 0 0 4px rgba(220, 20, 60, 0.15) !important;
        outline: none !important;
    }
    
    /* Metrics */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFFFF, #F0F9FF);
        border: 2px solid #DC143C;
        border-radius: var(--radius-sm);
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        animation: fadeInUp 0.6s ease-out;
    }
    
    div[data-testid="metric-container"] label { color: var(--text-light) !important; }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #DC143C !important;
        font-weight: 900;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #FFE4E1, #F0F9FF) !important;
        border: 1px solid #DC143C !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 700 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #DC143C, #1E40AF);
        margin: 2rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: var(--bg-light); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #DC143C, #1E40AF);
        border-radius: 5px;
        animation: rotate-gradient 3s linear infinite;
    }
    ::-webkit-scrollbar-thumb:hover { opacity: 0.8; }
    
    /* Global animations */
    * {
        box-sizing: border-box;
    }
    
    .stMarkdown code {
        background: linear-gradient(135deg, #FFE4E1, #F0F9FF) !important;
        border: 1px solid #DC143C !important;
        border-radius: 4px !important;
        padding: 0.25rem 0.5rem !important;
        color: #8B0000 !important;
        font-weight: 600 !important;
    }
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
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False


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
    
def handle_quick_prompt(prompt_text: str):
    """Handle a click on a quick prompt button."""
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    st.rerun()


def get_agent_response(user_input: str) -> str:
    """Get response from the agent."""
    try:
        response = st.session_state.agent.chat_completion(user_input)
        return response
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}\n\nPlease make sure your API key is valid and try again."


def render_chat_interface() -> None:
    """Render chat interface in the floating sidebar."""
    with st.sidebar:
        st.markdown("""
        <div style="padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #0F172A;">💬 CreditCairn Assistant</h3>
            <p style="margin: 0; font-size: 0.8rem; color: #64748B;">Ask me anything about credit cards</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick prompts (Compact Grid)
        if not st.session_state.messages:
             st.markdown('<p style="font-size: 0.75rem; font-weight: 700; color: #334155; margin-bottom: 0.5rem;">SUGGESTED</p>', unsafe_allow_html=True)
             c1, c2 = st.columns(2)
             with c1:
                 if st.button("🛒 Groceries", use_container_width=True):
                     handle_quick_prompt("What are the best credit cards for grocery shopping in Canada?")
                 if st.button("💵 No Fees", use_container_width=True):
                     handle_quick_prompt("What are the best no annual fee credit cards in Canada?")
             with c2:
                 if st.button("✈️ Travel", use_container_width=True):
                     handle_quick_prompt("How can I use credit card points to travel for free in Canada?")
                 if st.button("🎁 Bonuses", use_container_width=True):
                     handle_quick_prompt("Which Canadian credit cards have the best welcome bonus right now?")
             st.divider()

        # Chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Process pending user message
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_agent_response(st.session_state.messages[-1]["content"])
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

        # Input is handled by st.chat_input automatically at the bottom of the sidebar
        if prompt := st.chat_input("Type your question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()


def main() -> None:
    """Main application function."""
    initialize_session_state()
    
    # Auto-initialize agent from environment (no API/settings UI on page)
    if not st.session_state.agent_initialized:
        env_api_key = os.getenv("GOOGLE_API_KEY", "")
        if env_api_key:
            initialize_agent(env_api_key)
    
    # Always render branding and landing page content in Main Area
    st.markdown("""
    <div class="branding-header">
        <div class="branding-logo">💳</div>
        <h1 class="branding-title">CreditCairn</h1>
    </div>
    """, unsafe_allow_html=True)
    
    display_welcome_message()
    
    # Render Floating Chat Interface
    render_chat_interface()


if __name__ == "__main__":
    main()
