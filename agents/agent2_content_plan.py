"""
Agent 2: Karya - Content Planner
Tugas: Buat content plan 1 bulan + script viral
"""
from core.llm_client import get_llm
from core.config import OUTPUTS_DIR
from datetime import datetime


SYSTEM_PROMPT = """Kamu adalah Karya, AI Agent spesialis content planning & scriptwriting.

KEAHLIAN:
- Menyusun content calendar 30 hari yang optimal
- Menulis script viral untuk Reels/TikTok/Shorts
- Memahami algoritma IG & TikTok
- Hook psychology & storytelling

GAYA BICARA: Kreatif, tajam, paham tren.
OUTPUT: Dalam Bahasa Indonesia, dengan format script yang siap pakai (ada cue visual, dialog, durasi)."""


def run(niche: str, posts_per_week: int = 7, goal: str = "engagement", extra_context: str = "") -> str:
    """
    Buat content plan 1 bulan.

    Args:
        niche: Niche konten (misal: parenting, bisnis, makanan, dll)
        posts_per_week: Target posting per minggu (default 7 = 1/hari)
        goal: Tujuan utama (engagement | followers | sales | brand)
        extra_context: Brief tambahan (produk, target audience, dll)
    """
    llm = get_llm()
    total_posts = posts_per_week * 4

    prompt = f"""Buat content plan 1 bulan (30 hari) untuk niche: {niche}

KONFIGURASI:
- Total post: {total_posts} post ({posts_per_week}/minggu)
- Goal utama: {goal}
- Konteks tambahan: {extra_context or '-'}

OUTPUT WAJIB:

## BAGIAN 1: CONTENT PILLAR
Tentukan 4-5 content pillar dengan bobot (%) yang menutupi seluruh bulan.
Contoh: Edukasi 40%, Entertainment 25%, Behind the scene 15%, Testimoni 10%, Promo 10%

## BAGIAN 2: CONTENT CALENDAR (30 HARI)
Buat tabel untuk 30 hari dengan kolom:
| Tanggal | Hari | Pillar | Format | Judul/Topic | Hook | Hashtag | Goal |

## BAGIAN 3: 10 SCRIPT VIRAL LENGKAP
Pilih 10 post terbaik dari kalender di atas, lalu tulis script lengkap:

### Script #[nomor]: [Judul]
- **Format**: Reel/TikTok/Carousel
- **Durasi**: ... detik
- **Hook (3 detik pertama)**: ...
- **Body**: ...
- **CTA**: ...
- **Visual cue**: ...
- **Audio suggestion**: ...
- **Kenapa viral**: ...

## BAGIAN 4: HASHTAG BANK
- 30 hashtag utama (high volume)
- 30 hashtag niche (mid volume)
- 30 hashtag long-tail (low competition)

## BAGIAN 5: BEST PRACTICES
- 5 pola hook yang akan kita pakai
- 3 format konten paling potensial
- Timing posting terbaik
- Engagement bait yang aman (tidak spam)

Pastikan plan ini siap dieksekusi, detail, dan memiliki potensi viral tinggi."""

    result = llm.generate(prompt, system=SYSTEM_PROMPT, temperature=0.8)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUTS_DIR / f"agent2_content_plan_{timestamp}.md"
    filename.write_text(f"# Content Plan 1 Bulan - {niche}\n\n{result}", encoding="utf-8")

    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m agents.agent2_content_plan <niche> [posts_per_week]")
        sys.exit(1)
    niche = sys.argv[1]
    ppw = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    print(run(niche, ppw))
