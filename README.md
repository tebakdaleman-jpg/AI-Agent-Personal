# AI Agent Personal 🤖

6 AI Agents siap membantu pekerjaan sosial media, content, marketing, dan ads kamu.

## 🎯 Daftar Agent

| # | Emoji | Nama | Tugas |
|---|-------|------|-------|
| 1 | 🔍 | **Rimba** | Riset Instagram & TikTok, analisis niche |
| 2 | ✍️ | **Karya** | Content plan 1 bulan + script viral |
| 3 | 📊 | **Lensa** | Report analytics mingguan & bulanan |
| 4 | 📋 | **Stratego** | Marketing plan online + offline |
| 5 | 🧭 | **Navi** | Strategi marketing komprehensif |
| 6 | 💰 | **Hemat** | Riset ads + budget calculation |

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /Users/user/ai-agent-personal
pip install -r requirements.txt
```

### 2. Setup API Key (GRATIS)

**Cara termudah - Google Gemini:**
1. Buka https://aistudio.google.com/apikey
2. Login dengan Google account
3. Klik "Create API Key"
4. Copy API key

**Alternatif - Groq (lebih cepat):**
1. Buka https://console.groq.com/keys
2. Sign up gratis
3. Create API key

### 3. Konfigurasi
```bash
cp .env.example .env
# Edit .env, paste API key kamu
```

### 4. Jalankan

**Mode UI (dengan animasi kartun):**
```bash
streamlit run ui/app.py
# atau
python main.py --ui
```

**Mode CLI (terminal):**
```bash
python main.py
# atau langsung:
python main.py "riset instagram @namaakun"
```

**Akses UI:** http://localhost:8501

## 💡 Contoh Perintah

```
riset instagram @brandkamu
buat content plan untuk niche parenting
report mingguan (paste data performa di sini)
marketing plan F&B budget 5 juta
strategi marketing untuk fashion
riset ads untuk skincare budget 3 juta
```

## 🛠️ Tech Stack (100% Gratis)

| Komponen | Tools | Biaya |
|----------|-------|-------|
| Multi-agent | [CrewAI](https://github.com/crewAIInc/crewAI) (MIT) | Gratis |
| LLM Primary | [Google Gemini](https://ai.google.dev/) | Free tier |
| LLM Fallback | [Groq](https://console.groq.com/) | Free tier |
| LLM Local | [Ollama](https://ollama.com/) (optional) | Gratis |
| UI | [Streamlit](https://streamlit.io/) | Gratis |
| Animation | [Lottie](https://lottiefiles.com/) + streamlit-lottie | Gratis |

## 📁 Struktur Project

```
ai-agent-personal/
├── CLAUDE.md                      # Konteks project (untuk Claude Code)
├── README.md                      # Dokumentasi ini
├── requirements.txt               # Python dependencies
├── .env.example                   # Template API key
├── main.py                        # Entry point (CLI)
│
├── core/
│   ├── config.py                  # Konfigurasi & path
│   ├── llm_client.py              # LLM wrapper (Gemini + Groq)
│   └── orchestrator.py            # Router command → agent
│
├── agents/
│   ├── agent1_social_research.py  # 🔍 Rimba
│   ├── agent2_content_plan.py     # ✍️ Karya
│   ├── agent3_reports.py          # 📊 Lensa
│   ├── agent4_marketing_plan.py   # 📋 Stratego
│   ├── agent5_marketing_strategy.py # 🧭 Navi
│   └── agent6_ads_research.py     # 💰 Hemat
│
├── ui/
│   ├── app.py                     # Streamlit UI
│   └── animations/                # File animasi Lottie
│
└── data/
    ├── inputs/                    # Input mentah
    ├── outputs/                   # Output agent
    └── reports/                   # Report mingguan/bulanan
```

## 🎨 Animasi Kartun

UI menggunakan animasi Lottie untuk menampilkan:
- 🤖 Agent "thinking" saat menerima perintah
- ⚙️ Agent "working" dengan animasi kartun kerja
- ✅ Agent "done" saat selesai
- 🎉 Success animation saat task complete

## 🔑 API Key Gratis - Detail Limit

### Google Gemini (Recommended)
- 15 requests/minute
- 1,500 requests/day
- 1 million tokens/minute
- Cocok untuk: hampir semua use case

### Groq
- 30 requests/minute
- 14,400 requests/day
- Inference super cepat (Llama 3.3 70B)
- Cocok untuk: response cepat

## ⚠️ Catatan Penting

1. **Social Media Research**: Untuk riset Instagram/TikTok, agent akan menggunakan pengetahuan AI + analisis kamu. Scrape otomatis berisiko melanggar ToS platform.

2. **API Key**: Jaga kerahasiaan API key kamu. Jangan commit `.env` ke git.

3. **Output**: Semua output disimpan di `data/outputs/` dengan timestamp.

4. **Multi-language**: Default Bahasa Indonesia, bisa diubah di `.env` (`APP_LANGUAGE=id`).

## 🤝 Lanjutkan Project

Untuk melanjutkan development, ketik di Claude Code:
```
/lanjutkan-project-ai-agent-personal
```

## 📚 GitHub Repos sebagai Referensi

- [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) - Multi-agent framework
- [microsoft/autogen](https://github.com/microsoft/autogen) - Alternatif multi-agent
- [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) - LangChain agentic
- [BerriAI/litellm](https://github.com/BerriAI/litellm) - LLM router
- [streamlit/streamlit](https://github.com/streamlit/streamlit) - UI framework
- [andfanilo/streamlit-lottie](https://github.com/andfanilo/streamlit-lottie) - Lottie untuk Streamlit
- [ollama/ollama](https://github.com/ollama/ollama) - Local LLM

## 📝 License

MIT - bebas dipakai untuk personal & commercial.