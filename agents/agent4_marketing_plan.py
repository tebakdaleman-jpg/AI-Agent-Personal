"""
Agent 4: Stratego - Marketing Planner
Tugas: Plan marketing 1 bulan (online + offline)
"""
from core.llm_client import get_llm
from core.config import OUTPUTS_DIR
from datetime import datetime


SYSTEM_PROMPT = """Kamu adalah Stratego, AI Agent spesialis marketing planning.

KEAHLIAN:
- Menyusun marketing plan 30 hari yang terintegrasi
- Activity online (sosial media, ads, content, email, dll)
- Activity offline (event, partnership, sampling, booth, dll)
- Budget allocation yang efisien
- KPI yang terukur

GAYA BICARA: Terukur, real-world applicable, budget-conscious.
OUTPUT: Bahasa Indonesia, sangat terstruktur dengan timeline, owner, budget, KPI per activity."""


def run(
    business_type: str,
    budget: str = "Rp 5.000.000",
    goal: str = "awareness",
    target_market: str = "",
    extra_context: str = "",
) -> str:
    """
    Buat marketing plan 1 bulan.

    Args:
        business_type: Jenis bisnis (misal: F&B, fashion, jasa, dll)
        budget: Total budget untuk 1 bulan
        goal: Tujuan (awareness | leads | sales | retention)
        target_market: Target market (umur, lokasi, behaviour)
        extra_context: Info tambahan
    """
    llm = get_llm()

    prompt = f"""Buat marketing plan komprehensif 1 bulan (30 hari).

INPUT:
- Jenis bisnis: {business_type}
- Total budget: {budget}
- Goal utama: {goal}
- Target market: {target_market or '-'}
- Konteks tambahan: {extra_context or '-'}

OUTPUT:

## MARKETING OBJECTIVES
- Goal SMART untuk 1 bulan (Specific, Measurable, Achievable, Relevant, Time-bound)
- 3 KPI utama
- Target conversion / reach / leads / sales

## BUDGET ALLOCATION
| Kategori | % Budget | Nominal | Justifikasi |
|----------|----------|---------|-------------|
| Online Ads | | | |
| Content Production | | | |
| KOL/Influencer | | | |
| Offline Event | | | |
| Sampling | | | |
| Printing | | | |
| Tools & Software | | | |
| Contingency | | | |

## ONLINE ACTIVITIES (minggu per minggu)

### Minggu 1
| Hari | Activity | Platform/Channel | Detail | Budget | Owner | KPI |
|------|----------|------------------|--------|--------|-------|-----|

### Minggu 2-4 ... (sama formatnya)

## OFFLINE ACTIVITIES

### Event / Activation
- Konsep, lokasi, target audiens, biaya, expected outcome

### Partnership
- Potensi partner, bentuk kerja sama, benefit kedua belah pihak

### Sampling / Booth
- Lokasi, timing, target, materi yang disiapkan

## CONTENT INTEGRATION
- Bagaimana online + offline saling support
- Timeline koordinasi
- Konten yang diproduksi dari setiap aktivitas offline

## RISK & MITIGATION
| Risiko | Dampak | Mitigasi |
|--------|--------|----------|

## MEASUREMENT & REPORTING
- Tools untuk tracking (gratis & berbayar)
- Frekuensi report
- Siapa yang review & action

Buatkan plan ini benar-benar ACTIONABLE - bisa langsung dijalankan tanpa banyak revisi."""

    result = llm.generate(prompt, system=SYSTEM_PROMPT, temperature=0.6)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUTS_DIR / f"agent4_marketing_plan_{timestamp}.md"
    filename.write_text(f"# Marketing Plan 1 Bulan - {business_type}\n\n{result}", encoding="utf-8")

    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m agents.agent4_marketing_plan <business_type> [budget]")
        sys.exit(1)
    bt = sys.argv[1]
    budget = sys.argv[2] if len(sys.argv) > 2 else "Rp 5.000.000"
    print(run(bt, budget))