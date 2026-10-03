"""Main entry point untuk AI Agent Personal."""
import sys
import argparse
from core.orchestrator import route
from core.config import AGENTS


def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        🤖  AI  A G E N T   P E R S O N A L  🤖          ║
║                                                          ║
║  6 AI Agents siap membantu pekerjaan kamu!              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)
    print("Tim Agent kamu:\n")
    for agent_id, info in AGENTS.items():
        print(f"  {info['emoji']}  {info['name']}")
        print(f"     → {info['role']}\n")


def interactive():
    """Mode interaktif - ketik perintah."""
    print_banner()
    print("Ketik 'exit' untuk keluar, 'help' untuk bantuan.\n")

    while True:
        try:
            cmd = input("\n🎯 Perintah kamu: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nBye! 👋")
            break

        if not cmd:
            continue
        if cmd.lower() in ("exit", "quit", "keluar"):
            print("Bye! 👋")
            break
        if cmd.lower() in ("help", "bantuan", "?"):
            print("""
Contoh perintah:
  • riset instagram @namaakun
  • buat content plan untuk niche parenting
  • report mingguan + data performa
  • marketing plan untuk bisnis F&B budget 5 juta
  • strategi marketing untuk fashion
  • riset ads untuk bisnis skincare budget 3 juta

Atau langsung sebut agent:
  • agent1 - riset sosial media
  • agent2 - content plan
  • agent3 - report
  • agent4 - marketing plan
  • agent5 - strategi
  • agent6 - ads
""")
            continue
        if cmd.lower() in ("agents", "tim", "list"):
            for agent_id, info in AGENTS.items():
                print(f"  {info['emoji']}  [{agent_id}] {info['name']} - {info['role']}")
            continue

        print("\n⏳ Agent sedang bekerja...\n")
        result = route(cmd)

        if result["status"] == "success":
            print(f"✅ {result['agent']} selesai!\n")
            print("─" * 60)
            print(result["output"])
            print("─" * 60)
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")


def single_command(cmd: str):
    """Jalankan satu perintah langsung."""
    result = route(cmd)
    if result["status"] == "success":
        print(result["output"])
    else:
        print(f"Error: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Agent Personal")
    parser.add_argument("command", nargs="*", help="Perintah untuk agent")
    parser.add_argument("--ui", action="store_true", help="Jalankan UI Streamlit")

    args = parser.parse_args()

    if args.ui:
        import subprocess
        subprocess.run(["streamlit", "run", "ui/app.py"])
    elif args.command:
        single_command(" ".join(args.command))
    else:
        interactive()