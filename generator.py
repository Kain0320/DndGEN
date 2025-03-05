from base import races, Class, backgrounds, Character, classes
import random

def choose_option(options, prompt):
    """Umožní uživateli vybrat možnost nebo zvolit náhodnou variantu."""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("0. Random")

    choice = input("Vyber možnost (zadej číslo): ")
    
    if choice == "0":
        return random.choice(list(options.values()))
    elif choice.isdigit() and 1 <= int(choice) <= len(options):
        return list(options.values())[int(choice) - 1]
    else:
        print("Neplatná volba, vybírám náhodně.")
        return random.choice(list(options.values()))
def choose_gender():
    options = ["Muž", "Žena"]
    print("Vyber pohlaví:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    choice = int(input("Zadej číslo: ")) - 1
    return options[choice]

def generate_character():
    """Vygeneruje postavu podle výběru uživatele nebo náhodně."""
    print("\n=== GENERÁTOR POSTAV D&D 5E ===\n")

    race = choose_option(races, "Vyber rasu:")
    char_class = choose_option(classes, "Vyber povolání:")
    background = choose_option(backgrounds, "Vyber zázemí:")

    # Náhodné jméno (jen placeholder, může se vylepšit)
names = {
    "Elf": {"Muž": ["Aerendil", "Thalion", "Legolas"], "Žena": ["Arwen", "Lúthien", "Galadriel"]},
    "Dwarf": {"Muž": ["Thorin", "Balin"], "Žena": ["Dis", "Tana"]},
    "Human": {"Muž": ["Aragorn", "Boromir"], "Žena": ["Eowyn", "Elanor"]},
    "Halfling": {"Muž": ["Frodo", "Bilbo"], "Žena": ["Rosie", "Daisy"]},
    "Kobold": {"Muž": ["Poro", "Koro"], "Žena": ["Saassraa", "Zaassraa"]},
    "Gith": {"Muž": ["Zerthimon", "Vlaak"], "Žena": ["Vlaakith", "Layzel"]},
    "Tiefling": {"Muž": ["Morthos", "Kael"], "Žena": ["Lilith", "Morrigan"]},
    "Dragonborn": {"Muž": ["Bahamut", "Korvax"], "Žena": ["Andarna", "Vey"]},
    "Gnome": {"Muž": ["Rurik", "Boddynock"], "Žena": ["Bimpnottin", "Breena"]}
}

def generate_name(race, gender):
    race_name = race.name if hasattr(race, "name") else str(race)  # Oprava chyby s objektem
    if race_name not in names:
        raise ValueError(f"Rasa '{race_name}' není v databázi jmen!")
    if gender not in names[race_name]:
        raise ValueError(f"Pohlaví '{gender}' není dostupné pro rasu '{race_name}'!")
    return random.choice(names[race_name][gender])
 
def generate_character():
    print("\n=== GENERÁTOR POSTAV D&D 5E ===\n")

    race = choose_option(races, "Vyber rasu:")
    char_class = choose_option(classes, "Vyber povolání:")
    background = choose_option(backgrounds, "Vyber zázemí:")
    gender = choose_gender()
    name = generate_name(race, gender)

    character = Character(name, race, char_class, background)

    print("\n=== VYTVOŘENÁ POSTAVA ===")
    print(character)
    return character

import PyPDF2
from reportlab.pdfgen import canvas

def fill_character_sheet(input_pdf, output_pdf, character):
    """Vepíše data do existujícího D&D PDF sheetu."""
    
    # Vytvoříme overlay s textem
    overlay_pdf = "overlay.pdf"
    c = canvas.Canvas(overlay_pdf)
    
    # Pozice závisí na konkrétním PDF – budeš muset upravit souřadnice!
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 715, character.name)  # Jméno
    c.drawString(270, 705, character.race.name)  # Rasa
    c.drawString(270, 730, character.char_class.name)  # Povolání
    c.drawString(385, 730, character.background.name)  # Zázemí
    
    # Atributy (pozice upravit podle layoutu PDF)
    y_pos = 620
    for stat, value in character.stats.items():
        c.drawString(40, y_pos, f"{value}")
        y_pos -= 70

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
character = generate_character()
fill_character_sheet("dnd_character_sheet.pdf", "character_filled.pdf", character)
