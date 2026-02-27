import streamlit as st
import google.generativeai as genai
import os

# -----------------------------------------------
# Page Config
# -----------------------------------------------
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------
# CSS — Clean, modern flat dark theme
# -----------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Background */
.stApp {
    background-color: #0e1117;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b27 !important;
    border-right: 1px solid #1e2a3a;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }

/* Widget labels */
label { color: #8b949e !important; font-size: 0.82rem !important; letter-spacing: 0.4px; text-transform: uppercase; }

/* Text inputs */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background: #161b27 !important;
    border: 1px solid #21262d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 2px rgba(88,166,255,0.12) !important;
}

/* Selectbox / slider */
div[data-testid="stSelectbox"] > div,
div[data-testid="stSelectSlider"] > div { color: #e6edf3; }

/* Generate button */
div[data-testid="stButton"] > button {
    background: #1f6feb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.5rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: background 0.2s ease !important;
    letter-spacing: 0.3px !important;
}
div[data-testid="stButton"] > button:hover {
    background: #388bfd !important;
}

/* Download button */
div[data-testid="stDownloadButton"] > button {
    background: #161b27 !important;
    color: #58a6ff !important;
    border: 1px solid #21262d !important;
    border-radius: 8px !important;
    width: 100% !important;
    font-weight: 500 !important;
    margin-top: 1rem !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    border-color: #58a6ff !important;
    background: #1c2231 !important;
}

/* Hero */
.hero {
    padding: 2.5rem 0 1.5rem 0;
    border-bottom: 1px solid #21262d;
    margin-bottom: 2rem;
}
.hero h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #e6edf3;
    margin: 0 0 0.3rem 0;
}
.hero p {
    color: #8b949e;
    font-size: 0.95rem;
    margin: 0;
}

/* Summary strip */
.summary-strip {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}
.strip-card {
    flex: 1;
    background: #161b27;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
.strip-card .slabel {
    font-size: 0.72rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.3rem;
}
.strip-card .svalue {
    font-size: 1.05rem;
    font-weight: 600;
    color: #e6edf3;
}

/* Day card */
.day-card {
    background: #161b27;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.day-card .day-title {
    font-size: 1rem;
    font-weight: 600;
    color: #58a6ff;
    margin-bottom: 0.8rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #21262d;
}
.day-card .day-body {
    color: #c9d1d9;
    font-size: 0.9rem;
    line-height: 1.75;
    white-space: pre-wrap;
}

/* Placeholder */
.placeholder {
    text-align: center;
    padding: 6rem 2rem;
    color: #484f58;
}
.placeholder .icon { font-size: 4rem; margin-bottom: 1rem; }
.placeholder .text { font-size: 1rem; color: #6e7681; }

/* Spinner */
.stSpinner > div { border-top-color: #58a6ff !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0e1117; }
::-webkit-scrollbar-thumb { background: #21262d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #30363d; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------
# Gemini Setup
# -----------------------------------------------
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 **API key not found.** Set the `GEMINI_API_KEY` environment variable.")
    st.code("$env:GEMINI_API_KEY = 'your-key-here'  # PowerShell", language="powershell")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.95,
        "max_output_tokens": 8192,
    }
)

# -----------------------------------------------
# Prompt — uses a reliable sentinel so parsing never breaks
# -----------------------------------------------
SENTINEL = "###DAY###"

def generate_itinerary(destination, days, nights, style, budget):
    prompt = f"""You are an expert travel planner. Create a complete, detailed {days}-day travel itinerary for {destination}.

STRICT RULES:
- You MUST include ALL {days} days. Do not stop early.
- Budget level: {budget}
- Travel style: {style}
- Trip duration: {days} days and {nights} nights
- Every single day MUST begin on a new line with this EXACT format:
  {SENTINEL} Day N: <short theme title>
  Example: {SENTINEL} Day 1: Arrival & First Impressions
- Under each day include:
  - Morning, Afternoon, Evening breakdown
  - Specific places, landmarks and activities with timings
  - Breakfast, Lunch and Dinner spots with real restaurant names
  - Useful local tips or rough costs
- Do NOT use any other format for day headings.
- Complete ALL {days} days before finishing.

Begin the full {days}-day itinerary now:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"


def parse_days(text):
    """Split on the sentinel to get reliable day sections."""
    parts = text.split(SENTINEL)
    days = []
    for chunk in parts:
        chunk = chunk.strip()
        if not chunk:
            continue
        lines = chunk.splitlines()
        title = lines[0].strip().lstrip("#").strip()
        body = "\n".join(lines[1:]).strip()
        if title:
            days.append((title, body))
    return days


# -----------------------------------------------
# Sidebar
# -----------------------------------------------
with st.sidebar:
    st.markdown("### ✈️ Trip Settings")
    st.markdown("---")

    destination = st.text_input("Destination", placeholder="e.g. Tokyo, Japan")

    col1, col2 = st.columns(2)
    with col1:
        days = st.number_input("Days", min_value=1, max_value=30, value=4, step=1)
    with col2:
        nights = st.number_input("Nights", min_value=0, max_value=30, value=4, step=1)

    style = st.selectbox("Travel Style", [
        "Cultural & Historical",
        "Adventure & Outdoors",
        "Luxury & Relaxation",
        "Budget Backpacker",
        "Foodie & Culinary",
        "Family-Friendly",
        "Romantic Getaway",
    ])

    budget = st.select_slider("Budget", options=["Budget", "Mid-Range", "Luxury", "Ultra-Luxury"], value="Mid-Range")

    st.markdown("---")
    go = st.button("Generate Itinerary", use_container_width=True)

# -----------------------------------------------
# Main
# -----------------------------------------------

# Hero bar
st.markdown("""
<div class="hero">
    <h1>✈️ AI Travel Planner</h1>
    <p>Powered by Google Gemini · Personalized day-by-day itineraries</p>
</div>
""", unsafe_allow_html=True)

if not go:
    if destination.strip():
        # Small preview strip
        st.markdown(f"""
        <div class="summary-strip">
            <div class="strip-card"><div class="slabel">📍 Destination</div><div class="svalue">{destination}</div></div>
            <div class="strip-card"><div class="slabel">🗓️ Duration</div><div class="svalue">{days} days · {nights} nights</div></div>
            <div class="strip-card"><div class="slabel">🎒 Style</div><div class="svalue">{style}</div></div>
            <div class="strip-card"><div class="slabel">💰 Budget</div><div class="svalue">{budget}</div></div>
        </div>
        """, unsafe_allow_html=True)
        st.info("👆 Hit **Generate Itinerary** in the sidebar when you're ready.")
    else:
        st.markdown("""
        <div class="placeholder">
            <div class="icon">🌍</div>
            <div class="text">Enter a destination in the sidebar to get started.</div>
        </div>
        """, unsafe_allow_html=True)

else:
    if not destination.strip():
        st.error("Please enter a destination first.")
        st.stop()

    # Summary strip
    st.markdown(f"""
    <div class="summary-strip">
        <div class="strip-card"><div class="slabel">📍 Destination</div><div class="svalue">{destination}</div></div>
        <div class="strip-card"><div class="slabel">🗓️ Duration</div><div class="svalue">{days} days · {nights} nights</div></div>
        <div class="strip-card"><div class="slabel">🎒 Style</div><div class="svalue">{style}</div></div>
        <div class="strip-card"><div class="slabel">💰 Budget</div><div class="svalue">{budget}</div></div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(f"Building your {days}-day {destination} itinerary..."):
        raw = generate_itinerary(destination, days, nights, style, budget)

    day_sections = parse_days(raw)

    if day_sections:
        st.success(f"✅ {len(day_sections)}-day itinerary for **{destination}** is ready!")
        st.markdown(f"**{destination} · {days}D {nights}N · {style} · {budget}**")
        st.markdown("---")
        for title, body in day_sections:
            st.markdown(f"""
            <div class="day-card">
                <div class="day-title">📅 {title}</div>
            </div>
            """, unsafe_allow_html=True)
            # Use st.markdown so ** and * render as bold/italic properly
            with st.container():
                st.markdown(
                    f"<div style='padding: 0 1.6rem 1.2rem 1.6rem; margin-top:-1rem;'></div>",
                    unsafe_allow_html=True
                )
                st.markdown(body)
    else:
        # Fallback: raw output (shouldn't normally hit this)
        st.success(f"✅ Itinerary for **{destination}** generated!")
        st.markdown("---")
        st.markdown(f'<div class="day-card"><div class="day-body">{raw}</div></div>', unsafe_allow_html=True)

    st.download_button(
        label="⬇️ Download Itinerary (.txt)",
        data=raw.replace(SENTINEL, ""),
        file_name=f"{destination.replace(' ', '_')}_itinerary.txt",
        mime="text/plain",
    )
