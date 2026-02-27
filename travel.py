import streamlit as st
import google.generativeai as genai
import os
import re

# -----------------------------------------------
# Page Configuration
# -----------------------------------------------
st.set_page_config(
    page_title="✈️ AI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------
# Custom CSS
# -----------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global Reset */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }

    /* ---- Hero Banner ---- */
    .hero-banner {
        background: linear-gradient(120deg, rgba(99,102,241,0.2), rgba(139,92,246,0.15));
        border: 1px solid rgba(139,92,246,0.35);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.2;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* ---- Sidebar ---- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%) !important;
        border-right: 1px solid rgba(139,92,246,0.3);
    }
    [data-testid="stSidebar"] .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #a78bfa;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(139,92,246,0.3);
    }

    /* ---- Input Widgets ---- */
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        background: rgba(30, 27, 75, 0.7) !important;
        border: 1.5px solid rgba(139,92,246,0.4) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
        transition: border-color 0.3s ease;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
    }

    /* ---- Labels ---- */
    label, .stMarkdown p {
        color: #cbd5e1 !important;
    }

    /* ---- Generate Button ---- */
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(124,58,237,0.4) !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(124,58,237,0.6) !important;
        background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(0) !important;
    }

    /* ---- Info Card ---- */
    .info-card {
        background: rgba(30, 27, 75, 0.6);
        border: 1px solid rgba(139,92,246,0.25);
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        color: #e2e8f0;
        backdrop-filter: blur(8px);
        margin-bottom: 1rem;
    }
    .info-card-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .info-card-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    .info-card-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #a78bfa;
    }

    /* ---- Itinerary Output ---- */
    .itinerary-container {
        background: rgba(15, 12, 41, 0.7);
        border: 1px solid rgba(139,92,246,0.3);
        border-radius: 18px;
        padding: 2rem;
        backdrop-filter: blur(12px);
        margin-top: 1.5rem;
    }
    .itinerary-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #a78bfa;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 1px solid rgba(139,92,246,0.25);
        padding-bottom: 0.75rem;
    }
    .itinerary-body {
        color: #cbd5e1;
        line-height: 1.8;
        font-size: 0.97rem;
        white-space: pre-wrap;
    }

    /* ---- Feature Pills ---- */
    .feature-pill {
        display: inline-block;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.35);
        border-radius: 50px;
        padding: 0.3rem 0.9rem;
        font-size: 0.82rem;
        color: #a5b4fc;
        font-weight: 500;
        margin: 0.2rem;
    }

    /* ---- Expanders (Day cards) ---- */
    [data-testid="stExpander"] {
        background: rgba(30, 27, 75, 0.55) !important;
        border: 1px solid rgba(139,92,246,0.25) !important;
        border-radius: 12px !important;
        margin-bottom: 0.75rem !important;
    }
    [data-testid="stExpander"] summary {
        color: #c4b5fd !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* ---- Success / Error / Warning ---- */
    .stAlert {
        border-radius: 12px !important;
    }

    /* ---- Spinner ---- */
    .stSpinner > div {
        border-top-color: #a78bfa !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #1e1b4b; }
    ::-webkit-scrollbar-thumb { background: #7c3aed; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #a78bfa; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------
# Configure Gemini
# -----------------------------------------------
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 **API key not found.** Please set the `GEMINI_API_KEY` environment variable.")
    st.info("💡 **How to fix:** In Streamlit Cloud, go to **Settings → Secrets** and add `GEMINI_API_KEY = 'your-key'`.")
    st.stop()

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 4096,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config
)


# -----------------------------------------------
# Itinerary Generator
# -----------------------------------------------
def generate_itinerary(destination, days, nights, travel_style, budget):
    prompt = (
        f"Create a detailed, day-by-day travel itinerary for a trip to {destination}.\n"
        f"Duration: {days} days and {nights} nights.\n"
        f"Travel style: {travel_style}.\n"
        f"Budget level: {budget}.\n\n"
        "Format the itinerary with clear sections for each day:\n"
        "- Day number and theme\n"
        "- Morning, Afternoon, Evening activities\n"
        "- Local food recommendations for each meal\n"
        "- Practical travel tips and estimated costs\n"
        "- Must-see spots and hidden gems\n\n"
        "Make it engaging, specific and highly practical."
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error generating itinerary: {e}"


def parse_days(itinerary_text):
    """Split itinerary text into individual day sections."""
    pattern = r'(?:^|\n)(Day\s+\d+[^\n]*)'
    parts = re.split(pattern, itinerary_text, flags=re.IGNORECASE)
    days = []
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            title = parts[i].strip()
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            days.append((title, content))
    return days


# -----------------------------------------------
# Hero Section
# -----------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🌍 AI Travel Planner</div>
    <div class="hero-subtitle">Powered by Google Gemini · Personalized itineraries in seconds</div>
    <div style="margin-top: 1rem;">
        <span class="feature-pill">🗓️ Day-by-Day Plans</span>
        <span class="feature-pill">🍜 Food Recommendations</span>
        <span class="feature-pill">💡 Travel Tips</span>
        <span class="feature-pill">🏛️ Hidden Gems</span>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------
# Sidebar — Inputs
# -----------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">🧳 Trip Details</div>', unsafe_allow_html=True)

    destination = st.text_input(
        "🌐 Destination",
        placeholder="e.g. Tokyo, Japan",
        help="Enter any city, country, or region"
    )

    col1, col2 = st.columns(2)
    with col1:
        days = st.number_input("☀️ Days", min_value=1, max_value=30, value=5, step=1)
    with col2:
        nights = st.number_input("🌙 Nights", min_value=0, max_value=30, value=4, step=1)

    travel_style = st.selectbox(
        "🎒 Travel Style",
        ["Adventure & Outdoors", "Cultural & Historical", "Luxury & Relaxation",
         "Budget Backpacker", "Foodie & Culinary", "Family-Friendly", "Romantic Getaway"],
        index=0,
        help="Choose the vibe of your trip"
    )

    budget = st.select_slider(
        "💰 Budget Level",
        options=["Budget", "Mid-Range", "Luxury", "Ultra-Luxury"],
        value="Mid-Range"
    )

    st.markdown("---")
    generate_btn = st.button("✨ Generate My Itinerary", use_container_width=True)

    st.markdown("---")
    st.markdown("""
    <div style="color: #64748b; font-size: 0.78rem; line-height: 1.6;">
        <strong style="color:#a78bfa;">How it works:</strong><br>
        1. Enter your destination<br>
        2. Set trip duration<br>
        3. Pick style & budget<br>
        4. Click Generate!
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------
# Main Content
# -----------------------------------------------
if not generate_btn:
    # Show summary cards if destination filled
    if destination:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-icon">📍</div>
                <div class="info-card-label">Destination</div>
                <div class="info-card-value" style="font-size:1.2rem;">{destination}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-icon">🗓️</div>
                <div class="info-card-label">Duration</div>
                <div class="info-card-value">{days}D / {nights}N</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-icon">💰</div>
                <div class="info-card-label">Budget</div>
                <div class="info-card-value" style="font-size:1.1rem;">{budget}</div>
            </div>""", unsafe_allow_html=True)
    else:
        # Welcome message
        st.markdown("""
        <div style="text-align:center; padding: 4rem 2rem; color: #475569;">
            <div style="font-size: 5rem; margin-bottom: 1rem;">✈️</div>
            <div style="font-size: 1.3rem; font-weight: 600; color: #94a3b8;">
                Enter your destination in the sidebar to get started
            </div>
            <div style="font-size: 0.95rem; margin-top: 0.5rem; color: #475569;">
                Your AI-powered travel planner is ready to craft the perfect itinerary
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # Validate
    if not destination.strip():
        st.error("📍 Please enter a destination before generating.")
    elif days < 1:
        st.error("🗓️ Trip must be at least 1 day.")
    else:
        # Summary cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-icon">📍</div>
                <div class="info-card-label">Destination</div>
                <div class="info-card-value" style="font-size:1.1rem;">{destination}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-icon">☀️</div>
                <div class="info-card-label">Days / Nights</div>
                <div class="info-card-value">{days}D {nights}N</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-icon">🎒</div>
                <div class="info-card-label">Style</div>
                <div class="info-card-value" style="font-size:0.95rem;">{travel_style.split('&')[0].strip()}</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-icon">💰</div>
                <div class="info-card-label">Budget</div>
                <div class="info-card-value" style="font-size:1rem;">{budget}</div>
            </div>""", unsafe_allow_html=True)

        # Generate
        with st.spinner("🌍 Crafting your personalized itinerary with AI..."):
            itinerary = generate_itinerary(destination, days, nights, travel_style, budget)

        st.success(f"✅ Your {days}-day itinerary for **{destination}** is ready!")

        # Parse into days
        day_sections = parse_days(itinerary)

        if day_sections:
            st.markdown('<div class="itinerary-header">📋 Your Personalized Itinerary</div>', unsafe_allow_html=True)
            for title, content in day_sections:
                with st.expander(f"📅 {title}", expanded=(len(day_sections) == 1)):
                    st.markdown(f'<div class="itinerary-body">{content}</div>', unsafe_allow_html=True)
        else:
            # Fallback: show raw
            st.markdown('<div class="itinerary-container">', unsafe_allow_html=True)
            st.markdown('<div class="itinerary-header">📋 Your Personalized Itinerary</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="itinerary-body">{itinerary}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Download
        st.download_button(
            label="⬇️ Download Itinerary as .txt",
            data=itinerary,
            file_name=f"{destination.replace(' ', '_')}_itinerary.txt",
            mime="text/plain",
            use_container_width=True,

        )
