#!/usr/bin/env python3
"""
Auto-push AI Agent Personal ke GitHub.
Tinggal kasih username GitHub & Personal Access Token, semuanya jalan otomatis.

Usage:
    venv/bin/python3 push_now.py

Atau kalau sudah ada di Terminal:
    bash /Users/user/ai-agent-personal/push_now.py
"""
import os
import sys
import subprocess
import getpass

REPO_PATH = "/Users/user/ai-agent-personal"
GITHUB_USERNAME = "tebakdaleman-jpg"
# Repo name got auto-renamed to use capitals
REPO_NAME = "AI-Agent-Personal"
REPO_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

def run(cmd, **kwargs):
    """Run shell command, print output."""
    print(f"\n>>> {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
    result = subprocess.run(cmd, shell=isinstance(cmd, str), **kwargs)
    return result.returncode == 0

def main():
    os.chdir(REPO_PATH)

    print("=" * 60)
    print("  🚀 AUTO-PUSH AI AGENT PERSONAL KE GITHUB")
    print("=" * 60)
    print()
    print(f"GitHub User: {GITHUB_USERNAME}")
    print(f"Repo URL:    {REPO_URL}")
    print()

    # 1. Cek repo GitHub exists
    print("[1/7] Cek repo GitHub...")
    test = subprocess.run(
        ["git", "ls-remote", REPO_URL],
        capture_output=True, text=True, timeout=10,
    )
    if test.returncode != 0:
        print(f"❌ Repo gak bisa di-akses: {test.stderr[:200]}")
        print()
        print("Pastikan kamu sudah buat repo di:")
        print(f"  https://github.com/new")
        print(f"  - Name: ai-agent-personal")
        print(f"  - Public")
        print(f"  - JANGAN centang README/gitignore/license")
        print()
        sys.exit(1)
    print("  ✓ Repo accessible")

    # 2. Init git (kalau belum)
    print("\n[2/7] Init git (kalau belum)...")
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"])
        print("  ✓ Initialized")
    else:
        print("  ✓ Already initialized")

    # 3. Setup git config
    print("\n[3/7] Setup git config...")
    subprocess.run(["git", "config", "user.name", GITHUB_USERNAME])
    subprocess.run(["git", "config", "user.email", f"{GITHUB_USERNAME}@users.noreply.github.com"])
    print("  ✓ Done")

    # 4. Add files
    print("\n[4/7] Add files...")
    subprocess.run(["git", "add", "."])
    status = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)

    # Sanity check - hanya .env (exact) atau folder venv/__pycache__
    # JANGAN match .env.example (itu template, boleh di-commit)
    bad_files = []
    for line in status.stdout.split("\n"):
        if not line.strip():
            continue
        parts = line.split()
        filename = parts[-1] if parts else ""
        # Hanya block file .env persis (bukan .env.example)
        if filename == ".env" or filename.startswith("venv/") or "/venv/" in filename or filename.startswith("__pycache__/") or "/__pycache__/" in filename:
            bad_files.append(filename)

    if bad_files:
        print(f"❌ Ada file sensitif: {bad_files[:3]}")
        print("  Update .gitignore dulu")
        sys.exit(1)
    print(f"  ✓ {len([l for l in status.stdout.splitlines() if l.strip()])} files staged")

    # 5. Commit
    print("\n[5/7] Commit...")
    subprocess.run(["git", "commit", "-m", "Deploy AI Agent Personal"], capture_output=True)
    print("  ✓ Done")

    # 6. Set remote
    print("\n[6/7] Set remote...")
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", REPO_URL])
    subprocess.run(["git", "branch", "-M", "main"])
    print("  ✓ Done")

    # 7. Push - minta PAT (via CLI arg, env, file, atau prompt)
    print("\n[7/7] Push ke GitHub...")
    print()

    # Check sources in order: CLI arg > env > file > prompt
    pat = ""
    if len(sys.argv) > 1:
        pat = sys.argv[1].strip()
        print(f"  Token dari command-line arg (len={len(pat)})")
    if not pat:
        pat = os.environ.get("GH_TOKEN", "").strip()
        if pat:
            print(f"  Token dari env var (len={len(pat)})")
    if not pat and os.path.exists("/tmp/gh_token.tmp"):
        pat = open("/tmp/gh_token.tmp").read().strip()
        if pat:
            print(f"  Token dari file (len={len(pat)})")

    if not pat:
        print("=" * 60)
        print("  ⚠️  PERSONAL ACCESS TOKEN DIPERLUKAN!")
        print("=" * 60)
        print()
        print("Belum punya? Buat di:")
        print("  1. https://github.com/settings/tokens")
        print("  2. Klik 'Generate new token' → 'classic'")
        print("  3. Note: 'AI Agent Personal Deploy'")
        print("  4. Expiration: 30 days (atau lebih)")
        print("  5. Scopes: centang 'repo'")
        print("  6. Klik 'Generate token'")
        print("  7. COPY TOKEN (muncul sekali!)")
        print()
        print("Cara pakai:")
        print("  python3 push_now.py <TOKEN>")
        print("  atau set env: GH_TOKEN=<TOKEN> python3 push_now.py")
        print()
        print("=" * 60)
        print()

        pat = getpass.getpass("Paste Personal Access Token kamu (input hidden): ").strip()
        if not pat:
            print("❌ Token kosong. Batal.")
            sys.exit(1)

    # Build authenticated URL
    auth_url = REPO_URL.replace("https://", f"https://{GITHUB_USERNAME}:{pat}@")

    print()
    print("Pushing...")
    result = subprocess.run(
        ["git", "push", "-u", auth_url, "main"],
        capture_output=True, text=True, timeout=120,
    )

    # If rejected (remote has commits we don't), try force push
    if result.returncode != 0 and ("fetch first" in result.stderr or "rejected" in result.stderr or "non-fast-forward" in result.stderr):
        print("⚠️  Remote punya commits yang gak ada di local. Force push...")
        result = subprocess.run(
            ["git", "push", "-f", "-u", auth_url, "main"],
            capture_output=True, text=True, timeout=120,
        )

    if result.returncode == 0:
        print()
        print("=" * 60)
        print("  ✅ PUSH BERHASIL!")
        print("=" * 60)
        print()
        print(f"Repo: https://github.com/{GITHUB_USERNAME}/ai-agent-personal")
        print()
        print("🎯 NEXT: Deploy ke Streamlit Cloud")
        print()
        print("1. Buka https://share.streamlit.io/")
        print("2. Sign in dengan GitHub")
        print("3. Klik 'New app'")
        print("4. Isi:")
        print(f"   - Repository: {GITHUB_USERNAME}/ai-agent-personal")
        print("   - Branch: main")
        print("   - Main file path: ui/app.py")
        print("5. Klik 'Deploy!' (tunggu 3-5 menit)")
        print("6. Setelah deploy, klik ⚙️ Settings → Secrets")
        print("7. Paste:")
        print()
        print('   GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE"')
        print("   GEMINI_MODEL = \"gemini-flash-lite-latest\"")
        print()
        print("8. Save → auto-restart")
        print()
        print(f"🌐 URL FINAL: https://{GITHUB_USERNAME}-ai-agent-personal.streamlit.app")
        print()
        print("URL ini PERMANEN, 24/7 online, gak perlu terminal!")
    else:
        print()
        print("❌ Push gagal:")
        print(result.stderr[:500])
        print()
        print("Troubleshooting:")
        print("- Pastikan Personal Access Token benar")
        print("- Pastikan PAT punya scope 'repo'")
        print("- Pastikan repo public dan kosong")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Dibatalkan")
        sys.exit(1)