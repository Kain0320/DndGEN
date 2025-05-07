from base import races, Class, backgrounds, Character, classes, hit_dice, names, skill_positions, trait_descriptions, spells_by_class, class_spell_slots, spells_descriptions, cantripps_descriptions, saving_throw_positions, class_items, class_saving_throws, Weapon, Armor, potions_list, magic_items_list, path_classy, stats_positions, stat_skills, stats_names
import random
import textwrap
from functools import partial
import PyPDF2
import os
from customtkinter import *
import customtkinter as ctk
import tkinter as tk
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageTk
import json

"Gui pro bazove charackteristiky"
def choose_option_gui(options, title="Vyber možnost"):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    ctk.set_widget_scaling(1.0)

    root = ctk.CTk()
    root.title(title)
    root.geometry("400x530")
    root.resizable(False, False)

    chosen = {"object": None}
    already_selected = [False]

    if isinstance(options, dict):
        display_list = list(options.values())
    else:
        display_list = options

    def select(btn, option):
       if not already_selected[0]:
         already_selected[0] = True
         chosen["object"] = option
         btn.configure(fg_color="green", text="✅ Vybráno")

         
         def safe_close():
             try:
                 root.quit()
             except:
                 pass

         root.after(300, safe_close)


    frame = ctk.CTkScrollableFrame(root)
    frame.pack(expand=True, fill="both", pady=10, padx=10)

    for option in display_list:
        name = option.name if hasattr(option, "name") else str(option)
        btn = ctk.CTkButton(frame, text=name, width=300)
        btn.configure(command=partial(select, btn, option))
        btn.pack(pady=5)

    def random_select():
     if not already_selected[0]:
         already_selected[0] = True
         chosen["object"] = random.choice(display_list)

         def safe_close():
             try:
                root.quit()
             except:
                 pass

         root.after(300, safe_close)

    ctk.CTkButton(root, text="🎲 Náhodně", width=300, command=random_select).pack(pady=10)

    try:
        root.mainloop()
    except Exception as e:
        if any(x in str(e) for x in ["click_animation", "dpi_scaling", "update"]):
            print("⚠️ Potlačená systémová chyba:", e)
        else:
            raise
    finally:
        try:
            root.destroy()
        except:
            pass

    return chosen["object"] or random.choice(display_list)


def choose_gender_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Vyber pohlaví")
    root.geometry("300x200")

    gender = ctk.StringVar()

    def select(btn,value):
        btn.configure(fg_color="green", text="✅ Vybráno")
        root.after(300, lambda: finish(value))

    def finish(value):
        gender.set(value)
        root.destroy()

    ctk.CTkLabel(root, text="Zvol pohlaví:", font=("Arial", 16)).pack(pady=10)

    btn_m = ctk.CTkButton(root, text="Muž")
    btn_m.configure(command=lambda: select(btn_m, "Muž"))
    btn_m.pack(pady=5)

    btn_f = ctk.CTkButton(root, text="Žena")
    btn_f.configure(command=lambda: select(btn_f, "Žena"))
    btn_f.pack(pady=5)

    btn_r = ctk.CTkButton(root, text="🎲 Náhodně")
    btn_r.configure(command=lambda: select(btn_r, random.choice(["Muž", "Žena"])))
    btn_r.pack(pady=10)

    try:
        root.mainloop()
    except Exception as e:
        if "click_animation" in str(e) or "dpi_scaling" in str(e):
            print("⚠️ Potlačená systémová chyba:", e)
        else:
            raise

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

def roll_single_stat_animation(label, callback):
    roll_cycles = random.randint(10, 20)  # kolik krát čísla "točit"
    rolls = []

    def animate(cycle=0):
        nonlocal rolls
        rolls = [random.randint(1, 6) for _ in range(4)]
        label.configure(text=f"🎲 {rolls}")
        if cycle < roll_cycles:
            label.after(50, lambda: animate(cycle + 1))
        else:
            rolls.remove(min(rolls))
            total = sum(rolls)
            callback(total)

    animate()

