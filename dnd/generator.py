from base import races, Class, backgrounds, Character, classes, hit_dice, names, skill_positions, trait_descriptions, spells_by_class, class_spell_slots, spells_descriptions, cantripps_descriptions, saving_throw_positions, class_items, class_saving_throws, Weapon, Armor, potions_list, magic_items_list, path_classy, stats_positions, stat_skills, classes

# Ensure `races` is defined or imported correctly
if not races:
    races = {"Human": "Human", "Elf": "Elf", "Dwarf": "Dwarf"}  # Example fallback definition
import random
import textwrap
import PyPDF2
import os
import tkinter as tk
from tkinter import Label, Button
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageTk

class_spells = spells_by_class

def choose_option_gui(options, title="Vyber možnost"):
    root = tk.Tk()
    root.title(title)

    chosen = tk.Variable()
    if isinstance(options, dict):
        display_list = list(options.values())
    else:
        display_list = options

    def select(option):
        chosen.set(option)
        root.selected_object = option 
        root.destroy()

    for option in display_list:
        name = option.name if hasattr(option, "name") else str(option)
        btn = tk.Button(root, text=name, width=30, command=lambda opt=option: select(opt))
        btn.pack(pady=3)

    btn_random = tk.Button(root, text="🎲 Náhodně", width=30, command=lambda: select(random.choice(display_list)))
    btn_random.pack(pady=10)

    root.mainloop()
    return getattr(root, "selected_object", random.choice(display_list))

def choose_gender_gui():
    root = tk.Tk()
    root.title("Vyber pohlaví")

    gender = tk.StringVar()

    def select(g):
        gender.set(g)
        root.destroy()

    tk.Button(root, text="Muž", command=lambda: select("Muž")).pack(pady=10)
    tk.Button(root, text="Žena", command=lambda: select("Žena")).pack(pady=10)
    tk.Button(root, text="🎲 Náhodně", command=lambda: select(random.choice(["Muž", "Žena"]))).pack(pady=10)

    root.mainloop()
    return gender.get()

def calculate_hit_points(char_class, constitution_mod):
    """Vypočítá hit dice a maximální HP postavy."""
    dice = char_class.hit_dice  # Např. "1d10", "1d8"
    try:
        _, dice_value = dice.split("d")  # Oddělíme číslo
        max_hp = int(dice_value) + constitution_mod  # Převod na int + bonus z Constitution
    except (ValueError, IndexError):
        raise ValueError(f"Neplatný formát hit dice: {dice}")
    return dice, max_hp

def select_spells_gui(char_class):
    class_name = char_class.name
    spell_data = spells_by_class.get(class_name, {})
    spell_limits = class_spell_slots.get(class_name, {"cantrips": 0, "spells": 0})

    selected = {"cantrips": [], "spells": []}

    def select_from_list(spell_list, limit, spell_type):
        root = tk.Tk()
        root.title(f"Vyber {spell_type} ({limit}) pro {class_name}")
        root.geometry("1400x750")

        selected_local = []
        images = {}
        buttons = {}
        frame = tk.Frame(root)
        frame.pack()

        canvas = tk.Canvas(frame, width=1200, height=650)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0 ), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")
        def on_mousewheel(event):
          canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        def toggle(spell_name):
         if spell_name in selected_local:
             selected_local.remove(spell_name)
             buttons[spell_name].configure(bg="SystemButtonFace")
         elif len(selected_local) < limit:
            selected_local.append(spell_name)
            buttons[spell_name].configure(bg="lightgreen")
        columns = 3
        for index, spell_name in enumerate(spell_list):
            folder = "cantrips" if spell_type.lower() == "cantrips" else "spells"
            spell_path = os.path.join("/Users/user/DNDGEN/DndGEN/dnd/spell_images", folder, spell_name.replace(" ", "_") + ".png")
            frame_inner = tk.Frame(scrollable_frame, padx=10, pady=10, bd=5, relief="groove")
            row = index // columns
            col = index % columns
            frame_inner.grid(row=row, column=col, padx=10, pady=10)

            try:
                img = Image.open(spell_path).resize((350, 450))
                img_tk = ImageTk.PhotoImage(img)
                images[spell_name] = img_tk
                tk.Label(frame_inner, image=img_tk).pack()
            except:
                tk.Label(frame_inner, text=f"{spell_name} (bez obrázku)").pack()

            btn = tk.Button(frame_inner, text=spell_name, command=lambda name=spell_name: toggle(name))
            btn.pack()
            buttons[spell_name] = btn

        def confirm_selection():
            if len(selected_local) < limit:
                tk.messagebox.showerror("Chyba", f"Musíte vybrat alespoň {limit} položek.")
            else:
                root.destroy()

        tk.Button(root, text="✅ Potvrdit", command=confirm_selection).pack(pady=10)
        root.mainloop()
        return selected_local

    # Výběr cantripů
    if spell_limits["cantrips"] > 0:
        selected["cantrips"] = select_from_list(spell_data.get("cantrips", []), spell_limits["cantrips"], "Cantrips")

    # Výběr spellů
    if spell_limits["spells"] > 0:
        selected["spells"] = select_from_list(spell_data.get("spells", []), spell_limits["spells"], "Spells")

    return selected

