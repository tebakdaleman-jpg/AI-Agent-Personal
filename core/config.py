"""Konfigurasi utama project AI Agent Personal."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Path
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
INPUTS_DIR = DATA_DIR / "inputs"
OUTPUTS_DIR = DATA_DIR / "outputs"
REPORTS_DIR = DATA_DIR / "reports"
ANIMATIONS_DIR = ROOT_DIR / "ui" / "animations"

# Pastikan folder ada
for d in [DATA_DIR, INPUTS_DIR, OUTPUTS_DIR, REPORTS_DIR, ANIMATIONS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def _get_secret(key: str, default: str = "") -> str:
    """Ambil secret dari Streamlit st.secrets (kalau ada), fallback ke env.

    Ini agar deployment ke Streamlit Cloud gampang - tinggal set di secrets UI.
    """
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)


# API Keys - support .env (local) ATAU Streamlit secrets (cloud)
GOOGLE_API_KEY = _get_secret("GOOGLE_API_KEY", "")
GROQ_API_KEY = _get_secret("GROQ_API_KEY", "")
HUGGINGFACE_API_KEY = _get_secret("HUGGINGFACE_API_KEY", "")

# Models
GEMINI_MODEL = _get_secret("GEMINI_MODEL", "gemini-flash-lite-latest")
GROQ_MODEL = _get_secret("GROQ_MODEL", "llama-3.3-70b-versatile")

# App settings
APP_LANGUAGE = _get_secret("APP_LANGUAGE", "id")
DEFAULT_TIMEZONE = _get_secret("DEFAULT_TIMEZONE", "Asia/Jakarta")

# 6 Daftar Agent
AGENTS = {
    "agent1": {
        "name": "Rimba - Social Media Researcher",
        "role": "Riset Sosial Media Instagram & TikTok",
        "emoji": "🔍",
        "color": "#FF6B6B",
    },
    "agent2": {
        "name": "Karya - Content Planner",
        "role": "Content Plan & Script Viral 1 Bulan",
        "emoji": "✍️",
        "color": "#4ECDC4",
    },
    "agent3": {
        "name": "Lensa - Analytics Reporter",
        "role": "Report Sosial Media Mingguan & Bulanan",
        "emoji": "📊",
        "color": "#FFD93D",
    },
    "agent4": {
        "name": "Stratego - Marketing Planner",
        "role": "Plan Marketing Online + Offline 1 Bulan",
        "emoji": "📋",
        "color": "#6C5CE7",
    },
    "agent5": {
        "name": "Navi - Marketing Strategist",
        "role": "Strategi Marketing Offline & IG/TikTok",
        "emoji": "🧭",
        "color": "#A29BFE",
    },
    "agent6": {
        "name": "Hemat - Ads Researcher",
        "role": "Riset Meta/TikTok/Google Ads + Budget",
        "emoji": "💰",
        "color": "#FD79A8",
    },
}

# Lottie animation URLs (free LottieFiles - CC0)
ANIMATIONS = {
    "thinking": "https://lottie.host/files/4f3e8e6e-2c8e-4f5e-9c5e-8e6e2c8e4f5e/9XKgKw7IhQ.json",
    "working": "https://assets3.lottiefiles.com/packages/lf20_x62chJ.json",
    "complete": "https://assets1.lottiefiles.com/packages/lf20_s2yranru.json",
    "robot_thinking": "https://assets10.lottiefiles.com/packages/lf20_VbrWqV.json",
}