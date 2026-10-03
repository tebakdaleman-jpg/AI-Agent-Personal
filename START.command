#!/bin/bash
# ===========================================
# AI AGENT PERSONAL - ONE CLICK START (v2)
# ===========================================
# Pakai serveo.net (SSH tunnel) — support WebSocket
# Gak perlu install apa-apa, SSH built-in di Mac

cd "$(dirname "$0")"

clear
echo "================================================"
echo "  AI AGENT PERSONAL - STARTING..."
echo "================================================"
echo ""

# 1. Cleanup proses lama
echo "[1/4] Membersihkan proses lama..."
pkill -f "streamlit run" 2>/dev/null
pkill -f "localtunnel" 2>/dev/null
pkill -f "ssh.*serveo" 2>/dev/null
sleep 2

# 2. Start streamlit
echo "[2/4] Starting Streamlit di localhost:8501..."
source venv/bin/activate
nohup streamlit run ui/app.py --server.headless true --server.port 8501 --server.address 0.0.0.0 > /tmp/streamlit.log 2>&1 &

# Tunggu streamlit ready
for i in {1..15}; do
  if curl -s -o /dev/null http://localhost:8501/_stcore/health 2>/dev/null; then
    echo "  ✓ Streamlit ready dalam ${i}s"
    break
  fi
  sleep 1
done

# 3. Cek streamlit running
if ! curl -s -o /dev/null http://localhost:8501/_stcore/health 2>/dev/null; then
  echo "  ❌ Streamlit gagal start. Cek /tmp/streamlit.log"
  exit 1
fi

# 4. Start serveo tunnel
echo ""
echo "[3/4] Starting SSH Tunnel (serveo.net)..."
echo ""
echo "================================================"
echo "  COPY URL YANG MUNCUL DI BAWAH!"
echo "  Biasanya: https://xxxxx.serveo.net"
echo "================================================"
echo ""
echo "  (Kalau pertama kali, ketik 'yes' untuk trust host key)"
echo ""

# SSH reverse tunnel ke serveo.net
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:localhost:8501 serveo.net

echo ""
echo "[4/4] Tunnel closed. Streamlit masih jalan."
echo "Untuk stop semuanya: pkill -f 'streamlit run' && pkill -f 'ssh.*serveo'"