def generate_stats_gui_with_spin_and_build_selection(char_class_name=None):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("🎲 Kostky")
    root.geometry("300x460")

    label_title = ctk.CTkLabel(root, text="🎲 Hazeni kostky", font=("Arial", 20))
    label_title.pack(pady=10)

    stat_labels = []
    stat_values = []

    for stat in stats_names:
        frame = ctk.CTkFrame(root)
        frame.pack(pady=5)

        lbl = ctk.CTkLabel(frame, text=f"⏳", font=("Arial", 16))
        lbl.pack()
        stat_labels.append(lbl)

    def start_roll():
        stat_values.clear()

        def roll_next(index=0):
            if index < len(stat_labels):
                roll_single_stat_animation(stat_labels[index], lambda val: finish_stat(val, index))
            else:
                finalize()

        def finish_stat(val, index):
            stat_labels[index].configure(text=f"{val}")
            stat_values.append((stats_names[index], val))
            roll_next(index + 1)

        def finalize():
            roll_button.configure(state="disabled")
            

        roll_next()
    
    def clean_close():
        root.after(200, root.destroy)

    roll_button = ctk.CTkButton(root, text="🎲 Hoď kostky!", command=start_roll)
    roll_button.pack(pady=20)

    ctk.CTkButton(root, text="✅ Potvrdit a Zavřít", command=clean_close).pack(pady=10)


    try:
        root.mainloop()
    except Exception as e:
        if "click_animation" in str(e) or "dpi_scaling" in str(e):
            print("⚠️ Potlačená systémová chyba:", e)
        else:
            raise

    return stat_values

# ⚔️ PRIORITY podle classu
CLASS_PRIORITIES = {
    "Fighter": ["Strength", "Constitution", "Dexterity", "Wisdom", "Intelligence", "Charisma"],
    "Wizard": ["Intelligence", "Constitution", "Dexterity", "Wisdom", "Charisma", "Strength"],
    "Rogue": ["Dexterity", "Intelligence", "Charisma", "Constitution", "Wisdom", "Strength"],
    "Cleric": ["Wisdom", "Constitution", "Strength", "Charisma", "Dexterity", "Intelligence"],
    "Barbarian": ["Strength", "Constitution", "Dexterity", "Wisdom", "Charisma", "Intelligence"],
    "Sorcerer": ["Charisma", "Constitution", "Dexterity", "Wisdom", "Intelligence", "Strength"],
    "Paladin": ["Strength", "Charisma", "Constitution", "Wisdom", "Dexterity", "Intelligence"],
    "Ranger": ["Dexterity", "Wisdom", "Constitution", "Strength", "Charisma", "Intelligence"],
    "Druid": ["Wisdom", "Constitution", "Dexterity", "Intelligence", "Charisma", "Strength"],
    "Warlock": ["Charisma", "Constitution", "Dexterity", "Wisdom", "Intelligence", "Strength"],
    "Monk": ["Dexterity", "Wisdom", "Constitution", "Charisma", "Intelligence", "Strength"],
    "Bard": ["Charisma", "Dexterity", "Constitution", "Wisdom", "Intelligence", "Strength"],
    
}

