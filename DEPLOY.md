# 🚀 Panduan Deploy ke Public URL Gratis

Pilih salah satu dari 3 opsi ini (semua 100% GRATIS):

---

## 🏆 OPSI 1: Streamlit Community Cloud (RECOMMENDED)

**URL hasil:** `https://[username]-[repo].streamlit.app` (custom domain juga bisa)

**Kelebihan:**
- ✅ Paling mudah untuk Streamlit
- ✅ Auto-deploy dari GitHub (push → auto restart)
- ✅ Free tier: unlimited public apps, 1GB RAM
- ✅ Built-in secrets management untuk API key
- ✅ HTTPS otomatis
- ✅ Custom subdomain gratis

### Step-by-step:

**1. Buat GitHub Repo**
- Buka https://github.com/new
- Login dengan akun GitHub kamu
- Repository name: `ai-agent-personal` (atau nama lain)
- Set ke **Public**
- **JANGAN** centang "Add README" / "Add .gitignore" (kita sudah punya)
- Klik "Create repository"

**2. Push code ke GitHub**
```bash
cd /Users/user/ai-agent-personal

git init
git add .
git commit -m "Initial commit - AI Agent Personal"

# Ganti USERNAME dengan username GitHub kamu
git remote add origin https://github.com/USERNAME/ai-agent-personal.git
git branch -M main
git push -u origin main
```

**3. Deploy ke Streamlit Cloud**
- Buka https://share.streamlit.io/
- Klik "Sign in with GitHub"
- Klik "New app"
- Isi form:
  - **Repository**: `USERNAME/ai-agent-personal`
  - **Branch**: `main`
  - **Main file path**: `ui/app.py`
  - **App URL**: pilih subdomain (misal: `ai-agent.streamlit.app`)
- Klik "Deploy!"

**4. Set API Key (Secrets)**
- Di dashboard app, klik ⚙️ "Settings" → "Secrets"
- Paste format TOML:
  ```toml
  GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
  GEMINI_MODEL = "gemini-flash-lite-latest"
  ```
- Klik "Save" → app auto-restart dengan secrets loaded

**5. Akses App**
- URL: `https://USERNAME-ai-agent-personal.streamlit.app`
- Share ke siapa saja!

---

## 🥈 OPSI 2: HuggingFace Spaces

**URL hasil:** `https://huggingface.co/spaces/[username]/[space-name]`

**Kelebihan:**
- ✅ Unlimited free tier (CPU)
- ✅ Built-in git LFS
- ✅ Built-in secrets
- ✅ Domain `.hf.space` keren

### Step-by-step:

**1. Buat akun HuggingFace**
- https://huggingface.co/join

**3. Buat Space baru**
- https://huggingface.co/new-space
- Pilih **SDK: Streamlit**
- Visibility: **Public**
- Klik "Create Space"

**4. Upload code via git**
```bash
cd /Users/user/ai-agent-personal

git init
git remote add space https://huggingface.co/spaces/USERNAME/SPACE-NAME
git add .
git commit -m "Deploy AI Agent Personal"
git push space main
```

**5. Set Secrets**
- Di Space page → "Settings" → "Variables and secrets"
- Add:
  - `GOOGLE_API_KEY`: API key kamu
  - `GEMINI_MODEL`: `gemini-flash-lite-latest`

**6. Akses**
- URL: `https://huggingface.co/spaces/USERNAME/SPACE-NAME`

---

## 🥉 OPSI 3: Render.com

**URL hasil:** `https://[app-name].onrender.com`

### Step:

**1. Push ke GitHub** (sama seperti Opsi 1)

**2. Deploy ke Render**
- Buka https://render.com/ → Sign up dengan GitHub
- Klik "New" → "Web Service"
- Pilih repo `ai-agent-personal`
- Konfigurasi:
  - **Environment**: Python
  - **Build command**: `pip install -r requirements.txt`
  - **Start command**: `streamlit run ui/app.py --server.port $PORT --server.address 0.0.0.0`
  - **Instance type**: Free
- Klik "Create Web Service"

**3. Set Environment Variables**
- Di dashboard → "Environment" → "Add Environment Variable"
- `GOOGLE_API_KEY` = API key kamu
- `GEMINI_MODEL` = `gemini-flash-lite-latest`

---

## 🔒 Keamanan API Key

**JANGAN PERNAH** push API key ke GitHub!

Pastikan:
1. `.env` ada di `.gitignore` ✅ (sudah kita setup)
2. Pakai Streamlit Secrets / HuggingFace Secrets / Render Env Vars
3. Kalau gak sengaja ke-push, langsung regenerate API key

---

## 🆘 Troubleshooting

### App error setelah deploy?
1. Buka tab "Logs" di dashboard hosting
2. Biasanya karena:
   - `ModuleNotFoundError`: cek requirements.txt
   - API key error: cek secrets
   - Memory limit: optimasi kode

### Animasi gak muncul?
- Lottie URL butuh akses internet di server (hosting harus allow)
- Fallback animation sudah ada di code

### Cold start lambat?
- Streamlit Cloud free tier: cold start ~30 detik untuk app yang jarang diakses
- Solusi: buka app secara berkala, atau upgrade ke paid

---

## 💡 Rekomendasi

**Pakai Opsi 1 (Streamlit Cloud)** kalau:
- Mau paling gampang & cepat
- Butuh custom domain

**Pakai Opsi 2 (HuggingFace Spaces)** kalau:
- Udah punya akun HF
- Mau URL yang lebih "tech-y"

**Pakai Opsi 3 (Render)** kalau:
- Butuh kontrol lebih (Docker support, dll)

---

## ✅ Checklist Deploy

- [ ] GitHub repo dibuat (public)
- [ ] Code di-push (`.env` JANGAN di-push)
- [ ] Hosting setup (Streamlit Cloud / HF Spaces / Render)
- [ ] API key diset di Secrets (JANGAN hardcode)
- [ ] App jalan tanpa error
- [ ] Test 1 command untuk verifikasi LLM connected
- [ ] Share URL 🎉