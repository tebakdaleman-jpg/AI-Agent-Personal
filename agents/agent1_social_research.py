"""
Agent 1: Rimba - Social Media Researcher
Tugas: Riset Instagram & TikTok, tentukan niche, cari konten relevan
"""
from core.llm_client import get_llm
from core.config import OUTPUTS_DIR
from datetime import datetime


SYSTEM_PROMPT = """Kamu adalah Rimba, AI Agent spesialis riset sosial media.

KEAHLIAN:
- Analisis mendalam akun Instagram & TikTok
- Menentukan niche konten yang profitable
- Menemukan pola konten viral
- Memberikan rekomendasi strategis berdasarkan data

GAYA BICARA: Profesional, data-driven, actionable insights.
OUTPUT: Selalu dalam Bahasa Indonesia, terstruktur dengan heading, bullet points, dan tabel jika relevan."""


def run(target: str, platform: str = "instagram", extra_context: str = "") -> str:
    """
    Jalankan riset sosial media.

    Args:
        target: Username/handle atau link akun (misal: @namakamu atau link post)
        platform: 'instagram' | 'tiktok' | 'both'
        extra_context: Konteks tambahan (misal: target market, produk)
    """
    llm = get_llm()

    prompt = f"""Lakukan riset mendalam untuk akun sosial media berikut:

TARGET: {target}
PLATFORM: {platform}
KONTEKS TAMBAHAN: {extra_context or '-'}

Berikan output dengan struktur:

## 1. PROFIL AKUN
- Username, niche, target audience
- Estimasi followers, engagement rate
- Tone of voice & personality brand

## 2. ANALISIS NICHE
- Niche utama & sub-niche
- Mengapa niche ini potensial
- Kompetitor langsung & tidak langsung
- Market size & peluang

## 3. KONTEN RELEVAN (15 ide)
Berikan 15 ide konten yang relevan dengan niche, masing-masing berisi:
- Judul/hook
- Format (Reel/TikTok/Carousel/Story)
- Estimasi potensi viral (1-10)
- Hook pembuka (3 detik pertama)

## 4. POLA KONTEN VIRAL
- Pola hook yang sering works
- Format konten dengan performa terbaik
- Waktu posting optimal
- Hashtag & keyword yang relevan

## 5. REKOMENDASI STRATEGIS
- 5 quick wins yang bisa langsung dieksekusi
- 3 strategi jangka menengah (1-3 bulan)
- 1 strategi jangka panjang (6-12 bulan)
- Risiko & cara mitigasi

Pastikan output sangat detail, actionable, dan berbasis data. Gunakan markdown formatting."""

    result = llm.generate(prompt, system=SYSTEM_PROMPT, temperature=0.7)

    # Simpan output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUTS_DIR / f"agent1_social_research_{timestamp}.md"
    filename.write_text(f"# Riset Sosial Media - {target}\n\n{result}", encoding="utf-8")

    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m agents.agent1_social_research <username> [platform]")
        sys.exit(1)
    target = sys.argv[1]
    platform = sys.argv[2] if len(sys.argv) > 2 else "instagram"
    print(run(target, platform))