def generate_items(char_class_name):
    items = []
    if char_class_name in class_items:
        class_item = class_items[char_class_name]
        weapon = choose_option_gui(class_item["weapons"], "Vyber zbraň:")
        items.append(weapon)
        if class_item["armor"]:
            armor = choose_option_gui(class_item["armor"], "Vyber brnění:")
            items.append(armor)
    potion = random.choice(potions_list)
    magic_item = random.choice(magic_items_list)

    return items  + [potion, magic_item]

def choose_portrait_gui(race):
    """GUI pro výběr portrétu postavy podle rasy."""
    portraits_dir = "/Users/user/DNDGEN/DndGEN/dnd/portraits"  # Absolutní cesta ke složce
    race_name = getattr(race, "name", str(race))
    if "<" in race_name:  # Jestli dostaneme něco jako <base.Character.Race object ...>
      race_name = race.__class__.__name__
    race_dir = os.path.join(portraits_dir, race_name)
    portrait_files = [f for f in os.listdir(race_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    root = tk.Tk()
    root.geometry("500x600")
    root.title(f"Výběr portrétu pro {race_name}")
    index = tk.IntVar(value=0)
    def update_image():
        img_path = os.path.join(race_dir, portrait_files[index.get()])
        print(f"🖼️ Načítám obrázek: {img_path}")
        try:
            img = Image.open(img_path)
            img = img.resize((400, 500))
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk  # **Důležité, jinak se obrázek nezobrazí!**
        except Exception as e:
            print(f"❌ Chyba při načítání obrázku: {e}")

    def next_image():
        index.set((index.get() + 1) % len(portrait_files))
        update_image()

    def prev_image():
        index.set((index.get() - 1) % len(portrait_files))
        update_image()

    def select_image():
        root.selected_portrait = os.path.join(race_dir, portrait_files[index.get()])
        root.destroy()

    def select_random():
        root.selected_portrait = os.path.join(race_dir, random.choice(portrait_files))
        root.destroy()

    image_label = Label(root)
    image_label.pack()

    update_image()  # Zobrazí první obrázek

    btn_prev = Button(root, text="⬅️ Předchozí", command=prev_image)
    btn_prev.pack(side=tk.LEFT, padx=10)

    btn_select = Button(root, text="✅ Vybrat", command=select_image)
    btn_select.pack(side=tk.LEFT, padx=10)

    btn_random = Button(root, text="🎲 Náhodně", command=select_random)
    btn_random.pack(side=tk.LEFT, padx=10)

    btn_next = Button(root, text="➡️ Další", command=next_image)
    btn_next.pack(side=tk.LEFT, padx=10)

    root.mainloop()

    # ✅ Vrátíme vybraný portrét
    return getattr(root, "selected_portrait")

def get_saving_throws(character):
    """Vrací saving throws jako slovník: {'Strength': '+4', ...}"""
    saving_throws = {}
    profs = class_saving_throws.get(character.char_class.name, [])
 # Třídy mají různé proficiency
    prof_bonus = (2)

    for stat, value in character.stats.items():
        base = calculate_stat_bonus(value)
        total = base + prof_bonus if stat in profs else base
        formatted = f"+{total}" if total >= 0 else str(total)
        saving_throws[stat] = formatted

    return saving_throws

def generate_path(char_class_name):
    if char_class_name in path_classy:
        path = choose_option_gui(path_classy[char_class_name], "Vyber podclassu:")
        return path

def generate_name_gui(race, gender):
    race_name = race.name if hasattr(race, "name") else str(race)
    name_list = names.get(race_name, {}).get(gender, [])
    if not name_list:
        name_list = ["Default Name"]  # Provide a fallback name if the list is empty
    

    root = tk.Tk()
    root.title("Zadej nebo vyber jméno")

    entry = tk.Entry(root)
    entry.pack(pady=10)
    chosen = tk.StringVar()

    def confirm():
        name = entry.get()
        chosen.set(name if name else random.choice(name_list))
        root.destroy()

    btn_random = tk.Button(root, text="🎲 Náhodné jméno", command=lambda: entry.insert(0, random.choice(name_list)))
    btn_random.pack()
    tk.Button(root, text="✅ Potvrdit", command=confirm).pack()
    

    root.mainloop()
    return chosen.get()
    
def get_skills(character):
    bonus_skills = {}
    prof_bonus = 2

    for skill, related_stat in stat_skills.items():
        stat_value = character.stats.get(related_stat, 10)
        base = calculate_stat_bonus(stat_value)
        total = base + prof_bonus if skill in character.skills else base
        formatted = f"+{total}" if total >= 0 else str(total)
        bonus_skills[skill] = formatted
    return bonus_skills

def set_ac(character):
    """Nastaví AC (Armor Class) postavy na základě jejího vybavení."""
    dex_bonus = calculate_stat_bonus(character.stats.get("Dexterity", 0))
    base_ac = 10 + dex_bonus  # Základní AC bez brnění
    if character.char_class.name == "Monk":
        wis_bonus = calculate_stat_bonus(character.stats.get("Wisdom", 0))
        base_ac += wis_bonus
    elif character.char_class.name == "Barbarian":
        con_bonus = calculate_stat_bonus(character.stats.get("Constitution", 0))
        base_ac += con_bonus
    for item in character.inventory:
        if isinstance(item, Armor):
            if item.armor_type == "heavy":
                return item.ac  # Těžké brnění ignoruje bonus za obratnost
            else:
                return item.ac + dex_bonus  # Přidá bonus za obratnost pro lehké/střední brnění

    return base_ac  # Pokud není žádné brnění, vrátí základní AC

def generate_character():
    print("\n=== GENERÁTOR POSTAV D&D 5E ===\n")

    race = choose_option_gui(races, "Vyber rasu:")
    char_class = choose_option_gui(classes, "Vyber povolání:")
    background = choose_option_gui(backgrounds, "Vyber zázemí:")
    gender = choose_gender_gui()
    name = generate_name_gui(race, gender)
    portrait = choose_portrait_gui(race)
    skills = []  # Initialize skills
    traits = []  # Initialize traits
    character = Character(name, race, char_class, background, hit_dice, skills, traits, generate_items= generate_items)
    constitution_mod = character.stats.get("Constitution", 0)  # Modifikátor Constitution
    character.hit_dice, character.hp = calculate_hit_points(char_class, constitution_mod)
    skills = character.set_skills()
    traits = character.set_traits()
    character.spells = select_spells_gui(char_class)
    char_class.apply_class_bonus(character)
    character.path = generate_path(char_class.name) if char_class.name in path_classy else None
    character.portrait = portrait # Replace with a valid default path


    

    print("\n=== VYTVOŘENÁ POSTAVA ===")
    print(character)
    print(f"HP: {character.hp}")  
    print(f"Hit Dice: {character.hit_dice}")
    print(f"Skills: {skills}")
    print(f"Traits: {traits}")
    print(f"Spells: {character.spells}")
    inventory_names = [item.name if hasattr(item, "name") else str(item) for item in character.inventory]
    print(f"Inventory: {inventory_names}")
    print(f"AC: {set_ac(character)}")
    print(f"Features: {character.features}")
    print(f"Path: {character.path}")
    return character

#################PDFPRENOS#################

def calculate_stat_bonus(stat_value):
    """Vypočítá bonus na základě hodnoty statu."""
    return (stat_value - 10) // 2

def fill_character_sheet(input_pdf, output_pdf, character, spell_limits):
    """Vepíše data do existujícího D&D PDF sheetu."""
    
    # Vytvoříme overlay s textem
    overlay_pdf = "overlay.pdf"
    c = canvas.Canvas(overlay_pdf)
    
    "Saving throw"
    x_save = 112
    y_save_start = 579
    spacing = 13.5  # Mezera mezi jednotlivými staty
    c.setFont("Helvetica", 10)
    character_saving_throws = get_saving_throws(character)
    for i, stat in enumerate(["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]):
        y = y_save_start - i * spacing
        value = character_saving_throws[stat]
        c.drawString(x_save, y, f" {value}")

    c.setFont("Helvetica", 12)
    proficient_saves = class_saving_throws.get(character.char_class.name, [])
    for save_name, (x, y) in saving_throw_positions.items():
      if save_name in proficient_saves:
        c.drawString(x, y, "•")
    ""

    "Portraits"
    portrait_x = 32
    portrait_y = 37
    portrait_width = 170
    portrait_height = 130
    try:
        print(f"🖼️ Vkládám obrázek do PDF: {character.portrait}")  # ✅ Debug
        img_reader = ImageReader(character.portrait)
        c.drawImage(img_reader, portrait_x, portrait_y, width=portrait_width, height=portrait_height)
        print("✅ Obrázek úspěšně vložen do PDF!")
    except Exception as e:
        print(f"❌ Chyba při vkládání obrázku do PDF: {e}")
    ""

    "Base"
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 715, character.name)  # Jméno
    c.drawString(270, 705, character.race.name)  # Rasa
    c.drawString(270, 730, character.char_class.name)  # Povolání
    c.drawString(385, 730, character.background.name)  # Zázemí
    c.drawString(290, 585, str(character.hp))  # Hit Dice
    c.drawString(233, 448, str(character.hit_dice))  # HP
    ""
      
    "SKILLS"
    c.setFont("Helvetica", 9)
    x_pos = 112
    y_pos_start = 462
    spacing = 13.5  # Mezera mezi jednotlivými staty
    character_skills = get_skills(character)
    skill_list = list(stat_skills.keys())  # Všechny skilly ve správném pořadí

    for i, skill in enumerate(skill_list):
      y = y_pos_start - i * spacing
      value = character_skills.get(skill, "")
      c.drawString(x_pos, y, value)

    c.setFont("Helvetica", 12)
    for skill in character.skills:
        if skill in skill_positions:
            x, y = skill_positions[skill]
            c.drawString(x, y, "•")  # Přidáme tečku
    ""

    "Traits"
    c.setFont("Helvetica-Bold", 10)
    traits_x = 412  # X souřadnice
    traits_y = 394  # Začátek seznamu vlastností
    # ✅ Vykreslení traits (vlastností)
    for trait in character.set_traits():
        description = trait_descriptions.get(trait, "Neznámá vlastnost.")  
        wrapped_text = textwrap.wrap(f"• {trait}: {description}", width=30)  # Zalamování textu
        c.setFont("Helvetica", 9)
        for line in wrapped_text:
            c.drawString(traits_x, traits_y, line)
            traits_y -= 10  # Posun dolů pro další řádek
    ""
    
    "Stats+"
    c.setFont("Helvetica", 13)
    x_pos = 47
    x_val = 50
    for stat, y in stats_positions.items():
        value = character.stats.get(stat, 10)
        bonus = calculate_stat_bonus(value)
        bonus_str = f"+{bonus}" if bonus >= 0 else f"{bonus}"
        c.drawString(x_val, y, f"{value}")
        c.drawString(x_pos, y - 27, f"{bonus_str}")  
    ""

    "Prof bonus"
    prof_bonus = "+2"
    c.drawString(99, 610, f"{prof_bonus}")
    ""
    
    "Inventory"
    c.drawString(267, 191, "Inventory:")
    item_y = 181
    for item in character.inventory:
        c.setFont("Helvetica", 7)
        wrapped_item = textwrap.wrap(item.describe(), width=40)
        for line in wrapped_item:
            c.drawString(267, item_y, line)
            item_y -= 10
        item_y -= 5
    for weapon in character.inventory:
        if isinstance(weapon, Weapon):
            c.drawString(329,392 , f"{weapon.damage}")
            c.drawString(235, 392, f"{weapon.name}")
    c.setFont("Helvetica", 15)
    ac_value = set_ac(character)  # Calculate the armor class once
    if any(isinstance(item, Armor) for item in character.inventory):
        for armor in character.inventory:
            if isinstance(armor, Armor):
                c.drawString(238, 636, f"{ac_value}")
    else:
        c.drawString(238, 636, f"{ac_value}")  # Display AC even if no armor is in inventory
    ""   

    "Spells"
    c.showPage()
    c.showPage()
    spellcasting_classes = ["Warlock", "Wizard", "Cleric", "Druid", "Bard", "Sorcerer", "Paladin", "Ranger"]
    if character.char_class.name in spellcasting_classes:
        spell_ability_map = {
            "Warlock": "Charisma",
            "Wizard": "Intelligence",
            "Cleric": "Wisdom",
            "Druid": "Wisdom",
            "Bard": "Charisma",
            "Sorcerer": "Charisma",
            "Paladin": "Charisma",
            "Ranger": "Wisdom",
        }
        spellcasting_stat = spell_ability_map.get(character.char_class.name, "Charisma")
        spell_save_dc = 8 + character.stats.get("Proficiency Bonus", 2) + calculate_stat_bonus(character.stats.get(spellcasting_stat, 0))
        spell_attack_bonus = spell_save_dc - 8

        c.setFont("Helvetica-Bold", 13)
        c.drawString(46, 710, f"{character.char_class.name}")
        c.drawString(285, 720, f"{spellcasting_stat}")
        c.drawString(385, 720, f": {spell_save_dc}")
        c.drawString(490, 720, f": {spell_attack_bonus}")

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
        c.setFont("Helvetica-Bold", 14)
    c.save()
    with open(input_pdf, "rb") as base_pdf_file, open(overlay_pdf, "rb") as overlay_file:
        base_pdf = PyPDF2.PdfReader(base_pdf_file)
        overlay = PyPDF2.PdfReader(overlay_file)
        writer = PyPDF2.PdfWriter()
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
fill_character_sheet("/Users/user/DNDGEN/DndGEN/dnd/dnd_character_sheet.pdf", "character_sheet_filled.pdf", character, class_spell_slots[character.char_class.name])


