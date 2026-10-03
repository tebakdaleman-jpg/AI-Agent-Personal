#!/bin/bash
# deploy.sh - Deploy AI Agent Personal ke public URL
# Usage:
#   ./deploy.sh tunnel         # Instant public URL via localtunnel
#   ./deploy.sh cf-tunnel      # Instant via Cloudflare (trycloudflare.com)
#   ./deploy.sh custom-domain  # Setup dengan FreeDomain (nama.digitalplat.dev)
#   ./deploy.sh streamlit-bg   # Start streamlit di background
#   ./deploy.sh github         # Setup git & push ke GitHub
#   ./deploy.sh help           # Tampilkan bantuan

set -e

cd "$(dirname "$0")"

show_help() {
    cat << 'EOF'
================================================
🚀 AI AGENT PERSONAL - DEPLOY SCRIPT
================================================

Pilih salah satu:

  ./deploy.sh streamlit-bg  → Start streamlit di localhost:8501

  ./deploy.sh tunnel        → INSTANT public URL via localtunnel
                              URL: https://random.loca.lt
                              Permanen? TIDAK

  ./deploy.sh cf-tunnel     → INSTANT via Cloudflare
                              URL: https://random.trycloudflare.com
                              Bisa pakai custom domain (FreeDomain)!

  ./deploy.sh custom-domain → Lihat FREEDOMAIN_SETUP.md
                              Setup: aiagent.digitalplat.dev (permanen)

  ./deploy.sh github        → Push ke GitHub untuk deploy permanen
                              (Streamlit Cloud, HF Spaces, Render)

================================================
EOF
}

start_streamlit() {
    echo "🚀 Starting Streamlit..."
    pkill -f "streamlit run" 2>/dev/null || true
    sleep 2

    if [ ! -d venv ]; then
        echo "❌ venv belum ada. Jalankan: python3 -m venv venv && pip install -r requirements.txt"
        exit 1
    fi

    source venv/bin/activate
    nohup streamlit run ui/app.py --server.headless true --server.port 8501 --server.address 0.0.0.0 > /tmp/streamlit.log 2>&1 &
    sleep 5

    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8501/_stcore/health | grep -q "200"; then
        echo "✓ Streamlit running di http://localhost:8501"
        return 0
    else
        echo "⚠️  Streamlit mungkin gagal start. Cek log: tail -f /tmp/streamlit.log"
        return 1
    fi
}

deploy_tunnel() {
    echo "🚀 LocalTunnel"
    echo ""
    start_streamlit || exit 1
    echo ""
    echo "Starting tunnel..."
    echo "(URL akan muncul di bawah - itu public URL kamu!)"
    echo ""
    npx localtunnel --port 8501
}

deploy_cf_tunnel() {
    echo "🚀 Cloudflare Quick Tunnel"
    echo ""

    if ! command -v cloudflared &> /dev/null; then
        echo "❌ cloudflared belum terinstall."
        echo ""
        echo "Install via: brew install cloudflared"
        echo "Atau download: https://github.com/cloudflare/cloudflared/releases"
        exit 1
    fi

    start_streamlit || exit 1
    echo ""
    echo "Starting Cloudflare Tunnel..."
    echo "(URL trycloudflare.com akan muncul - itu public URL!)"
    echo ""
    cloudflared tunnel --url http://localhost:8501
}

deploy_custom_domain() {
    echo "🌐 Custom Domain via DigitalPlatDev/FreeDomain"
    echo ""
    echo "Ikuti panduan lengkap di:"
    echo "  cat FREEDOMAIN_SETUP.md"
    echo ""
    echo "Ringkasan:"
    echo "  1. Fork https://github.com/DigitalPlatDev/FreeDomain"
    echo "  2. Tambah file subdomain kamu (misal: tubes/aiagent.json)"
    echo "  3. Submit Pull Request"
    echo "  4. Setelah merge, dapat URL seperti: aiagent.digitalplat.dev"
    echo ""
    echo "Untuk host, kita pakai Cloudflare Tunnel:"
    echo ""
    deploy_cf_tunnel
}

deploy_github() {
    echo "📦 Setup Git & Push ke GitHub"
    echo ""

    if [ ! -d .git ]; then
        git init
        echo "✓ Git initialized"
    fi

    if [ -z "$(git config user.name)" ]; then
        read -p "GitHub username: " GH_USER
        git config user.name "$GH_USER"
        git config user.email "$GH_USER@users.noreply.github.com"
    fi

    git add .
    git status --short
    echo ""
    read -p "Commit semua file di atas? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git commit -m "Deploy AI Agent Personal"
    fi

    echo ""
    echo "=== NEXT STEPS ==="
    echo ""
    echo "1. Buat repo baru di https://github.com/new (jangan init README)"
    echo ""
    echo "2. Push:"
    echo "   git remote add origin https://github.com/USERNAME/ai-agent-personal.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "3. Deploy ke salah satu:"
    echo "   • Streamlit Cloud: https://share.streamlit.io/"
    echo "   • HuggingFace Spaces: https://huggingface.co/new-space"
    echo "   • Render: https://render.com/"
    echo ""
    echo "4. Set secrets di hosting (JANGAN push API key):"
    echo "   GOOGLE_API_KEY = ..."
    echo "   GEMINI_MODEL = gemini-flash-lite-latest"
}

case "${1:-help}" in
    streamlit-bg|streamlit)
        start_streamlit
        ;;
    tunnel)
        deploy_tunnel
        ;;
    cf-tunnel|cf)
        deploy_cf_tunnel
        ;;
    custom-domain|domain)
        deploy_custom_domain
        ;;
    github)
        deploy_github
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac