# AI Agent Personal

Project untuk membangun **6 AI Agent Assistant** yang membantu aktivitas social media, content, marketing, dan ads management.

## 🎯 6 AI Agents

| ID | Nama | Emoji | Tugas |
|----|------|-------|-------|
| agent1 | Rimba | 🔍 | Riset Instagram & TikTok, analisis niche, cari konten relevan |
| agent2 | Karya | ✍️ | Content plan 1 bulan + script viral |
| agent3 | Lensa | 📊 | Report social media mingguan & bulanan |
| agent4 | Stratego | 📋 | Marketing plan 1 bulan (online + offline) |
| agent5 | Navi | 🧭 | Strategi marketing offline & IG/TikTok |
| agent6 | Hemat | 💰 | Riset Meta/TikTok/Google Ads + budget calculation |

## 🛠️ Tech Stack (100% Gratis)

- **Multi-agent**: CrewAI (MIT)
- **LLM Primary**: Google Gemini API (free tier)
- **LLM Fallback**: Groq API (free tier)
- **UI**: Streamlit + Lottie animations
- **Optional**: Ollama untuk local LLM

## 📁 Struktur Project

```
ai-agent-personal/
├── CLAUDE.md                      # Konteks project ini
├── README.md                      # Dokumentasi lengkap
├── requirements.txt               # Python dependencies
├── .env.example                   # Template API key
├── main.py                        # Entry point CLI
│
├── core/                          # Konfigurasi, LLM client, orchestrator
├── agents/                        # 6 agent implementation
├── ui/                            # Streamlit UI + animasi
└── data/                          # inputs/outputs/reports
```

## 🚀 Cara Jalankan

```bash
# 1. Install
pip install -r requirements.txt

# 2. Setup API key
cp .env.example .env
# Isi GOOGLE_API_KEY (gratis di https://aistudio.google.com/apikey)

# 3. Jalankan UI
streamlit run ui/app.py

# Atau CLI:
# python main.py
```

## 📊 Status & Progress

### 2026-10-03
- [x] Setup project structure
- [x] Setup dependencies (requirements.txt - ringan, requests only)
- [x] Setup config & LLM client wrapper (Gemini + Groq fallback via REST)
- [x] Implement Agent 1 (Rimba - Social Research)
- [x] Implement Agent 2 (Karya - Content Plan)
- [x] Implement Agent 3 (Lensa - Reports)
- [x] Implement Agent 4 (Stratego - Marketing Plan)
- [x] Implement Agent 5 (Navi - Marketing Strategy)
- [x] Implement Agent 6 (Hemat - Ads Research)
- [x] Build orchestrator dengan weighted scoring keyword routing
- [x] Build Streamlit UI dengan animasi kartun Lottie
- [x] Buat entry point (CLI + UI + run.sh)
- [x] README.md + dokumentasi lengkap
- [x] Setup API key Google Gemini (works dengan model `gemini-flash-lite-latest`)
- [x] Test Agent 1-6 end-to-end (semua 6 agent BERHASIL)
- [x] Fix bug routing (keyword weighting)
- [x] Fix bug timeout (180s + retry 3x)
- [x] **Tambah PDF export** (semua output agent bisa di-download PDF)
- [x] **Tambah Memory module** (auto-save history + business context)
- [x] **Tambah UI memory panel** + business context setting
- [ ] Improve prompt berdasarkan hasil testing
- [ ] Integrasi Ollama untuk local LLM
- [ ] Tambah lebih banyak animasi (3D character, dll)

## 🔑 Setup Info

- **API Key**: Sudah dikonfigurasi di `.env` (Gemini)
- **Model**: `gemini-flash-lite-latest` (stabil, free tier)
- **Virtual env**: `venv/` (Python 3.9)
- **Cara jalankan**:
  ```bash
  source venv/bin/activate
  streamlit run ui/app.py    # UI dengan animasi
  # atau
  python main.py             # CLI
  ```

## 🆕 Fitur Terbaru

- **PDF Export**: Semua output agent bisa di-download sebagai PDF siap-presentasi
- **Memory**: History semua interaksi agent tersimpan, bisa di-restore di sidebar UI
- **Business Context**: Set info bisnis sekali, agent pakai untuk context
- **Retry Logic**: Auto-retry 3x kalau Gemini overloaded/rate-limited
- **Routing Pintar**: Weighted keyword scoring (keyword panjang = lebih spesifik)

## 🔑 Setup API Key Gratis

1. Buka https://aistudio.google.com/apikey
2. Login → "Create API Key"
3. Copy key ke `.env` di `GOOGLE_API_KEY=...`
4. Restart app

Alternatif gratis lain:
- Groq: https://console.groq.com/keys (super cepat)
- HuggingFace: https://huggingface.co/settings/tokens

## 🎨 Fitur Animasi

UI Streamlit menampilkan:
- 6 card agent dengan emoji & warna unik
- Status badge (idle/working/done)
- Pulse animation saat agent bekerja
- Working Lottie animation
- Smooth transition

## 💡 Contoh Perintah

```
riset instagram @brandkamu
buat content plan untuk niche parenting 7 post/minggu
report mingguan [paste data]
marketing plan F&B budget 5jt
strategi marketing fashion
riset ads untuk skincare budget 3jt
```

## 🔗 Referensi GitHub

- [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) - Multi-agent framework
- [microsoft/autogen](https://github.com/microsoft/autogen)
- [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
- [streamlit/streamlit](https://github.com/streamlit/streamlit)
- [andfanilo/streamlit-lottie](https://github.com/andfanilo/streamlit-lottie)

## 📌 Catatan Penting

- **Social media research** mengandalkan analisis AI + data yang user sediakan. Scrape otomatis melanggar ToS Instagram/TikTok.
- Semua output agent disimpan otomatis di `data/outputs/` dengan timestamp.
- Default Bahasa Indonesia, bisa diubah di `.env`.

## 🛠️ Cara Lanjutkan

Ketik: **`/lanjutkan-project-ai-agent-personal`**

Atau manual: `cd /Users/user/ai-agent-personal && claude`