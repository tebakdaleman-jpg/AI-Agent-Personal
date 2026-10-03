# 🚀 Deploy PERMANEN ke Streamlit Cloud (24/7 Online)

URL permanen yang **selalu bisa diakses kapanpun**, gak perlu terminal hidup, gak perlu tunnel.

**Final URL**: `https://[username]-ai-agent-personal.streamlit.app`

---

## 📋 Prerequisites (1 menit)

1. **Akun GitHub** (gratis) — https://github.com/signup
2. **Akun Streamlit Cloud** (gratis) — https://share.streamlit.io (sign in dengan GitHub)

---

## 🎯 STEP 1: Push Code ke GitHub

### 1a. Buat repo baru di GitHub
- Buka https://github.com/new
- Isi:
  - **Repository name**: `ai-agent-personal` (atau nama lain)
  - **Description**: `6 AI Agents untuk social media marketing`
  - **Pilih**: Public ✅
  - **JANGAN** centang "Add README" / "Add .gitignore" / "Add license"
- Klik **"Create repository"**

### 1b. Copy URL repo
Setelah dibuat, akan muncul URL seperti:
```
https://github.com/USERNAME/ai-agent-personal.git
```
**Copy URL itu!** (Ganti `USERNAME` dengan username GitHub kamu)

### 1c. Push dari Terminal

Saya sudah siapkan script otomatis. **Paste command ini** di Terminal:

```bash
cd /Users/user/ai-agent-personal && git init && git add . && git commit -m "Deploy AI Agent Personal" && git branch -M main && git remote add origin https://github.com/USERNAME/ai-agent-personal.git && git push -u origin main
```

**Ganti `USERNAME`** dengan username GitHub kamu!

Akan diminta **username & password** GitHub:
- Username: username GitHub kamu
- Password: **BUKAN password biasa**, tapi **Personal Access Token** (lihat Step 1d)

### 1d. Buat Personal Access Token (kalau perlu)

GitHub sekarang gak terima password biasa untuk push. Harus pakai **Personal Access Token (PAT)**:

1. Buka https://github.com/settings/tokens
2. Klik **"Generate new token"** → **"Generate new token (classic)"**
3. Isi:
   - **Note**: `AI Agent Personal Deploy`
   - **Expiration**: `30 days` (atau lebih lama)
   - **Scopes**: centang `repo` ✅
4. Klik **"Generate token"**
5. **COPY token-nya** (hanya muncul sekali!)
6. Paste sebagai password saat push

---

## 🎯 STEP 2: Deploy ke Streamlit Cloud

1. Buka **https://share.streamlit.io/**
2. Sign in dengan GitHub
3. Klik **"New app"**
4. Isi form:
   - **Repository**: `USERNAME/ai-agent-personal`
   - **Branch**: `main`
   - **Main file path**: `ui/app.py`
   - **App URL**: pilih subdomain unik (misal `ai-agent-personal-kamu`)
5. Klik **"Deploy!"**

Tunggu 2-5 menit untuk build & deploy pertama.

---

## 🎯 STEP 3: Set API Key (Secrets)

Setelah deploy selesai:

1. Klik **⚙️ Settings** (pojok kanan atas)
2. Pilih tab **"Secrets"**
3. Paste format TOML ini:

```toml
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
GEMINI_MODEL = "gemini-flash-lite-latest"
```

4. Klik **"Save"**
5. App auto-restart, ~1 menit, lalu jadi

---

## ✅ Selesai!

URL app kamu: **`https://USERNAME-ai-agent-personal.streamlit.app`**

**Bisa diakses:**
- ✅ Kapanpun (24/7)
- ✅ Dari mana saja (HP, laptop, komputer kantor)
- ✅ Tanpa buka terminal
- ✅ Gak perlu tunnel
- ✅ HTTPS otomatis
- ✅ **GRATIS selamanya** (Streamlit Community Cloud free tier unlimited public apps)

---

## 🔄 Update App Nanti

Kalau kamu edit code, push ke GitHub:
```bash
cd /Users/user/ai-agent-personal
git add .
git commit -m "Update description"
git push
```

App auto-restart dalam ~30 detik. **Gak perlu sentuh Streamlit Cloud sama sekali.**

---

## 🆘 Troubleshooting

### "Permission denied" saat push
- Pastikan pakai Personal Access Token, bukan password biasa
- Token harus punya scope `repo`

### "Repository not found"
- Cek URL repo benar (case-sensitive)
- Cek username GitHub benar

### "ModuleNotFoundError" di Streamlit Cloud
- Cek requirements.txt lengkap
- Streamlit Cloud install otomatis dari requirements.txt

### "API Key Error"
- Cek secrets format TOML benar (pakai tanda kutip)
- Cek API key masih valid di https://aistudio.google.com/apikey

---

## 💡 Mau Lebih Cepat Lagi?

Saya bisa buatkan script yang **otomatis** semua step di atas. Tinggal kasih tahu:
1. Username GitHub kamu
2. Personal Access Token (atau mau saya pandu bikin dulu)

Saya eksekusi semua push-nya. Tinggal tungguin Streamlit Cloud deploy ~5 menit. 🚀