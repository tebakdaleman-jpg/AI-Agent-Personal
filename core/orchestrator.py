"""Orchestrator - route command ke agent yang sesuai."""
from core.llm_client import get_llm
from core import memory
from agents import (
    agent1_social_research,
    agent2_content_plan,
    agent3_reports,
    agent4_marketing_plan,
    agent5_marketing_strategy,
    agent6_ads_research,
)


# Keyword mapping untuk routing cepat
KEYWORD_MAP = {
    "agent1": [
        "riset", "research", "analisis", "instagram", "tiktok", "niche",
        "cari konten", "tren", "kompetitor",
    ],
    "agent2": [
        "content plan", "konten plan", "content calendar", "kalender konten",
        "planning konten", "rencana konten", "ide konten", "script viral",
        "1 bulan", "30 hari", "postingan", "scheduling",
    ],
    "agent3": [
        "report", "laporan", "analytics", "analitik", "mingguan", "bulanan",
        "performa", "statistik",
    ],
    "agent4": [
        "marketing plan", "plan marketing", "rencana marketing",
        "activity", "kegiatan", "offline", "online",
    ],
    "agent5": [
        "strategi", "strategy", "positioning", "persona",
        "brand strategy", "kompetitor",
    ],
    "agent6": [
        "ads", "iklan", "meta ads", "facebook ads", "tiktok ads",
        "google ads", "budget", "roas", "cpm", "cpc",
    ],
}


def classify_command(command: str) -> str:
    """Detect agent yang paling relevan dari command.

    Returns: 'agent1' | 'agent2' | ... | 'unknown'

    Scoring: longer/multi-word keywords di-prioritaskan (lebih spesifik).
    """
    cmd_lower = command.lower()
    scores = {}

    for agent_id, keywords in KEYWORD_MAP.items():
        score = 0
        for kw in keywords:
            if kw in cmd_lower:
                # Longer keyword = lebih spesifik = skor lebih tinggi
                score += len(kw.split())
        scores[agent_id] = score

    # Ambil yang score-nya paling tinggi
    best_agent = max(scores, key=scores.get)
    if scores[best_agent] == 0:
        return "unknown"
    return best_agent


def route(command: str) -> dict:
    """Route command ke agent yang sesuai.

    Returns dict: {agent, status, output | error}
    """
    agent_id = classify_command(command)
    if agent_id == "unknown":
        return {
            "agent": None,
            "status": "error",
            "error": "Tidak bisa mendeteksi agent yang dituju. Coba sebut kata kunci seperti: riset, content plan, report, marketing plan, strategi, atau ads.",
        }

    agents_funcs = {
        "agent1": ("Rimba (Social Researcher)", agent1_social_research.run),
        "agent2": ("Karya (Content Planner)", agent2_content_plan.run),
        "agent3": ("Lensa (Reporter)", agent3_reports.run),
        "agent4": ("Stratego (Marketing Planner)", agent4_marketing_plan.run),
        "agent5": ("Navi (Strategist)", agent5_marketing_strategy.run),
        "agent6": ("Hemat (Ads Researcher)", agent6_ads_research.run),
    }

    name, func = agents_funcs[agent_id]

    # Extract parameter dari command (sederhana - first arg after command)
    # User bisa ngomong: "riset instagram @namaakun"
    parts = command.split(maxsplit=1)
    arg = parts[1] if len(parts) > 1 else ""

    try:
        # Pass ke agent function dengan argumen yang sesuai
        if agent_id == "agent1":
            output = func(arg or "@general", "instagram")
        elif agent_id == "agent2":
            output = func(arg or "general niche")
        elif agent_id == "agent3":
            output = func("weekly", arg)
        elif agent_id == "agent4":
            output = func(arg or "general business")
        elif agent_id == "agent5":
            output = func(arg or "general business")
        elif agent_id == "agent6":
            output = func(arg or "general business")

        # Auto-save ke memory (dengan excerpt output 500 char pertama)
        memory.remember(
            agent_id=agent_id,
            command=command,
            output_excerpt=output[:500],
        )

        return {
            "agent": name,
            "agent_id": agent_id,
            "status": "success",
            "output": output,
            "memory_id": f"mem_{len(memory.get_recent(100))}",
        }
    except Exception as e:
        return {
            "agent": name,
            "agent_id": agent_id,
            "status": "error",
            "error": str(e),
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m core.orchestrator <command>")
        print("\nContoh:")
        print('  python -m core.orchestrator "riset instagram @namaakun"')
        print('  python -m core.orchestrator "buat content plan bisnis"')
        print('  python -m core.orchestrator "report mingguan"')
        sys.exit(1)

    cmd = " ".join(sys.argv[1:])
    result = route(cmd)
    print(f"\n{'='*60}")
    print(f"Agent: {result.get('agent', 'Unknown')}")
    print(f"Status: {result.get('status')}")
    print(f"{'='*60}\n")

    if result["status"] == "success":
        print(result["output"])
    else:
        print(f"Error: {result.get('error')}")