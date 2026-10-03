"""
Agent 6: Hemat - Ads Researcher
Tugas: Riset Meta Ads, TikTok Ads, Google Ads + budget calculation
"""
from core.llm_client import get_llm
from core.config import OUTPUTS_DIR
from datetime import datetime


SYSTEM_PROMPT = """Kamu adalah Hemat, AI Agent spesialis paid ads & budget optimization.

KEAHLIAN:
- Riset Meta Ads (Facebook + Instagram), TikTok Ads, Google Ads
- Kalkulasi budget realistis per minggu/bulan/tahun
- Target audience & interest targeting
- Bidding strategy & optimization
- ROAS forecasting
- Industry benchmarks

GAYA BICARA: Detail, math-driven, ROI-focused, transparan soal asumsi.
OUTPUT: Bahasa Indonesia, dengan tabel kalkulasi yang jelas, asumsi, dan rekomendasi alokasi budget."""


def run(
    business_type: str,
    monthly_budget: str = "Rp 3.000.000",
    goal: str = "sales",
    target_market: str = "",
) -> str:
    """
    Buat strategi ads + kalkulasi budget.

    Args:
        business_type: Jenis bisnis
        monthly_budget: Total budget iklan per bulan
        goal: Tujuan (sales | leads | awareness | app_install)
        target_market: Target market (opsional)
    """
    llm = get_llm()

    prompt = f"""Buat strategi paid ads + kalkulasi budget detail untuk 3 platform.

INPUT:
- Bisnis: {business_type}
- Monthly budget total: {monthly_budget}
- Goal: {goal}
- Target market: {target_market or '-'}

OUTPUT:

## LANDSCAPE & BENCHMARK
Untuk industri {business_type} di Indonesia, rata-rata industri:
- CPM: Rp ...
- CPC: Rp ...
- CTR: X%
- Conversion rate: X%
- ROAS: X

## PLATFORM COMPARISON

### Meta Ads (Facebook + Instagram)
| Aspek | Detail |
|-------|--------|
| Kelebihan | |
| Kekurangan | |
| Cocok untuk | |
| Avg CPM industri | |
| Targeting options | |

### TikTok Ads
| Aspek | Detail |
|-------|--------|
| Kelebihan | |
| Kekurangan | |
| Cocok untuk | |
| Avg CPM industri | |
| Targeting options | |

### Google Ads
| Aspek | Detail |
|-------|--------|
| Kelebihan | |
| Kekurangan | |
| Cocok untuk | |
| Avg CPC industri | |
| Targeting options | |

## BUDGET ALLOCATION (Recommended Split)

### Justifikasi Alokasi
Mengapa split ini?

| Platform | % Budget | Nominal/Bulan | Goals |
|----------|----------|---------------|-------|
| Meta Ads | | | |
| TikTok Ads | | | |
| Google Ads | | | |

## KALKULASI DETAIL

### Meta Ads
- Budget/bulan: Rp ...
- Budget/minggu: Rp ...
- Budget/hari: Rp ...
- Estimasi reach: ...
- Estimasi impressions: ...
- Estimasi clicks: ...
- Estimasi conversions: ...
- Estimasi revenue (jika goal sales): Rp ...
- ROAS: X

### TikTok Ads
(kalkulasi sama)

### Google Ads
(kalkulasi sama)

## TAHUNAN PROJECTION

| Periode | Budget | Expected Results | Notes |
|---------|--------|------------------|-------|

| Bulan | Budget Bulanan | Cumulative | Performance Pattern |
|-------|----------------|------------|---------------------|

## CAMPAIGN STRUCTURE (per platform)

### Meta Ads
- Campaign 1: ... (objective, budget, audience, placements)
- Campaign 2: ...
- Ad sets & creatives (jenis)

### TikTok Ads
- Campaign structure
- Spark Ads vs In-Feed
- Creative recommendations

### Google Ads
- Search vs Display
- Keyword groups
- Negative keywords

## TARGETING RECOMMENDATIONS

### Meta Ads
- Interest targeting
- Lookalike audiences
- Custom audiences

### TikTok Ads
- Interest categories
- Hashtag targeting
- Creator categories

### Google Ads
- Keyword research
- Match types
- Audience signals

## OPTIMIZATION STRATEGY
- Hari 1-7: phase apa
- Hari 8-14: ...
- Kapan scale up vs cut losses
- A/B testing framework
- Creative refresh schedule

## CREATIVE BRIEF
- 3 konsep iklan untuk Meta
- 3 konsep iklan untuk TikTok
- 3 search ad copy untuk Google

## RISK & PITFALLS
- 5 kesalahan umum yang harus dihindari
- Red flags saat optimasi

## ACTION PLAN
- [ ] Setup akun & pixel
- [ ] Install tracking
- [ ] Buat creative
- [ ] Launch campaign
- [ ] Daily monitoring
- [ ] Weekly review
- [ ] Monthly optimization

Asumsikan kita mulai dari NOL dengan budget di atas. Berikan panduan yang benar-benar bisa dieksekusi."""

    result = llm.generate(prompt, system=SYSTEM_PROMPT, temperature=0.5)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUTS_DIR / f"agent6_ads_research_{timestamp}.md"
    filename.write_text(f"# Riset Ads & Budget - {business_type}\n\n{result}", encoding="utf-8")

    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m agents.agent6_ads_research <business_type> [budget]")
        sys.exit(1)
    bt = sys.argv[1]
    budget = sys.argv[2] if len(sys.argv) > 2 else "Rp 3.000.000"
    print(run(bt, budget))