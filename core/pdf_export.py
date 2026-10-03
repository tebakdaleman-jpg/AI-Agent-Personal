"""PDF export - convert markdown agent output ke PDF."""
import re
from pathlib import Path
from datetime import datetime
from fpdf import FPDF
from .config import OUTPUTS_DIR, REPORTS_DIR


class MarkdownPDF(FPDF):
    """Custom FPDF untuk handle markdown -> PDF."""

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128)
            self.cell(0, 5, "AI Agent Personal - Generated Report", align="C")
            self.ln(8)
            self.set_text_color(0)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128)
        self.cell(0, 8, f"Halaman {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, title: str):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(40, 80, 150)
        self.ln(4)
        self.multi_cell(0, 7, title)
        self.set_text_color(0)
        self.ln(2)

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(60)
        self.ln(3)
        self.multi_cell(0, 6, title)
        self.set_text_color(0)
        self.ln(1)

    def body_text(self, text: str):
        self.set_font("Helvetica", "", 10)
        # Bersihkan markdown
        text = self._clean_markdown(text)
        # Wrap text
        self.multi_cell(0, 5, text)
        self.ln(1)

    def _clean_markdown(self, text: str) -> str:
        """Bersihkan markdown syntax untuk PDF."""
        # Bold + italic
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        # Inline code
        text = re.sub(r'`(.+?)`', r'\1', text)
        # Links
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1 (\2)', text)
        # Bullets
        text = re.sub(r'^\s*[-*+]\s+', '- ', text, flags=re.MULTILINE)
        # Numbered list
        text = re.sub(r'^\s*(\d+)\.\s+', r'\1. ', text, flags=re.MULTILINE)
        # Unicode chars yang gak di-support latin-1
        text = text.replace("•", "-")  # bullet
        text = text.replace("—", "--")  # em-dash
        text = text.replace("–", "-")  # en-dash
        text = text.replace("→", "->")  # arrow
        text = text.replace("←", "<-")
        text = text.replace("'", "'")
        text = text.replace("'", "'")
        text = text.replace('"', '"')
        text = text.replace('"', '"')
        text = text.replace("…", "...")
        text = text.replace("✓", "[OK]")
        text = text.replace("✗", "[X]")
        text = text.replace("⚠", "[!]")
        text = text.replace("⭐", "*")
        text = text.replace("📍", "[loc]")
        text = text.replace("💡", "[i]")
        text = text.replace("🎯", "[t]")
        text = text.replace("✅", "[OK]")
        text = text.replace("❌", "[X]")
        text = text.replace("🤖", "")
        text = text.replace("📊", "")
        text = text.replace("📋", "")
        text = text.replace("🔍", "")
        text = text.replace("✍️", "")
        text = text.replace("🧭", "")
        text = text.replace("💰", "")
        return text


def export_to_pdf(markdown_text: str, title: str = "Report", save_dir: Path = None) -> Path:
    """Convert markdown text ke PDF.

    Args:
        markdown_text: Output dari agent (markdown)
        title: Judul PDF
        save_dir: Folder simpan (default: data/outputs)

    Returns: Path ke file PDF yang dihasilkan.
    """
    if save_dir is None:
        save_dir = OUTPUTS_DIR
    save_dir.mkdir(parents=True, exist_ok=True)

    pdf = MarkdownPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title page
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(40, 80, 150)
    pdf.multi_cell(0, 10, title)
    pdf.set_text_color(0)
    pdf.set_font("Helvetica", "I", 9)
    timestamp = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    pdf.cell(0, 6, f"Generated: {timestamp}", ln=1)
    pdf.cell(0, 6, "By AI Agent Personal", ln=1)
    pdf.ln(8)

    # Parse markdown line-by-line
    lines = markdown_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        # Skip empty
        if not line.strip():
            i += 1
            continue

        # Tables: detect dan render sebagai tabel sederhana
        if line.startswith("|") and i + 1 < len(lines) and "---" in lines[i + 1]:
            # Kumpulkan baris tabel
            table_lines = [line]
            j = i + 1
            while j < len(lines) and lines[j].startswith("|"):
                if "---" in lines[j]:
                    j += 1
                    continue
                table_lines.append(lines[j])
                j += 1
            # Render tabel sebagai monospace
            pdf.set_font("Courier", "", 8)
            for tbl_line in table_lines:
                cleaned = tbl_line.replace("|", " | ").strip()
                try:
                    pdf.multi_cell(0, 4, cleaned)
                except Exception:
                    pass
            pdf.set_font("Helvetica", "", 10)
            pdf.ln(2)
            i = j
            continue

        # Headers
        if line.startswith("# "):
            pdf.chapter_title(line[2:].strip())
        elif line.startswith("## "):
            pdf.section_title(line[3:].strip())
        elif line.startswith("### "):
            pdf.set_font("Helvetica", "B", 10)
            pdf.ln(2)
            pdf.multi_cell(0, 5, line[4:].strip())
            pdf.set_font("Helvetica", "", 10)
            pdf.ln(1)
        # Lists
        elif line.lstrip().startswith(("- ", "* ", "• ")):
            text = line.lstrip()[2:] if line.lstrip()[:2] in ("- ", "* ") else line.lstrip()[2:]
            cleaned = pdf._clean_markdown(text)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 5, f"- {cleaned}")
        elif re.match(r'^\d+\.\s', line.lstrip()):
            # Numbered list
            cleaned = pdf._clean_markdown(line.strip())
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5, cleaned)
        # Horizontal rule
        elif line.strip() in ("---", "***", "___"):
            pdf.ln(2)
            pdf.set_draw_color(200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
            pdf.set_draw_color(0)
        # Normal text
        else:
            pdf.body_text(line)

        i += 1

    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = re.sub(r"[^\w\s-]", "", title)[:50].strip().replace(" ", "_")
    filename = save_dir / f"{safe_title}_{timestamp}.pdf"
    pdf.output(str(filename))
    return filename


if __name__ == "__main__":
    # Test
    sample = """
# Test Report
## Section 1
This is **bold** and *italic*.

- Item 1
- Item 2

| Col A | Col B |
|-------|-------|
| 1 | 2 |
| 3 | 4 |
"""
    path = export_to_pdf(sample, "Test Report")
    print(f"PDF created: {path}")