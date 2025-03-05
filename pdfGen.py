import PyPDF2
from base import Character
from reportlab.pdfgen import canvas

def fill_character_sheet(input_pdf, output_pdf, character):
    """Vepíše data do existujícího D&D PDF sheetu."""
    
    # Vytvoříme overlay s textem
    overlay_pdf = "overlay.pdf"
    c = canvas.Canvas(overlay_pdf)
    
    # Pozice závisí na konkrétním PDF – budeš muset upravit souřadnice!
    c.setFont("Helvetica-Bold", 12)
    c.drawString(150, 700, character.name)  # Jméno
    c.drawString(150, 680, character.race.name)  # Rasa
    c.drawString(150, 660, character.char_class.name)  # Povolání
    c.drawString(150, 640, character.background.name)  # Zázemí
    
    # Atributy (pozice upravit podle layoutu PDF)
    y_pos = 600
    for stat, value in character.stats.items():
        c.drawString(150, y_pos, f"{value}")
        y_pos -= 20

    c.save()

    # Otevřeme původní PDF a overlay
    with open(input_pdf, "rb") as base_pdf_file, open(overlay_pdf, "rb") as overlay_file:
        base_pdf = PyPDF2.PdfReader(base_pdf_file)
        overlay = PyPDF2.PdfReader(overlay_file)
        writer = PyPDF2.PdfWriter()

        # Přidáme overlay na každou stránku
        for i in range(len(base_pdf.pages)):
            base_page = base_pdf.pages[i]
            if i == 0:  # Pouze na první stránku přidáme overlay
                overlay_page = overlay.pages[0]
                base_page.merge_page(overlay_page)
            writer.add_page(base_page)

        # Uložíme výsledek
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)

    print(f"Data byla vepsána do {output_pdf}!")

# Příklad použití
fill_character_sheet("dnd_character_sheet.pdf", "character_filled.pdf", Character)
