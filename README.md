# ✈️ AI Travel Planner

A **personalized travel itinerary generator** powered by Google Gemini AI, built with Streamlit. Enter your destination, trip duration, travel style, and budget — and get a detailed day-by-day itinerary in seconds.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-AI-purple?logo=google)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌟 Features

- 🗓️ **Day-by-day itineraries** with morning, afternoon & evening activities
- 🍜 **Food recommendations** for every meal
- 🏛️ **Hidden gems** alongside must-see attractions
- 🎒 **Travel style selector** — Adventure, Cultural, Luxury, Foodie & more
- 💰 **Budget levels** — Budget to Ultra-Luxury
- ⬇️ **Download** your itinerary as a `.txt` file
- 🎨 **Premium dark UI** with responsive layout

---

## 🗂️ Project Structure

```
ai-travel-planner/
├── travel.py          # Main Streamlit app
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## ⚙️ Setup & Local Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-travel-planner.git
cd ai-travel-planner
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Gemini API key

Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey), then:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
```

**macOS / Linux:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 4. Run the app
```bash
streamlit run travel.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🚀 Deploy to Streamlit Cloud (Free)

1. **Push this repo to GitHub** (must be public)
2. Go to **[share.streamlit.io](https://share.streamlit.io)** → Sign in with GitHub → **New App**
3. Select your repo, set **Main file path** to `travel.py`, click **Deploy**
4. Go to **Settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
5. Your app is live at `https://your-username-ai-travel-planner.streamlit.app` 🎉

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web app framework |
| [Google Gemini AI](https://ai.google.dev) | Itinerary generation |
| Python 3.9+ | Core language |

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
