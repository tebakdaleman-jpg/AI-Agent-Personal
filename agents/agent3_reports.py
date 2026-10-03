"""
Agent 3: Lensa - Analytics Reporter
Tugas: Report mingguan & bulanan social media
"""
from core.llm_client import get_llm
from core.config import OUTPUTS_DIR
from datetime import datetime


SYSTEM_PROMPT = """Kamu adalah Lensa, AI Agent spesialis analytics & reporting sosial media.

KEAHLIAN:
- Menganalisis metrik IG & TikTok (reach, impressions, engagement, saves, shares)
- Membuat laporan yang actionable, bukan cuma angka
- Menemukan insight tersembunyi dari pola data
- Rekomendasi berdasarkan data

GAYA BICARA: Analitis, objektif, tajam dalam menemukan insight.
OUTPUT: Bahasa Indonesia, dengan tabel, grafik ASCII jika perlu, dan rekomendasi konkret."""


def run(period: str = "weekly", data: str = "", platform: str = "instagram") -> str:
    """
    Buat report analytics.

    Args:
        period: 'weekly' | 'monthly'
        data: Data mentah (follower, reach, engagement, dll) - bisa dipaste langsung
        platform: 'instagram' | 'tiktok' | 'both'
    """
    llm = get_llm()

    prompt = f"""Buat laporan analytics sosial media.

PERIODE: {period.upper()}
PLATFORM: {platform}

DATA MENTAH:
{data or 'Tidak ada data mentah - buat template laporan standar yang bisa diisi'}

OUTPUT WAJIB:

## EXECUTIVE SUMMARY
- 3 highlight utama minggu/bulan ini
- 1 angka yang perlu diwaspadai
- 1 angka paling membanggakan

## PERFORMA AKUN
Buat tabel ringkasan:

| Metrik | Minggu/Bulan Ini | Sebelumnya | Perubahan (%) |
|--------|------------------|------------|---------------|
| Followers | | | |
| Reach | | | |
| Impressions | | | |
| Engagement Rate | | | |
| Saves | | | |
| Shares | | | |
| Profile Visits | | | |
| Link Clicks | | | |

## TOP 5 KONTEN PERFORMA TERBAIK
| Rank | Judul/Topik | Format | Reach | Engagement | Mengapa Works |
|------|-------------|--------|-------|------------|---------------|

## TOP 3 KONTEN PERFORMA TERBURUK
| Judul/Topik | Format | Reach | Engagement | Hipotesis Mengapa Gagal |
|-------------|--------|-------|------------|--------------------------|

## INSIGHT & ANALISIS
- Pola yang muncul dari top content
- Audience behavior pattern
- Content pillar mana yang paling & paling kurang perform
- Waktu posting paling optimal
- Hashtag/keyword paling efektif

## REKOMENDASI MINGGU/DEPAN
- 5 quick wins untuk minggu/bulan depan
- 3 eksperimen yang harus dicoba
- 1 hal yang harus DIHENTIKAN
- Forecast: target angka realistis untuk periode berikutnya

## ACTION ITEMS
Checklist actionable untuk tim/owner:
- [ ]
- [ ]
- [ ]

Pastikan laporan bisa langsung dipresentasikan ke klien atau stakeholder."""

    result = llm.generate(prompt, system=SYSTEM_PROMPT, temperature=0.5)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUTS_DIR / f"agent3_report_{period}_{timestamp}.md"
    filename.write_text(f"# Report {period.title()} - {platform}\n\n{result}", encoding="utf-8")

    return result


if __name__ == "__main__":
    import sys
    period = sys.argv[1] if len(sys.argv) > 1 else "weekly"
    print(run(period))