from base import races, Class, backgrounds, Character, classes, hit_dice, names, skill_positions, trait_descriptions, spells_by_class, class_spell_slots, spells_descriptions, cantripps_descriptions

# Define class_spells using spells_by_class
class_spells = spells_by_class
import random
import textwrap

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

def select_spells(char_class):
    """Umožní hráči vybrat pevný počet cantripů a 1st-level spellů odděleně."""
    
    class_name = char_class.name
    if class_name not in spells_by_class or class_name not in class_spell_slots:
        print(f"{class_name} nemá žádná kouzla na 1. úrovni.")
        return {"cantrips": [], "spells": []}

    spell_limits = class_spell_slots[class_name]
    cantrip_limit = spell_limits["cantrips"]
    spell_limit = spell_limits["spells"] 

    spell_choices = spells_by_class[class_name]
    selected_spells = {"cantrips": [], "spells": []}

    # ✅ Výběr cantripů (pokud classa nějaké má)
    if cantrip_limit > 0:
        print(f"Vyběr: {cantrip_limit} Cantrips pro {class_name}:")
        selected_spells["cantrips"] = select_from_list(spell_choices["cantrips"], cantrip_limit)

    # ✅ Výběr 1st-level spellů (pokud classa nějaké má)
    if spell_limit > 0:
        print(f"Vyběr: {spell_limit} Spells 1. úrovně pro  {class_name}:")
        selected_spells["spells"] = select_from_list(spell_choices["spells"], spell_limit)

    return selected_spells

def select_from_list(spell_list, limit):
    """Pomocná funkce pro výběr pevně daného počtu kouzel."""
    selected = []
    while len(selected) < limit:
        print("\nMůžete vybrat:")
        for idx, spell in enumerate(spell_list, 1):
            print(f"{idx}. {spell}")

        choice = input(f"Vybeirate z (1-{len(spell_list)}), {limit - len(selected)} zbývá: ")
        if choice.isdigit():
            selected_idx = int(choice) - 1
            if 0 <= selected_idx < len(spell_list) and spell_list[selected_idx] not in selected:
                selected.append(spell_list[selected_idx])
            else:
                print("❌ Neplatná volba nebo už vybrané kouzlo, zkus znovu.")
        else:
            print("❌ Zadej číslo kouzla.")

    return selected
    

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
    character = Character(name, race, char_class, background, hit_dice, skills, traits, )
    constitution_mod = character.stats.get("Constitution", 0)  # Modifikátor Constitution
    character.hit_dice, character.hp = calculate_hit_points(char_class, constitution_mod)
    skills = character.set_skills()
    traits = character.set_traits()
    character.spells = select_spells(char_class)
    

    print("\n=== VYTVOŘENÁ POSTAVA ===")
    print(character)
    print(f"HP: {character.hp}")  
    print(f"Hit Dice: {character.hit_dice}")
    print(f"Skills: {skills}")
    print(f"Traits: {traits}")
    print(f"Spells: {character.spells}")
    return character


#################PDFPRENOS#################
import PyPDF2
from reportlab.pdfgen import canvas

def calculate_stat_bonus(stat_value):
    """Vypočítá bonus na základě hodnoty statu."""
    return (stat_value - 10) // 2


