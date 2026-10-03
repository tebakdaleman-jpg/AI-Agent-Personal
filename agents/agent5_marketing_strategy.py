"""
Agent 5: Navi - Marketing Strategist
Tugas: Strategi marketing offline + Instagram/TikTok
"""
from core.llm_client import get_llm
from core.config import OUTPUTS_DIR
from datetime import datetime


SYSTEM_PROMPT = """Kamu adalah Navi, AI Agent spesialis marketing strategy.

KEAHLIAN:
- Menyusun strategi marketing holistik (online + offline)
- Positioning & differentiation
- Customer journey mapping
- Offline-to-online & online-to-offline integration
- Brand strategy untuk IG & TikTok

GAYA BICARA: Strategic, visioner, big-picture thinker yang tetap praktis.
OUTPUT: Bahasa Indonesia, dengan framework yang jelas, matrix, dan roadmap yang runut."""


def run(
    business_type: str,
    current_challenge: str = "",
    competitor: str = "",
    target_market: str = "",
) -> str:
    """
    Buat strategi marketing komprehensif.

    Args:
        business_type: Jenis bisnis
        current_challenge: Tantangan saat ini (opsional)
        competitor: Kompetitor utama (opsional)
        target_market: Target market (opsional)
    """
    llm = get_llm()

    prompt = f"""Buat strategi marketing komprehensif yang mengombinasikan offline + Instagram + TikTok.

INPUT:
- Bisnis: {business_type}
- Tantangan saat ini: {current_challenge or '-'}
- Kompetitor: {competitor or '-'}
- Target market: {target_market or '-'}

OUTPUT:

## SITUATIONAL ANALYSIS

### SWOT
| Strengths | Weaknesses |
|-----------|------------|
| | |

| Opportunities | Threats |
|--------------|---------|
| | |

### Competitive Landscape
- Posisi kita vs kompetitor
- Blue ocean opportunity yang bisa digarap
- Differentiation strategy

## TARGET AUDIENCE (Persona)
Buat 2-3 persona detail:
- Nama, umur, pekerjaan, lokasi
- Pain points & goals
- Media consumption (online + offline)
- Touchpoint yang paling efektif

## BRAND POSITIONING

### Positioning Statement
Untuk [target] yang [kebutuhan], [brand] adalah [kategori] yang [benefit utama] karena [alasan unik].

### Value Proposition
- 3 benefit utama
- Tagline
- Brand personality & tone of voice

## INSTAGRAM STRATEGY

### Account Optimization
- Bio, highlight, profile pic
- Grid aesthetic & color palette

### Content Strategy
- 5 content pillar
- Posting frequency
- Format mix (Reel, Carousel, Story)
- Hashtag strategy

### Growth Tactics
- Follower acquisition (organik + paid)
- Engagement rate optimization
- Reach conversion (Instagram)
- Conversion strategy (jualan via IG)

### KPI Target (per bulan)
- Follower growth: X%
- Engagement rate: X%
- Reach: X
- Saves: X
- Conversion: X

## TIKTOK STRATEGY

### Profile Setup
- Username, bio, link

### Content Pillar untuk TikTok
- 4-5 pillar khusus TikTok (beda dengan IG)

### Algorithm Hacks
- Hook 3 detik
- Loop strategy
- Trending audio integration
- Comment bait
- Stitch & duet strategy

### Growth Tactics
- Posting frequency (3-5x/hari)
- Best posting times
- Hashtag mix

### KPI Target (per bulan)

## OFFLINE STRATEGY

### Brand Activation
- 3 konsep aktivasi yang impactful
- Lokasi strategis
- Estimated budget
- Success metric

### Partnership & Collaboration
- Jenis partner (komunitas, brand, event organizer)
- Win-win value proposition

### Guerrilla Marketing
- 3 konsep murah tapi impactful
- Budget estimate

## INTEGRATION STRATEGY (Online ↔ Offline)
- Bagaimana online drive offline traffic
- Bagaimana offline boost online content
- Unified brand experience

## 90-DAY EXECUTION ROADMAP
| Bulan | Fokus Utama | Milestone | Budget Range |
|-------|-------------|-----------|--------------|

## MEASUREMENT FRAMEWORK
- Metrics yang di-track
- Tools yang dipakai (prioritaskan yang GRATIS)
- Review cadence

Strategi ini harus komprehensif, terukur, dan siap dijalankan."""

    result = llm.generate(prompt, system=SYSTEM_PROMPT, temperature=0.7)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUTS_DIR / f"agent5_strategy_{timestamp}.md"
    filename.write_text(f"# Strategi Marketing - {business_type}\n\n{result}", encoding="utf-8")

    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m agents.agent5_marketing_strategy <business_type>")
        sys.exit(1)
    print(run(sys.argv[1]))