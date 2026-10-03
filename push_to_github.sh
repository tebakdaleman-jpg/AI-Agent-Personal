#!/bin/bash
# push_to_github.sh - Auto-push project ke GitHub untuk deploy permanen
# Usage:
#   ./push_to_github.sh
#
# Akan minta:
#   - Username GitHub
#   - Personal Access Token (bukan password)
#   - Nama repo (default: ai-agent-personal)

set -e

cd "$(dirname "$0")"

# Warna
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  Push ke GitHub untuk Deploy Permanen${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Validasi prerequisite
if [ ! -f requirements.txt ]; then
  echo -e "${RED}❌ File requirements.txt gak ada. Pastikan jalanin dari folder project.${NC}"
  exit 1
fi

if [ ! -f ui/app.py ]; then
  echo -e "${RED}❌ File ui/app.py gak ada. Pastikan jalanin dari folder project.${NC}"
  exit 1
fi

# Input
read -p "GitHub username kamu: " GH_USER
read -p "Nama repo (default: ai-agent-personal): " REPO_NAME
REPO_NAME=${REPO_NAME:-ai-agent-personal}

if [ -z "$GH_USER" ]; then
  echo -e "${RED}❌ Username gak boleh kosong${NC}"
  exit 1
fi

echo ""
echo -e "${YELLOW}Pastikan kamu sudah:${NC}"
echo -e "  1. Buat akun GitHub di https://github.com/signup (kalau belum)"
echo -e "  2. Buat Personal Access Token di https://github.com/settings/tokens"
echo -e "     - Note: 'AI Agent Personal Deploy'"
echo -e "     - Expiration: 30 days"
echo -e "     - Scopes: centang 'repo'"
echo -e "  3. SUDAH buat repo kosong di https://github.com/new (Public, JANGAN init README)"
echo ""
read -p "Udah siap semua? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Batal. Siapin dulu prerequisite di atas."
  exit 1
fi

echo ""
echo -e "${BLUE}[1/6] Initialize git...${NC}"
if [ -d .git ]; then
  echo "  .git sudah ada, skip"
else
  git init
  echo "  ✓ Done"
fi

echo ""
echo -e "${BLUE}[2/6] Set git config...${NC}"
git config user.name "$GH_USER"
git config user.email "$GH_USER@users.noreply.github.com"
echo "  ✓ user.name = $GH_USER"
echo "  ✓ user.email = $GH_USER@users.noreply.github.com"

echo ""
echo -e "${BLUE}[3/6] Add files (excluding .env, venv, etc.)...${NC}"
git add .
echo "  ✓ Files added"

# Show what will be committed
echo ""
echo "Files yang akan di-commit:"
git status --short | head -20
echo ""

# Sanity check - pastikan .env TIDAK masuk
if git status --short | grep -E "\.env$|venv/|__pycache__"; then
  echo -e "${RED}❌ Ada file sensitif (.env, venv) yang akan di-commit!${NC}"
  echo "  Hapus dulu atau update .gitignore"
  exit 1
fi

echo -e "${YELLOW}Penting: Cek list di atas. .env (API key) jangan sampai ada!${NC}"
read -p "Lanjut commit? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Batal."
  exit 1
fi

echo ""
echo -e "${BLUE}[4/6] Commit...${NC}"
git commit -m "Initial commit - AI Agent Personal"
echo "  ✓ Done"

echo ""
echo -e "${BLUE}[5/6] Set remote...${NC}"
REPO_URL="https://github.com/$GH_USER/$REPO_NAME.git"
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
echo "  ✓ Remote: $REPO_URL"

echo ""
echo -e "${BLUE}[6/6] Push ke GitHub...${NC}"
echo "Akan minta Personal Access Token sebagai password."
echo "(Bukan password GitHub biasa!)"
echo ""

# Push dengan credential helper temporary
git push -u origin main 2>&1 | head -20

if [ $? -eq 0 ]; then
  echo ""
  echo -e "${GREEN}================================================${NC}"
  echo -e "${GREEN}  ✓ PUSH BERHASIL!${NC}"
  echo -e "${GREEN}================================================${NC}"
  echo ""
  echo -e "${YELLOW}NEXT STEP: Deploy ke Streamlit Cloud${NC}"
  echo ""
  echo "1. Buka https://share.streamlit.io/"
  echo "2. Sign in dengan GitHub"
  echo "3. Klik 'New app'"
  echo "4. Isi:"
  echo "   - Repository: $GH_USER/$REPO_NAME"
  echo "   - Branch: main"
  echo "   - Main file: ui/app.py"
  echo "5. Klik 'Deploy!'"
  echo "6. Tunggu ~5 menit"
  echo "7. Set Secrets (API key) di Settings → Secrets"
  echo ""
  echo "URL akhir: https://$GH_USER-$REPO_NAME.streamlit.app"
  echo ""
else
  echo ""
  echo -e "${RED}❌ Push gagal. Cek error di atas.${NC}"
  echo ""
  echo "Troubleshooting umum:"
  echo "- Pastikan Personal Access Token benar (bukan password)"
  echo "- Pastikan PAT punya scope 'repo'"
  echo "- Pastikan repo public dan kosong (no README)"
  exit 1
fi