def fill_character_sheet(input_pdf, output_pdf, character, spell_limits):
    """Vepíše data do existujícího D&D PDF sheetu."""
    
    # Vytvoříme overlay s textem
    overlay_pdf = "overlay.pdf"
    c = canvas.Canvas(overlay_pdf)
    
    # Pozice závisí na konkrétním PDF 
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 715, character.name)  # Jméno
    c.drawString(270, 705, character.race.name)  # Rasa
    c.drawString(270, 730, character.char_class.name)  # Povolání
    c.drawString(385, 730, character.background.name)  # Zázemí
    c.drawString(290, 585, str(character.hp))  # Hit Dice
    c.drawString(233, 448, str(character.hit_dice))  # HP
    
    c.setFont("Helvetica", 12)
    for skill in character.skills:
        if skill in skill_positions:
            x, y = skill_positions[skill]
            c.drawString(x, y, "•")  # Přidáme tečku

    c.setFont("Helvetica", 9)
    traits_x = 412  # X souřadnice
    traits_y = 394  # Začátek seznamu vlastností
    # ✅ Vykreslení traits (vlastností)
    for trait in character.set_traits():
        description = trait_descriptions.get(trait, "Neznámá vlastnost.")  
        wrapped_text = textwrap.wrap(f"• {trait}: {description}", width=30)  # Zalamování textu
        for line in wrapped_text:
            c.drawString(traits_x, traits_y, line)
            traits_y -= 10  # Posun dolů pro další řádek

    c.setFont("Helvetica", 13)
    y_pos = 620
    for stat, value in character.stats.items():
        c.drawString(40, y_pos, f"{value}")
        y_pos -= 70
    
    c.showPage()
    c.showPage()

  
    # ✅ Přidání spellcasting class & DC
    c.setFont("Helvetica-Bold", 14)
    if character.char_class.name == "Warlock":
        spell_save_dc = 8 + character.stats.get("Proficiency Bonus", 2) + calculate_stat_bonus(character.stats.get("Charisma", 0))
        spell_attack_bonus = spell_save_dc - 8
    elif character.char_class.name == "Wizard":
        spell_save_dc = 8 + character.stats.get("Proficiency Bonus", 2) + calculate_stat_bonus(character.stats.get("Intelligence", 0))
        spell_attack_bonus = spell_save_dc - 8
    elif character.char_class.name == "Cleric":
        spell_save_dc = 8 + character.stats.get("Proficiency Bonus", 2) + calculate_stat_bonus(character.stats.get("Wisdom", 0))
        spell_attack_bonus = spell_save_dc - 8
    elif character.char_class.name == "Druid":
        spell_save_dc = 8 + character.stats.get("Proficiency Bonus", 2) + calculate_stat_bonus(character.stats.get("Wisdom", 0))
        spell_attack_bonus = spell_save_dc - 8
    elif character.char_class.name == "Bard":
        spell_save_dc = 8 + character.stats.get("Proficiency Bonus", 2) + calculate_stat_bonus(character.stats.get("Charisma", 0))
        spell_attack_bonus = spell_save_dc - 8
    elif character.char_class.name == "Sorcerer":
        spell_save_dc = 8 + character.stats.get("Proficiency Bonus", 2) + calculate_stat_bonus(character.stats.get("Charisma", 0))
        spell_attack_bonus = spell_save_dc - 8
    elif character.char_class.name == "Paladin":
        spell_save_dc = 8 + character.stats.get("Proficiency Bonus", 2) + calculate_stat_bonus(character.stats.get("Charisma", 0))
        spell_attack_bonus = spell_save_dc - 8
    elif character.char_class.name == "Ranger":
        spell_save_dc = 8 + character.stats.get("Proficiency Bonus", 2) + calculate_stat_bonus(character.stats.get("Wisdom", 0))
        spell_attack_bonus = spell_save_dc - 8
    # Přidejte další třídy podle potřeby
    else:
        spell_save_dc = 8 + character.stats.get("Proficiency Bonus", 2)
        spell_attack_bonus = spell_save_dc - 8

    c.setFont("Helvetica-Bold", 14)
    c.drawString(385, 720, f":{spell_save_dc}")
    c.drawString(490, 720, f":{spell_attack_bonus}")


    # ✅ Přidání cantripů a spellů
    spell_x = 40  # Define spell_x with an appropriate value
    spell_y = 610  # Define spell_y with an appropriate value
    for spell_type, spells in character.spells.items():
        c.setFont("Helvetica", 10)
        c.drawString(spell_x, spell_y, f"{spell_type.capitalize()}s:")
        spell_y -= 10  # Posun dolů pro další řádek
        wrapped_text = textwrap.wrap(f"{spell_type.capitalize()}s:", width=30)
        if spell_limits["cantrips"] == 2:
            for spell in spells:
                if spell_type.lower() == "cantrips":
                    description = cantripps_descriptions.get(spell, "Neznámé kouzlo.")
                else:
                    description = spells_descriptions.get(spell, "Neznámé kouzlo.")
                
                wrapped_spell = textwrap.wrap(f"{spell}: {description}", width=35)
                for line in wrapped_spell:
                    c.drawString(spell_x, spell_y, line)
                    spell_y -= 13
                spell_y -= 5
            if spell_type.lower() == "cantrips":
                 spell_y = 437
        c.setFont("Helvetica", 6)
        if spell_limits["cantrips"] >= 3:
            for spell in spells:
                if spell_type.lower() == "cantrips":
                    description = cantripps_descriptions.get(spell, "Neznámé kouzlo.")
                else:
                    description = spells_descriptions.get(spell, "Neznámé kouzlo.")
                
                wrapped_spell = textwrap.wrap(f"{spell}: {description}", width=60)
                for line in wrapped_spell:
                    c.drawString(spell_x, spell_y, line)
                    spell_y -= 6
                spell_y -= 5
            if spell_type.lower() == "cantrips":
                 spell_y = 437  # Reset pozice pro další typ kouzel
            
        
        c.setFont("Helvetica", 10)
        if spell_limits["cantrips"] == 0:
            for spell in spells:
                if spell_type.lower() == "cantrips":
                    description = cantripps_descriptions.get(spell, "Neznámé kouzlo.")
                else:
                    description = spells_descriptions.get(spell, "Neznámé kouzlo.")
                
                wrapped_spell = textwrap.wrap(f"{spell}: {description}", width=40)
                for line in wrapped_spell:
                    c.drawString(spell_x, spell_y, line)
                    spell_y -= 10
                spell_y -= 5
            if spell_type.lower() == "cantrips":
                 spell_y = 437

            
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
        for i in range(len(base_pdf.pages)):
            base_page = base_pdf.pages[i]
            if i == 2:  # ⚠️ TŘETÍ STRÁNKA (index 2)
                overlay_page = overlay.pages[2]
                base_page.merge_page(overlay_page)
                writer.add_page(base_page)
            
        # Uložíme výsledek
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)

    print(f"Data byla vepsána do {output_pdf}!")

# Příklad použití
character = generate_character()
fill_character_sheet("dnd_character_sheet.pdf", "character_sheet_filled.pdf", character, class_spell_slots[character.char_class.name])

