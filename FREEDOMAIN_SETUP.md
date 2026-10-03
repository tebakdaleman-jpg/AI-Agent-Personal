# 🌐 Setup Domain GRATIS — DigitalPlatDev/FreeDomain

## Arsitektur yang Kita Butuhkan

```
[Browser Chrome]
       ↓ (https://aiagent.digitalplat.dev)
[Cloudflare Tunnel]  ← Gratis, support custom domain
       ↓
[Streamlit di localhost:8501]  ← Jalan di Mac kamu
```

**3 Komponen Gratis:**
1. **DigitalPlatDev/FreeDomain** → kasih subdomain `nama.digitalplat.dev`
2. **Cloudflare Tunnel** (`cloudflared`) → expose localhost ke internet
3. **Streamlit** → app-nya udah jadi

---

## 📋 Step-by-Step Setup

### Step 1: Install cloudflared (Cloudflare Tunnel)

```bash
# macOS (pakai brew, ATAU download langsung)
brew install cloudflared

# Atau tanpa brew:
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz | tar xz
sudo mv cloudflared /usr/local/bin/
```

Verifikasi:
```bash
cloudflared --version
```

### Step 2: Dapatkan Subdomain dari DigitalPlatDev/FreeDomain

**2a. Fork repo**
- Buka https://github.com/DigitalPlatDev/FreeDomain
- Klik tombol **"Fork"** (kanan atas)
- Pilih akun GitHub kamu

**2b. Tambah file subdomain kamu**

Di repo fork, klik **"Add file"** → **"Create new file"**, buat file di folder `tubes/` (atau folder lain yang tersedia - lihat README repo):

**Path file**: `tubes/aiagent.json` (atau path yang sesuai repo)

**Isi file** (contoh):
```json
{
  "description": "AI Agent Personal - 6 AI agents for social media marketing",
  "domain": "aiagent.digitalplat.dev",
  "owner": {
    "username": "username-github-kamu",
    "email": "email-github-kamu"
  },
  "records": [
    {
      "type": "CNAME",
      "host": "aiagent",
      "value": "your-tunnel.trycloudflare.com",
      "ttl": 3600
    }
  ]
}
```

**Catatan**:
- Format & folder bisa beda tergantung repo. **WAJIB baca README repo** untuk format yang benar.
- `value` di CNAME adalah URL Cloudflare Tunnel kamu (lihat Step 3)
- Bisa di-update nanti setelah dapat URL tunnel

**2c. Submit Pull Request**
- Klik **"Propose changes"** → **"Create Pull Request"**
- Tunggu di-review & di-merge (biasanya 1-7 hari)

### Step 3: Start Cloudflare Tunnel (Dapat URL)

Jalankan Streamlit + Tunnel:

```bash
cd /Users/user/ai-agent-personal
source venv/bin/activate
chmod +x deploy.sh

# Start streamlit
streamlit run ui/app.py &

# Tunggu 5 detik, lalu start tunnel
sleep 5
cloudflared tunnel --url http://localhost:8501
```

Outputnya seperti:
```
Your quick tunnel: https://random-words-here.trycloudflare.com
```

**Copy URL `trycloudflare.com` itu!** Itu yang dipakai sebagai CNAME value.

### Step 4: Update FreeDomain dengan URL Tunnel

Edit file JSON yang kamu submit (update CNAME value), lalu commit ke fork kamu. PR akan otomatis update.

### Step 5: Test

Tunggu sampai PR di-merge. Setelah merge:
- Buka `https://aiagent.digitalplat.dev` di Chrome
- Harusnya muncul Streamlit app kamu!

---

## 🚀 Script Otomatis

Saya sudah tambah command di `deploy.sh`:

```bash
cd /Users/user/ai-agent-personal
chmod +x deploy.sh

# Quick tunnel tanpa custom domain (instant):
./deploy.sh tunnel-bg

# Quick tunnel dengan custom domain (perlu setup FreeDomain dulu):
./deploy.sh custom-domain
```

---

## ⚠️ PENTING - Sebelum lanjut

Kamu perlu:
1. **Akun GitHub** (untuk fork FreeDomain)
2. **Cloudflare account** (opsional, kalau pakai Named Tunnel permanen)
4. **Streamlit app jalan** di `localhost:8501`

Kalau mau versi paling sederhana (tanpa FreeDomain, tanpa setup GitHub):
- Pakai `./deploy.sh tunnel-bg` langsung dapat `https://random.loca.lt` URL
- Instant, gak perlu setup apa-apa

---

## 🔄 Alternatif Lebih Simpel

Kalau ribet dengan FreeDomain, ada opsi lebih gampang:

| Opsi | URL | Setup | Permanen? |
|------|-----|-------|-----------|
| **localtunnel** | `random.loca.lt` | 1 menit | ❌ |
| **Cloudflare quick tunnel** | `random.trycloudflare.com` | 1 menit | ❌ |
| **Cloudflare tunnel + FreeDomain** | `nama.digitalplat.dev` | 30 menit | ✅ |
| **Streamlit Cloud** | `username-app.streamlit.app` | 30 menit | ✅ |
| **HuggingFace Spaces** | `username-app.hf.space` | 30 menit | ✅ |

**Rekomendasi:**
- Sekarang: pakai `localtunnel` atau `cloudflared quick` (instant)
- Nanti: setup FreeDomain atau Streamlit Cloud untuk permanen

---

## 📞 Troubleshooting

### "cloudflared: command not found"
Install via brew (lihat Step 1)

### "tunnel gagal start"
- Cek Streamlit jalan di port 8501
- Cek firewall macOS tidak block

### "domain tidak resolve"
- Tunggu sampai PR FreeDomain di-merge (bisa 1-7 hari)
- Cek CNAME value benar (URL trycloudflare.com)

### "PR FreeDomain ditolak"
- Pastikan format JSON benar (lihat README repo)
- Pastikan username GitHub valid
- Pastikan nama subdomain belum dipakai orang lain

---

## 📚 Resources

- [DigitalPlatDev/FreeDomain repo](https://github.com/DigitalPlatDev/FreeDomain) — baca README untuk format terbaru
- [Cloudflare Tunnel docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) — untuk advanced config
- [Streamlit Cloud](https://share.streamlit.io/) — alternatif permanent hosting