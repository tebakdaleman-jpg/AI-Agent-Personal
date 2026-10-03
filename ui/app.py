"""Streamlit UI untuk AI Agent Personal - dengan animasi kartun."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import requests
from streamlit_lottie import st_lottie
from core.config import AGENTS
from core.orchestrator import route, classify_command
from core import memory, export_to_pdf
import time


# ===== Page Config =====
st.set_page_config(
    page_title="AI Agent Personal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ===== Custom CSS untuk tema kartun =====
CUSTOM_CSS = """
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .agent-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        transition: transform 0.2s;
        border: 2px solid transparent;
        height: 280px;
    }

    .agent-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }

    .agent-card.working {
        border-color: #4ECDC4;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(78, 205, 196, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(78, 205, 196, 0); }
        100% { box-shadow: 0 0 0 0 rgba(78, 205, 196, 0); }
    }

    .agent-emoji {
        font-size: 48px;
        margin-bottom: 8px;
    }

    .agent-name {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 4px;
    }

    .agent-role {
        font-size: 13px;
        color: #666;
    }

    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
        margin-top: 8px;
    }

    .status-idle { background: #e0e0e0; color: #666; }
    .status-working { background: #FFE66D; color: #333; }
    .status-done { background: #95E1D3; color: #333; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ===== Lottie Animation Loader =====
@st.cache_data
def load_lottie_url(url: str):
    """Load animasi Lottie dari URL (cached)."""
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


# Animasi default (pakai built-in fallback jika gagal)
FALLBACK_ANIMATION = {
    "v": "5.5.7",
    "fr": 30,
    "ip": 0,
    "op": 60,
    "w": 200,
    "h": 200,
    "nm": "loading",
    "ddd": 0,
    "assets": [],
    "layers": [
        {
            "ddd": 0, "ind": 1, "ty": 4, "nm": "circle",
            "sr": 1, "ks": {
                "o": {"a": 0, "k": 100},
                "r": {"a": 1, "k": [{"i": {"x": [0.5], "y": [1]}, "o": {"x": [0.5], "y": [0]}, "t": 0, "s": [0]}, {"t": 60, "s": [360]}]},
                "p": {"a": 0, "k": [100, 100, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            },
            "ao": 0,
            "shapes": [{
                "ty": "el", "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [60, 60]},
                "nm": "Ellipse"
            }, {
                "ty": "st", "c": {"a": 0, "k": [0.3, 0.8, 0.7, 1]}, "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": 6}, "lc": 2, "lj": 2, "ml": 4, "nm": "Stroke"
            }],
            "ip": 0, "op": 60, "st": 0, "bm": 0
        }
    ]
}


def get_animation(animation_name: str):
    """Get Lottie animation dengan fallback."""
    urls = {
        "thinking": "https://lottie.host/4f3e8e6e-2c8e-4f5e-9c5e-8e6e2c8e4f5e/9XKgKw7IhQ.json",
        "working": "https://assets3.lottiefiles.com/packages/lf20_x62chJ.json",
        "complete": "https://assets1.lottiefiles.com/packages/lf20_s2yranru.json",
        "robot_thinking": "https://assets10.lottiefiles.com/packages/lf20_VbrWqV.json",
        "team": "https://assets1.lottiefiles.com/packages/lf20_yzoqyyqf.json",
    }
    url = urls.get(animation_name, "")
    if url:
        anim = load_lottie_url(url)
        if anim:
            return anim
    return FALLBACK_ANIMATION


# ===== Header =====
col_logo, col_text = st.columns([1, 5])
with col_logo:
    try:
        st_lottie(get_animation("robot_thinking"), height=120, key="header_anim")
    except Exception:
        st.markdown("<div style='font-size:80px; text-align:center'>🤖</div>", unsafe_allow_html=True)
with col_text:
    st.title("🤖 AI Agent Personal")
    st.markdown("**6 AI Agents siap membantu pekerjaan kamu** — ketik perintah di sidebar atau klik agent di bawah.")


# ===== Sidebar - Command Input =====
with st.sidebar:
    st.header("🎯 Command Center")

    command = st.text_area(
        "Perintah kamu:",
        placeholder="Contoh: riset instagram @namaakun\nbuat content plan untuk niche parenting\nreport mingguan",
        height=120,
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        run_btn = st.button("🚀 Jalankan", use_container_width=True, type="primary")
    with col_btn2:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)

    st.divider()
    st.markdown("### 💡 Contoh Perintah")
    examples = [
        "riset instagram @brand",
        "buat content plan parenting",
        "report mingguan",
        "marketing plan F&B",
        "strategi marketing",
        "riset ads budget 3jt",
    ]
    for ex in examples:
        if st.button(f"→ {ex}", key=f"ex_{ex}", use_container_width=True):
            st.session_state.command = ex
            st.rerun()

    st.divider()
    with st.expander("ℹ️ Setup API Key"):
        st.markdown("""
        1. Daftar gratis di [aistudio.google.com](https://aistudio.google.com/apikey)
        2. Copy `.env.example` ke `.env`
        3. Isi `GOOGLE_API_KEY`
        4. Restart app
        """)


# ===== Agent Cards =====
st.markdown("### 👥 Tim Agent Kamu")

# Inisialisasi state untuk track status agent
if "agent_status" not in st.session_state:
    st.session_state.agent_status = {aid: "idle" for aid in AGENTS.keys()}
if "last_output" not in st.session_state:
    st.session_state.last_output = None
if "command" not in st.session_state:
    st.session_state.command = ""


# Override command from button click
if hasattr(st.session_state, 'command') and st.session_state.command:
    command = st.session_state.command


# Tampilkan 6 agent cards dalam grid 3x2
for row in range(2):
    cols = st.columns(3)
    for col_idx in range(3):
        agent_idx = row * 3 + col_idx
        agent_id = list(AGENTS.keys())[agent_idx]
        info = AGENTS[agent_id]
        status = st.session_state.agent_status.get(agent_id, "idle")

        with cols[col_idx]:
                status_class = {
                    "idle": "status-idle",
                    "working": "status-working",
                    "done": "status-done",
                }[status]

                status_label = {
                    "idle": "💤 Idle",
                    "working": "⚙️ Working",
                    "done": "✅ Done",
                }[status]

                # Animasi working
                working_anim = ""
                if status == "working":
                    working_anim = f"""
                    <div style='margin-bottom:8px'>
                    </div>
                    """

                st.markdown(f"""
                <div class="agent-card {('working' if status == 'working' else '')}">
                    <div class="agent-emoji">{info['emoji']}</div>
                    <div class="agent-name">{info['name']}</div>
                    <div class="agent-role">{info['role']}</div>
                    <div class="status-badge {status_class}">{status_label}</div>
                </div>
                """, unsafe_allow_html=True)

                # Tampilkan animasi Lottie di bawah card jika working
                if status == "working":
                    try:
                        st_lottie(get_animation("working"), height=80, key=f"anim_{agent_id}", speed=1.5)
                    except Exception:
                        pass


# ===== Eksekusi command =====
if run_btn and command:
    # Detect agent
    agent_id = classify_command(command)

    # Set semua ke idle, yang aktif jadi working
    for aid in AGENTS.keys():
        st.session_state.agent_status[aid] = "idle"
    if agent_id in AGENTS:
        st.session_state.agent_status[agent_id] = "working"

    # Tampilkan animasi working sebentar
    if agent_id in AGENTS:
        with st.spinner(f"{AGENTS[agent_id]['emoji']} {AGENTS[agent_id]['name']} sedang bekerja..."):
            result = route(command)
            st.session_state.last_output = result
            st.session_state.agent_status[agent_id] = "done"

    st.rerun()

elif run_btn and not command:
    st.warning("⚠️ Masukkan perintah dulu di sidebar!")


# ===== Tampilkan output =====
if st.session_state.last_output:
    st.divider()
    st.markdown("### 📋 Output Agent")

    result = st.session_state.last_output

    if result.get("status") == "success":
        agent_id = result.get("agent_id")
        if agent_id:
            info = AGENTS.get(agent_id, {})
            st.success(f"✅ **{info.get('name', 'Agent')}** selesai!")

        with st.expander("📄 Lihat output lengkap", expanded=True):
            st.markdown(result.get("output", ""))

        # PDF download button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            try:
                with st.spinner("Generating PDF..."):
                    pdf_path = export_to_pdf(
                        result.get("output", ""),
                        title=f"Agent Report - {result.get('agent', 'Unknown')}"
                    )
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download PDF",
                        data=f.read(),
                        file_name=pdf_path.name,
                        mime="application/pdf",
                        use_container_width=True,
                    )
            except Exception as e:
                st.error(f"PDF error: {e}")
        with col2:
            st.download_button(
                label="📄 Download MD",
                data=result.get("output", "").encode("utf-8"),
                file_name=f"agent_output_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True,
            )
    else:
        st.error(f"❌ {result.get('error', 'Unknown error')}")


# ===== Memory Sidebar Section =====
with st.sidebar:
    st.divider()
    with st.expander("🧠 Memory & Context"):
        stats = memory.stats()
        st.metric("Total Interaksi", stats["total_interactions"])
        if stats["by_agent"]:
            st.markdown("**Per agent:**")
            for aid, count in stats["by_agent"].items():
                info = AGENTS.get(aid, {})
                st.markdown(f"  {info.get('emoji', '?')} {info.get('name', aid)[:20]}: {count}")

        recent = memory.get_recent(5)
        if recent:
            st.markdown("**5 Terakhir:**")
            for entry in reversed(recent):
                info = AGENTS.get(entry["agent"], {})
                st.caption(f"{info.get('emoji', '?')} {entry['command'][:50]}")

        if st.button("🗑️ Clear Memory", use_container_width=True):
            memory.clear()
            st.rerun()

    with st.expander("⚙️ Set Business Context"):
        st.caption("Set sekali, agent akan pakai untuk context")
        biz_name = st.text_input("Nama bisnis/brand", value=memory.get_context("business_name") or "")
        biz_niche = st.text_input("Niche", value=memory.get_context("business_niche") or "")
        biz_target = st.text_input("Target market", value=memory.get_context("target_market") or "")
        if st.button("💾 Save Context"):
            if biz_name: memory.set_context("business_name", biz_name)
            if biz_niche: memory.set_context("business_niche", biz_niche)
            if biz_target: memory.set_context("target_market", biz_target)
            st.success("Context saved!")


# ===== Footer =====
st.divider()
st.markdown("""
<div style='text-align:center; color:#888; font-size:12px'>
🤖 AI Agent Personal — 6 Agents siap membantu • Dibuat dengan ❤️ menggunakan free tools<br>
Powered by Google Gemini (free) + Streamlit + Lottie animations
</div>
""", unsafe_allow_html=True)