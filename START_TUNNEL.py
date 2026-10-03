#!/usr/bin/env python3
"""Start streamlit + tunnel otomatis."""
import subprocess
import sys
import time
import os
import signal
import socket

os.chdir("/Users/user/ai-agent-personal")

def is_port_open(port):
    """Cek apakah port sudah dipakai."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("127.0.0.1", port))
    sock.close()
    return result == 0

def kill_existing():
    """Kill streamlit & tunnel yang masih jalan."""
    print("🧹 Membersihkan proses lama...")
    subprocess.run(["pkill", "-f", "streamlit run"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", "localtunnel"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", "cloudflared"], stderr=subprocess.DEVNULL)
    time.sleep(3)

def start_streamlit():
    """Start streamlit di background."""
    print("🚀 Starting Streamlit...")
    log = open("/tmp/streamlit.log", "w")
    proc = subprocess.Popen(
        ["./venv/bin/streamlit", "run", "ui/app.py",
         "--server.headless", "true",
         "--server.port", "8501",
         "--server.address", "0.0.0.0"],
        stdout=log,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid,
    )
    print(f"  PID: {proc.pid}")

    # Tunggu streamlit ready
    for i in range(20):
        time.sleep(1)
        if is_port_open(8501):
            print(f"  ✓ Ready dalam {i+1}s")
            return True
    print("  ⚠️  Belum ready setelah 20s, cek log: /tmp/streamlit.log")
    return False

def start_tunnel():
    """Start localtunnel."""
    print()
    print("🌐 Starting LocalTunnel...")
    print("=" * 60)
    print("COPY URL YANG MUNCUL DI BAWAH INI!")
    print("=" * 60)
    print()
    # Foreground, biar URL langsung muncul
    subprocess.run(["npx", "localtunnel", "--port", "8501"])

def main():
    kill_existing()
    if start_streamlit():
        start_tunnel()
    else:
        print("Streamlit gagal start. Cek log:")
        with open("/tmp/streamlit.log") as f:
            print(f.read())
        sys.exit(1)

if __name__ == "__main__":
    main()