import io
import json
import os
import uuid
from PyPDF2 import PdfReader
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor

def extract_text(file_bytes, mime_type):
    if mime_type == "application/pdf":
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join([page.extract_text() for page in reader.pages])
    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return file_bytes.decode("utf-8", errors="ignore")

def apply_edit(text, instructions):
    if "replace" in instructions.lower():
        parts = instructions.split("'")
        if len(parts) >= 3: return text.replace(parts[1], parts[3])
    return text

def repackage_and_save(text, format_type, filename_base):
    file_id = str(uuid.uuid4())
    file_path = f"temp/{file_id}.{format_type}"
    os.makedirs("temp", exist_ok=True)

    # Custom colors
    silver = HexColor('#C0C0C0')
    light_blue = HexColor('#4A90E2')
    white = HexColor('#FFFFFF')

    if format_type == "pdf":
        c = canvas.Canvas(file_path, pagesize=letter)
        lines = text.split("\n")
        y = 750
        for line in lines:
            c.drawString(50, y, line)
            y -= 15
            if y < 50: c.showPage(); y = 750

        # --- CUSTOM WATERMARK DESIGN ---
        c.showPage() # Add a final page for the watermark
        width, height = letter
        center_x = width / 2
        center_y = height / 2

        # 1. "From" (Faint Silver, small)
        c.setFont("Helvetica", 12)
        c.setFillColor(silver)
        c.drawCentredString(center_x, center_y + 30, "From")

        # 2. "DOCFORGE" (Bold Light Blue, large)
        c.setFont("Helvetica-Bold", 36)
        c.setFillColor(light_blue)
        c.drawCentredString(center_x, center_y - 15, "DOCFORGE")

        # 3. "JESUS LOVES YOU ❤️" (White, pronounced, large)
        c.setFont("Helvetica-BoldOblique", 28)
        c.setFillColor(white)
        c.drawCentredString(center_x, center_y - 60, "JESUS LOVES YOU ❤️")
        c.save()

    elif format_type == "docx":
        doc = Document()
        for line in text.split("\n"): doc.add_paragraph(line)
        
        # Watermark footer (Note: DOCX doesn't support colored text in footers easily without advanced runs, 
        # but this is the cleanest standard implementation)
        section = doc.sections[-1]
        footer = section.footer
        p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p.text = "From DOCFORGE, JESUS LOVES YOU ❤️"
        p.alignment = 1
        doc.save(file_path)

    elif format_type == "json":
        try: data = json.loads(text)
        except: data = {"content": text}
        with open(file_path, "w") as f: json.dump(data, f)

    else: # txt
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text + f"\n\nFrom\nDOCFORGE\nJESUS LOVES YOU ❤️")

    return file_path
