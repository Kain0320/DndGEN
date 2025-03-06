from base import races, Class, backgrounds, Character, classes, hit_dice, names
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

def calculate_hit_points(char_class, constitution_mod):
    """Vypočítá hit dice a maximální HP postavy."""
    dice = char_class.hit_dice  # Např. "1d10", "1d8"
    try:
        _, dice_value = dice.split("d")  # Oddělíme číslo
        max_hp = int(dice_value) + constitution_mod  # Převod na int + bonus z Constitution
    except (ValueError, IndexError):
        raise ValueError(f"Neplatný formát hit dice: {dice}")

    return dice, max_hp

def generate_character():
    """Vygeneruje postavu podle výběru uživatele nebo náhodně."""
    print("\n=== GENERÁTOR POSTAV D&D 5E ===\n")

    race = choose_option(races, "Vyber rasu:")
    char_class = choose_option(classes, "Vyber povolání:")
    background = choose_option(backgrounds, "Vyber zázemí:")

def generate_name(race, gender):
    """Umožní uživateli zadat vlastní jméno nebo vygeneruje náhodné."""
    user_input = input("Chceš zadat vlastní jméno? (ano/ne): ").strip().lower()
    if user_input == "ano":
        name = input("Zadej jméno postavy: ").strip()
        if name:  # Ověření, že něco zadal
            return name
        print("Nezadáno žádné jméno, generuji náhodné...")
    # Pokud uživatel nezadal jméno nebo nezadal nic
    race_name = race.name if hasattr(race, "name") else str(race)
    
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
    
    skills = []  # Initialize skills
    traits = []  # Initialize traits
    character = Character(name, race, char_class, background, hit_dice, skills, traits)
    constitution_mod = character.stats.get("Constitution", 0)  # Modifikátor Constitution
    character.hit_dice, character.hp = calculate_hit_points(char_class, constitution_mod)
    skills = character.set_skills()
    traits = character.set_traits()

    print("\n=== VYTVOŘENÁ POSTAVA ===")
    print(character)
    print(f"HP: {character.hp}")  
    print(f"Hit Dice: {character.hit_dice}")
    print (f"Skills: {skills}")
    print (f"Traits: {traits}")
    return character


#################PDFPRENOS#################
import PyPDF2
from reportlab.pdfgen import canvas

def fill_character_sheet(input_pdf, output_pdf, character):
    """Vepíše data do existujícího D&D PDF sheetu."""
    
    # Vytvoříme overlay s textem
    overlay_pdf = "overlay.pdf"
    c = canvas.Canvas(overlay_pdf)
    
    # Pozice závisí na konkrétním PDF 
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 715, character.name)  # Jméno
    c.drawString(270, 705, character.race.name)  # Rasa
    c.drawString(270, 730, character.char_class.name)  # Povolání
    c.drawString(385, 730, character.background.name)  # Zázemí
    c.drawString(290, 585, str(character.hp))  # Hit Dice
    c.drawString(233, 450, str(character.hit_dice))  # HP
    
    skill_positions = {
        "Acrobatics": (102, 462),
        "Animal Handling": (102, 448),
        "Arcana": (102, 434),
        "Athletics": (102, 422),
        "Deception": (102, 407),
        "History": (102, 394),
        "Insight": (102, 380),
        "Intimidation": (102, 367),
        "Investigation": (102, 350),
        "Medicine": (102, 340),
        "Nature": (102, 322),
        "Perception": (102, 308),
        "Performance": (102, 300),
        "Persuasion": (102, 286),
        "Religion": (102, 273),
        "Sleight of Hand": (102, 257),
        "Stealth": (102, 246),
        "Survival": (102, 233)
    }
    for skill in character.skills:
        if skill in skill_positions:
            x, y = skill_positions[skill]
            c.drawString(x, y, "•")  # Přidáme tečku

    # Atributy 
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