def assign_stats_gui(char_class_name):
    stats = generate_stats_gui_with_spin_and_build_selection(char_class_name)
    available_values = sorted([val for _, val in stats], reverse=True)

    priorities = CLASS_PRIORITIES.get(char_class_name, ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"])
    stat_names = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title(f"✍️ Přidělení statů pro {char_class_name}")
    root.geometry("300x400")

    ctk.CTkLabel(root, text="📜 Vyber, jak chceš staty přiřadit:", font=("Arial", 16)).pack(pady=10)

    method_var = ctk.StringVar(value="auto")

    def choose_auto():
        method_var.set("auto")
        root.after(200, root.quit)

    def choose_manual():
        method_var.set("manual")
        root.after(200, root.quit)

    def choose_point_buy():
        method_var.set("point_buy")
        root.after(200, root.quit)

    ctk.CTkButton(root, text="🎲 Automaticky podle classy", command=choose_auto).pack(pady=5)
    ctk.CTkButton(root, text="✍️ Manuálně přidělit staty", command=choose_manual).pack(pady=5)
    ctk.CTkButton(root, text="📊 Point Buy (27 bodů)", command=choose_point_buy).pack(pady=5)

    root.mainloop()
    root.destroy()

    selected_method = method_var.get()

    # 1️⃣ AUTO – jako dřív
    if selected_method == "auto":
        assignments = {priority: available_values[i] for i, priority in enumerate(priorities)}
        return assignments

    # 2️⃣ MANUÁL
    elif selected_method == "manual":
        return manual_assign_gui(stat_names, available_values)

    # 3️⃣ POINT BUY
    elif selected_method == "point_buy":
        return open_point_buy_gui()

    # fallback
    return {stat: 10 for stat in stat_names}

def manual_assign_gui(stat_names, values):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Manuální přidělení statů")
    root.geometry("500x600")

    assignments = {}
    dropdowns = {}

    for stat in stat_names:
        frame = ctk.CTkFrame(root)
        frame.pack(pady=5)
        ctk.CTkLabel(frame, text=stat, width=100).pack(side="left", padx=5)

        var = ctk.StringVar(value=str(values[0]))
        dropdown = ctk.CTkOptionMenu(frame, values=[str(v) for v in values], variable=var)
        dropdown.pack(side="left")
        dropdowns[stat] = var

    error_label = ctk.CTkLabel(root, text="", text_color="red")
    error_label.pack()

    def confirm():
        chosen = [v.get() for v in dropdowns.values()]
        if sorted(map(int, chosen)) != sorted(values):
            error_label.configure(text="❌ Staty musí být jedinečné a použít všechny hodnoty.")
        else:
            for stat in stat_names:
                assignments[stat] = int(dropdowns[stat].get())
            root.after(200, root.quit)

    ctk.CTkButton(root, text="✅ Potvrdit", command=confirm).pack(pady=20)
    root.mainloop()
    root.destroy()
    return assignments
STAT_NAMES = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
MAX_POINTS = 27
POINT_BUY_COST = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
def calculate_total_cost(stats):
    return sum(POINT_BUY_COST[val] for val in stats.values())
def open_point_buy_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("🧠 Point Buy systém")
    root.geometry("500x600")

    stats = {stat: 8 for stat in STAT_NAMES}
    stat_labels = {}
    remaining_points_label = ctk.CTkLabel(root, text="", font=("Arial", 16))
    remaining_points_label.pack(pady=10)

    def update_display():
        total_cost = calculate_total_cost(stats)
        remaining = MAX_POINTS - total_cost
        remaining_points_label.configure(text=f"Zbývá bodů: {remaining}")
        for stat in STAT_NAMES:
            val = stats[stat]
            cost = POINT_BUY_COST.get(val, "❌")
            stat_labels[stat].configure(text=f"{stat}: {val} (náklady: {cost})")

    def increase(stat):
        if stats[stat] < 15:
            new_val = stats[stat] + 1
            if calculate_total_cost({**stats, stat: new_val}) <= MAX_POINTS:
                stats[stat] = new_val
                update_display()

    def decrease(stat):
        if stats[stat] > 8:
            stats[stat] -= 1
            update_display()

    for stat in STAT_NAMES:
        frame = ctk.CTkFrame(root)
        frame.pack(pady=5)

        btn_dec = ctk.CTkButton(frame, text="➖", width=40, command=lambda s=stat: decrease(s))
        btn_dec.pack(side="left", padx=5)

        label = ctk.CTkLabel(frame, text="", font=("Arial", 16), width=250)
        label.pack(side="left", padx=5)
        stat_labels[stat] = label

        btn_inc = ctk.CTkButton(frame, text="➕", width=40, command=lambda s=stat: increase(s))
        btn_inc.pack(side="left", padx=5)

    update_display()

    def confirm():
        root.selected_stats = stats.copy()
        root.after(200, root.quit)

    ctk.CTkButton(root, text="✅ Potvrdit", command=confirm).pack(pady=20)
    root.mainloop()
    root.destroy()

    return getattr(root, "selected_stats", None)

def select_spells_gui(char_class):
    class_name = char_class.name
    spell_data = spells_by_class.get(class_name, {})
    spell_limits = class_spell_slots.get(class_name, {"cantrips": 0, "spells": 0})

    selected = {"cantrips": [], "spells": []}

    def select_from_list(spell_list, limit, spell_type):
        root = ctk.CTk()
        root.title(f"Vyber {spell_type} ({limit}) pro {class_name}")
        root.geometry("1480x800")

        selected_local = []
        images = {}
        buttons = {}
        frame = ctk.CTkFrame(root)
        frame.pack(expand=True, fill="both")

        canvas = ctk.CTkCanvas(frame, width=1400, height=750)
        scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        def toggle(spell_name):
            if spell_name in selected_local:
                selected_local.remove(spell_name)
                buttons[spell_name].configure(fg_color="gray")
            elif len(selected_local) < limit:
                selected_local.append(spell_name)
                buttons[spell_name].configure(fg_color="green")

        columns = 4
        for index, spell_name in enumerate(spell_list):
            folder = "cantrips" if spell_type.lower() == "cantrips" else "spells"
            spell_path = os.path.join("/Users/user/DNDGEN/DndGEN/dnd/spell_images", folder, spell_name.replace(" ", "_") + ".png")
            frame_inner = ctk.CTkFrame(scrollable_frame, corner_radius=10)
            row = index // columns
            col = index % columns
            frame_inner.grid(row=row, column=col, padx=10, pady=10)

            try:
                img = Image.open(spell_path).resize((350, 450))
                img_ctk = ctk.CTkImage(light_image=img, size=(350, 450))
                images[spell_name] = img_ctk
                ctk.CTkLabel(frame_inner, image=img_ctk, text="").pack()
            except:
                ctk.CTkLabel(frame_inner, text=f"{spell_name} (bez obrázku)").pack()

            btn = ctk.CTkButton(frame_inner, text=spell_name, command=lambda name=spell_name: toggle(name))
            btn.pack(pady=5)
            buttons[spell_name] = btn

        def confirm_selection():
            if len(selected_local) < limit:
                ctk.CTkMessagebox.show_error("Chyba", f"Musíte vybrat alespoň {limit} položek.")
            else:
                root.after(200, lambda: root.destroy())

        ctk.CTkButton(root, text="✅ Potvrdit", command=confirm_selection).pack(pady=10)
        try:
            root.mainloop()
        except Exception as e:
            if "click_animation" in str(e) or "dpi_scaling" in str(e):
                print("⚠️ Potlačená systémová chyba:", e)
            else:
                raise
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

def choose_portrait_gui(race, gender):
    portraits_dir = "/Users/user/DNDGEN/DndGEN/dnd/portraits"
    race_name = getattr(race, "name", str(race))
    gender_dir = os.path.join(portraits_dir, race_name, gender)

    if not os.path.exists(gender_dir):
        print(f"❌ Složka pro {race_name} a {gender} neexistuje.")
        return None

    portrait_files = [f for f in os.listdir(gender_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not portrait_files:
        print(f"❌ Žádné portréty nenalezeny pro {race_name} a {gender}.")
        return None

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.geometry("650x670")
    root.title(f"Výběr portrétu pro {race_name} ({gender})")
    index = ctk.IntVar(value=0)
    image_label = ctk.CTkLabel(root, text="")
    image_label.pack(pady=10)

    image_cache = {}

    def update_image():
        img_path = os.path.join(gender_dir, portrait_files[index.get()])
        try:
            pil_img = Image.open(img_path).convert("RGBA").resize((500, 600))
            ctk_img = ctk.CTkImage(light_image=pil_img, size=(500, 600))
            image_cache["img"] = ctk_img
            root.ctk_img = ctk_img
            image_label.configure(image=ctk_img, text="")
        except Exception as e:
            print(f"❌ Chyba při načítání obrázku: {e}")
            image_label.configure(text="⚠️ Nelze načíst obrázek.", image=None)

    def next_image():
        index.set((index.get() + 1) % len(portrait_files))
        update_image()

    def prev_image():
        index.set((index.get() - 1) % len(portrait_files))
        update_image()

    def select_image():
        root.selected_portrait = os.path.join(gender_dir, portrait_files[index.get()])
        root.after(100, root.destroy)

    def select_random():
        root.selected_portrait = os.path.join(gender_dir, random.choice(portrait_files))
        root.after(200, root.destroy)

    # Buttons
    frame = ctk.CTkFrame(root)
    frame.pack(pady=10)

    ctk.CTkButton(frame, text="⬅️ Předchozí", command=prev_image).pack(side="left", padx=10)
    ctk.CTkButton(frame, text="✅ Vybrat", command=select_image).pack(side="left", padx=10)
    ctk.CTkButton(frame, text="🎲 Náhodně", command=select_random).pack(side="left", padx=10)
    ctk.CTkButton(frame, text="➡️ Další", command=next_image).pack(side="left", padx=10)

    update_image()
    root.mainloop()

    return getattr(root, "selected_portrait", None)

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

    root = ctk.CTk()
    root.title("Zadej nebo vyber jméno")
    root.geometry("400x200")
    chosen = ctk.StringVar()
    def select(btn, option):
            btn.configure(fg_color="green", text="✅ Vybráno")
            root.after(300, lambda: finish(option))

    def finish(option):
            chosen.set(option)
            root.after(200, root.destroy)  # ukončí mainloop

    entry = ctk.CTkEntry(root, placeholder_text="Zadej vlastní jméno")
    entry.pack(pady=10)

    def confirm_entry():
        name = entry.get()
        if name.strip():
            finish(name)
        else:
            finish(random.choice(name_list))

    ctk.CTkButton(root, text="✅ Potvrdit  jméno", command=confirm_entry).pack(pady=5)

    # Náhodně vybrané jméno (zobrazení)
    random_name_label = ctk.CTkLabel(root, text="", font=("Arial", 16))
    random_name_label.pack(pady=5)

    def show_random_name():
        random_name = random.choice(name_list)
        random_name_label.configure(text=random_name)
        entry.delete(0, tk.END)        # Vymaže pole
        entry.insert(0, random_name)   # Vloží náhodné jméno do entry

    ctk.CTkButton(root, text="🎲 Náhodné jméno", width=300, command=show_random_name).pack(pady=10)

    # Scroll seznam existujících jmen
    frame = ctk.CTkScrollableFrame(root)
    frame.pack(expand=True, fill="both", pady=10, padx=10)

    for name in name_list:
        btn = ctk.CTkButton(frame, text=name, width=300)
        btn.configure(command=lambda n=name, b=btn: select(b, n))
        btn.pack(pady=5)

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
    race_key = choose_option_gui(list(races.keys()), "Vyber rasu:")  # hráč vybírá jméno (text)
    race = races[race_key]
    char_class = choose_option_gui(classes, "Vyber povolání:")
    background = choose_option_gui(backgrounds, "Vyber zázemí:")
    gender = choose_gender_gui()
    name = generate_name_gui(race, gender)
    portrait = choose_portrait_gui(race, gender)
    stats = assign_stats_gui(char_class.name)
    stats_dict = dict(stats)
    stats_with_race = race.apply_modifiers(stats_dict) 
    skills = []  # Initialize skills
    traits = []  # Initialize traits
    character = Character( name, race, char_class, background, hit_dice, skills, traits, generate_items= generate_items)
    character.stats = stats_with_race
    constitution_mod = character.stats.get("Constitution", 0)  # Modifikátor Constitution
    character.hit_dice, character.hp = calculate_hit_points(char_class, constitution_mod)
    skills = character.set_skills()
    traits = character.set_traits()
    character.spells = select_spells_gui(char_class)
    char_class.apply_class_bonus(character)
    character.path = generate_path(char_class.name) if char_class.name in path_classy else None
    character.portrait = portrait # Replace with a valid default path
    return character

def display_character_info(character):
     info_window = ctk.CTkToplevel()
     info_window.title(f"Informace o postavě - {character.name}")
     info_window.geometry("700x400")
     info_window.resizable(True, True)
     text_box = ctk.CTkTextbox(info_window, width=550, height=350, font=("Arial", 14))
     text_box.pack(pady=10)
     inventory_names = [item.name if hasattr(item, "name") else str(item) for item in character.inventory]
     character_info = (
                f"=== VYTVOŘENÁ POSTAVA ===\n"
                f"Jméno: {character.name}\n"
                f"Rasa: {character.race.name if hasattr(character.race, 'name') else str(character.race)}\n"
                f"Povolání: {character.char_class.name if hasattr(character.char_class, 'name') else str(character.char_class)}\n"
                f"Zázemí: {character.background.name if hasattr(character.background, 'name') else str(character.background)}\n"
                f"HP: {character.hp}\n"
                f"Hit Dice: {character.hit_dice}\n"
                f"Skills: {character.skills}\n"
                f"Traits: {character.trait}\n"
                f"Spells: {character.spells}\n"
                f"Inventory: {inventory_names}\n"
                f"AC: {set_ac(character)}\n"
                f"Features: {character.features}\n"
                f"Path: {character.path}\n"
                f"Stats: {character.stats}\n"
            )

     text_box.insert("1.0", character_info)
     text_box.configure(state="disabled")  # Disable editing

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

def open_character_journal(character):
    journal_window = ctk.CTkToplevel()
    journal_window.title(f"Deník postavy - {character.name}")
    journal_window.geometry("600x700")
    journal_window.resizable(True, True)

    text_box = ctk.CTkTextbox(journal_window, width=550, height=600, font=("Arial", 14))
    text_box.pack(pady=10)

    # 📝 Cesta k souboru
    journal_path = f"/Users/user/DNDGEN/DndGEN/dnd/journals/{character.name}_journal.txt"
    os.makedirs("journals", exist_ok=True)

    # 🔵 Funkce pro načtení
    def load_journal():
        if os.path.exists(journal_path):
            with open(journal_path, "r", encoding="utf-8") as f:
                content = f.read()
                text_box.delete("1.0", "end")
                text_box.insert("1.0", content)

    # 🔵 Funkce pro uložení
    def save_journal():
        with open(journal_path, "w", encoding="utf-8") as f:
            f.write(text_box.get("1.0", "end"))
        print(f"✅ Deník postavy {character.name} uložen!")

    # 🔵 Tlačítka
    button_frame = ctk.CTkFrame(journal_window)
    button_frame.pack(pady=5)

    ctk.CTkButton(button_frame, text="💾 Uložit", command=save_journal).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="🔄 Načíst", command=load_journal).pack(side="left", padx=5)

def save_character_to_json(character, filename):
    """Uloží charakter do JSON souboru."""
    character_data = {
        "name": character.name,
        "race": character.race.name if hasattr(character.race, "name") else str(character.race),
        "class": character.char_class.name if hasattr(character.char_class, "name") else str(character.char_class),
        "background": character.background.name if hasattr(character.background, "name") else str(character.background),
        "stats": character.stats,
        "skills": character.skills,
        "traits": character.trait,
        "spells": character.spells,
        "inventory": [item.name if hasattr(item, "name") else str(item) for item in character.inventory],
        "hp": character.hp,
        "hit_dice": character.hit_dice,
        "portrait": character.portrait,
        "path": character.path
    }
    with open(filename, "w") as f:
        json.dump(character_data, f, indent=4)
    print(f"✅ Postava {character.name} byla uložena do {filename}!")

def show_character_options(character):
    root = ctk.CTk()
    root.title(f"Možnosti pro {character.name}")
    root.geometry("250x200")
    # Tlačítko pro zobrazení deníku
    ctk.CTkButton(root, text="📜 Zobrazit informace", command=lambda: display_character_info(character)).pack(pady=10)

    ctk.CTkButton(root, text="📝 Zobraz historii postavy", command=lambda: open_character_journal(character)).pack(pady=10)
    
    # Třeba i tlačítko na export do PDF
    ctk.CTkButton(root, text="📜 Exportovat do PDF", command=lambda: (fill_character_sheet("/Users/user/DNDGEN/DndGEN/dnd/dnd_character_sheet.pdf", "character_sheet_filled.pdf", character, class_spell_slots[character.char_class.name]))).pack(pady=10)
    
    ctk.CTkButton(root, text="💬Exportovat do JSON", command=lambda: (save_character_to_json(character, "my_character.json"))).pack(pady=10)

    ctk.CTkButton(root, text="❌ Zavřít generator", command=root.destroy).pack(pady=10)
    root.mainloop()

character = generate_character()
show_character_options(character)






