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

def generate_character():
    """Vygeneruje postavu podle výběru uživatele nebo náhodně."""
    print("\n=== GENERÁTOR POSTAV D&D 5E ===\n")

    race = choose_option(races, "Vyber rasu:")
    char_class = choose_option(classes, "Vyber povolání:")
    background = choose_option(backgrounds, "Vyber zázemí:")

    # Náhodné jméno (jen placeholder, může se vylepšit)
    name = random.choice(["Sylva", "Dain", "Eldrin", "Xaden", "Mira", "Lilith", "Violet", " Quyet", "Tropos" ])

    character = Character(name, race, char_class, background)

    print("\n=== VYTVOŘENÁ POSTAVA ===")
    print(character)

# Spuštění generátoru
generate_character()
