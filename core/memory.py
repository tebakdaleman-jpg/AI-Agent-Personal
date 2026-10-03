"""Memory module - simpan konteks & history agent ke JSON file."""
import json
from datetime import datetime
from pathlib import Path
from .config import DATA_DIR


MEMORY_FILE = DATA_DIR / "memory.json"


def _load() -> dict:
    """Load memory dari file (atau buat baru)."""
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {"history": [], "context": {}}
    return {"history": [], "context": {}}


def _save(data: dict):
    """Simpan memory ke file."""
    MEMORY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def remember(agent_id: str, command: str, output_excerpt: str = "") -> str:
    """Simpan interaksi agent ke memory.

    Returns: memory_id untuk referensi nanti.
    """
    data = _load()
    memory_id = f"mem_{len(data['history']) + 1:04d}_{datetime.now().strftime('%H%M%S')}"
    entry = {
        "id": memory_id,
        "agent": agent_id,
        "command": command[:300],
        "output_excerpt": output_excerpt[:500],
        "timestamp": datetime.now().isoformat(),
    }
    data["history"].append(entry)

    # Simpan max 100 entries terakhir
    if len(data["history"]) > 100:
        data["history"] = data["history"][-100:]

    _save(data)
    return memory_id


def get_recent(n: int = 5) -> list:
    """Ambil N interaksi terakhir."""
    data = _load()
    return data["history"][-n:]


def get_context_for_agent(agent_id: str) -> str:
    """Ambil konteks dari interaksi sebelumnya yang relevan.

    Returns string yang bisa di-include di prompt untuk context.
    """
    data = _load()
    recent = data["history"][-3:]  # 3 terakhir
    if not recent:
        return ""

    lines = ["Konteks dari interaksi sebelumnya:"]
    for entry in recent:
        lines.append(f"- [{entry['agent']}] {entry['command'][:150]}")
        if entry.get("output_excerpt"):
            lines.append(f"  Ringkasan: {entry['output_excerpt'][:200]}...")

    return "\n".join(lines)


def set_context(key: str, value: str):
    """Simpan key-value context (misal: business info, brand name, dll)."""
    data = _load()
    data["context"][key] = {
        "value": value,
        "updated": datetime.now().isoformat(),
    }
    _save(data)


def get_context(key: str) -> str:
    """Ambil context value."""
    data = _load()
    ctx = data.get("context", {}).get(key, {})
    return ctx.get("value", "") if isinstance(ctx, dict) else ""


def get_all_context() -> dict:
    """Ambil semua context (untuk prompt)."""
    data = _load()
    return {k: v.get("value", "") if isinstance(v, dict) else v for k, v in data.get("context", {}).items()}


def clear():
    """Hapus semua memory."""
    _save({"history": [], "context": {}})


def stats() -> dict:
    """Statistik memory."""
    data = _load()
    history = data.get("history", [])
    by_agent = {}
    for h in history:
        agent = h.get("agent", "unknown")
        by_agent[agent] = by_agent.get(agent, 0) + 1
    return {
        "total_interactions": len(history),
        "by_agent": by_agent,
        "context_keys": list(data.get("context", {}).keys()),
    }