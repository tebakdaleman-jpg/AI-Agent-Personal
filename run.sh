#!/bin/bash
# Quick start script untuk AI Agent Personal
# Usage: ./run.sh [command] or ./run.sh --ui

cd "$(dirname "$0")"

# Check .env
if [ ! -f .env ]; then
    echo "⚠️  .env belum ada, copy dari .env.example"
    cp .env.example .env
    echo "📝 Edit .env dan isi API key kamu, lalu jalankan lagi"
    echo "   https://aistudio.google.com/apikey (gratis)"
    exit 1
fi

# Check venv
if [ ! -d venv ]; then
    echo "📦 Buat virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies (skip jika sudah)
echo "📦 Install dependencies..."
pip install -q -r requirements.txt

# Jalankan
if [ "$1" == "--ui" ]; then
    echo "🎨 Jalankan Streamlit UI..."
    streamlit run ui/app.py
elif [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "Usage:"
    echo "  ./run.sh --ui        Jalankan UI"
    echo "  ./run.sh             Mode interaktif CLI"
    echo "  ./run.sh \"command\"   Jalankan 1 perintah langsung"
else
    python main.py "$@"
fi