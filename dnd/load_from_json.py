from base import races, Class, backgrounds, Character, classes, hit_dice
import json

def load_character_from_json(filename):
    """Načte charakter z JSON souboru."""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Teď musíme z dat udělat znovu Character objekt
    race = next((r for r in races if getattr(r, "name", None) == data["race"]), data["race"])
    char_class = next((c for c in classes if getattr(c, "name", None) == data["class"]), data["class"])
    background = next((b for b in backgrounds if getattr(b, "name", None) == data["background"]), None)

    character = Character(
        name=data["name"],
        race=races[data["race"]],  
        char_class=classes[data["class"]],
        background=backgrounds[data["background"]],
        hit_dice=hit_dice,
        skills=data["skills"],
        traits=data["traits"],
        generate_items=lambda x: []
    )

    # Přidáme další data
    character.stats = data["stats"]
    character.spells = data["spells"]
    character.inventory = data["inventory"]  # POZOR: tady budou jen názvy, ne objekty Weapon/Armor
    character.hp = data["hp"]
    character.portrait = data.get("portrait", None)
    character.path = data.get("path", None)

    print(f"✅ Postava {character.name} byla načtena z {filename}!")
    return character

character_json = load_character_from_json("my_character.json")
