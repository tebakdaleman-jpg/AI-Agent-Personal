#!/usr/bin/env python3
"""Read token from file and push to GitHub. Token disimpan terpisah dari command."""
import os
import sys
import subprocess
from pathlib import Path

REPO_PATH = "/Users/user/ai-agent-personal"
TOKEN_FILE = "/tmp/gh_token.tmp"
GITHUB_USERNAME = "tebakdaleman-jpg"
REPO_URL = f"https://github.com/{GITHUB_USERNAME}/ai-agent-personal.git"


def main():
    os.chdir(REPO_PATH)

    # Get token from file or prompt
    pat = ""
    if Path(TOKEN_FILE).exists():
        pat = Path(TOKEN_FILE).read_text().strip()

    if not pat:
        print("ERROR: Token gak ada")
        sys.exit(1)

    # Init git
    if not Path(".git").exists():
        subprocess.run(["git", "init"])

    subprocess.run(["git", "config", "user.name", GITHUB_USERNAME])
    subprocess.run(["git", "config", "user.email", f"{GITHUB_USERNAME}@users.noreply.github.com"])

    # Add files
    subprocess.run(["git", "add", "."])

    # Sanity check
    status = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
    bad = [l for l in status.stdout.split("\n") if ".env" in l or "venv/" in l or "__pycache__" in l]
    if bad:
        print(f"BAD FILES: {bad[:3]}")
        sys.exit(1)

    # Commit
    subprocess.run(["git", "commit", "-m", "Deploy AI Agent Personal"], capture_output=True)

    # Set remote
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", REPO_URL])
    subprocess.run(["git", "branch", "-M", "main"])

    # Push with auth
    auth_url = REPO_URL.replace("https://", f"https://{GITHUB_USERNAME}:{pat}@")
    print("Pushing...")
    result = subprocess.run(
        ["git", "push", "-u", auth_url, "main"],
        capture_output=True, text=True, timeout=120,
    )

    if result.returncode == 0:
        print("=" * 60)
        print("PUSH BERHASIL!")
        print("=" * 60)
        print(f"Repo: https://github.com/{GITHUB_USERNAME}/ai-agent-personal")
        print()
        print("NEXT STEP:")
        print("1. Buka https://share.streamlit.io/")
        print("2. Sign in dengan GitHub")
        print("3. New app -> pilih repo tebakdaleman-jpg/ai-agent-personal")
        print("4. Main file: ui/app.py")
        print("5. Deploy!")
        print("6. Set Secrets di Settings:")
        print('   GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE"')
        print('   GEMINI_MODEL = "gemini-flash-lite-latest"')
        print()
        print(f"URL FINAL: https://{GITHUB_USERNAME}-ai-agent-personal.streamlit.app")
    else:
        print("PUSH GAGAL:")
        print(result.stderr[:500])

    # Cleanup token file
    try:
        Path(TOKEN_FILE).unlink()
    except Exception:
        pass


if __name__ == "__main__":
    main()