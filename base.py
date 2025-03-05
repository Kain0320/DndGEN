import random

class Character:
    def __init__(self, name, race, char_class, background):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.background = background
        self.stats = self.generate_stats()
        self.stats = self.race.apply_modifiers(self.stats)  # Aplikuje bonusy rasy
        self.inventory = self.generate_inventory()
        self.skills = self.set_skills()
        self.hit_dice = hit_dice[char_class.name]
        self.max_hp = random.randint(1, int(self.hit_dice[0]))  

    def generate_stats(self):
        """Generuje šest hlavních atributů (hod kostkami 4k6, nejnižší se zahodí)."""
        def roll_stat():
            rolls = [random.randint(1, 6) for _ in range(4)]
            return sum(sorted(rolls)[1:])  # Sečte 3 nejvyšší hody

        return {
            "Strength": roll_stat(),
            "Dexterity": roll_stat(),
            "Constitution": roll_stat(),
            "Intelligence": roll_stat(),
            "Wisdom": roll_stat(),
            "Charisma": roll_stat(),
        }

    def generate_inventory(self):
        """Přidá základní vybavení podle povolání a zázemí."""
        return self.char_class.starting_equipment + self.background.starting_equipment

    def set_skills(self):
        """Nastaví dovednosti na základě rasy, povolání a zázemí."""
        return self.race.skills + self.char_class.skills + self.background.skills

    def __str__(self):
        """Vrací statblock postavy jako text."""
        stats = "\n".join(f"{key}: {value}" for key, value in self.stats.items())
        return f"Name: {self.name}\nRace: {self.race.name}\nClass: {self.char_class.name}\nBackground: {self.background.name}\nStats:\n{stats}"
    class Race:
        def __init__(self, name, stat_modifiers, skills=[], traits=[]):
            self.name = name
            self.stat_modifiers = stat_modifiers  # Bonusy k atributům (např. {"Strength": +2})
            self.skills = skills  # Seznam dovedností získaných díky rase
            self.traits = traits  # Speciální schopnosti rasy
        
        def apply_modifiers(self, stats):
            """Aplikuje bonusy k atributům postavy."""
            for stat, bonus in self.stat_modifiers.items():
                if stat == "All":
                    for key in stats.keys():
                        stats[key] += bonus
                else:
                    stats[stat] += bonus
            return stats

races = {
    "Human": Character.Race("Human", {"All": +1}, [], ["Versatile"]),
    "Elf": Character.Race("Elf", {"Dexterity": +2}, ["Perception"], ["Darkvision", "Fey Ancestry"]),
    "Dwarf": Character.Race("Dwarf", {"Constitution": +2}, ["Smith's Tools"], ["Darkvision", "Dwarven Resilience"]),
    "Halfling": Character.Race("Halfling", {"Dexterity": +2}, ["Stealth"], ["Lucky", "Brave"]),
    "Kabold": Character.Race("Kabold", {"Strength": -2, "Dexterity": +2}, ["Sneak"], ["Darkvision", "Pack Tactics"]),
    "Gith": Character.Race("Gith", {"Intelligence": +1}, ["Survival"], ["Telepathy", "Githyanki Weapon Training"]),
    "Tiefling": Character.Race("Tiefling", {"Charisma": +2}, ["Intimidation"], ["Darkvision", "Hellish Resistance"]),
    "Dragonborn": Character.Race("Dragonborn", {"Strength": +2}, ["Intimidation"], ["Draconic Ancestry", "Breath Weapon"]),
    "Gnome": Character.Race("Gnome", {"Intelligence": +2}, ["Arcana"], ["Darkvision", "Gnome Cunning"]),
}
class Class:
    def __init__(self, name, hit_dice, skills, starting_equipment, spellcasting=None):
        self.name = name
        self.hit_dice = hit_dice  # Např. "1d10"
        self.skills = skills  # Seznam dovedností, které povolání dává
        self.starting_equipment = starting_equipment  # Počáteční vybavení
        self.spellcasting = spellcasting  # Seznam kouzel pro castery (může být None)
classes = {
    "Fighter": Class("Fighter", "1d10", ["Athletics", "Intimidation"], ["Longsword", "Shield"]),
    "Wizard": Class("Wizard", "1d6", ["Arcana", "History"], ["Spellbook", "Dagger"], ["Fire Bolt", "Mage Hand"]),
    "Rogue": Class("Rogue", "1d8", ["Stealth", "Deception"], ["Dagger", "Thieves' Tools"]),
    "Cleric": Class("Cleric", "1d8", ["Medicine", "Insight"], ["Mace", "Holy Symbol"], ["Cure Wounds", "Sacred Flame"]),
    "Bard": Class("Bard", "1d8", ["Performance", "Persuasion"], ["Rapier", "Lute"], ["Vicious Mockery", "Healing Word"]),
    "Ranger": Class("Ranger", "1d10", ["Survival", "Animal Handling"], ["Longbow", "Arrows"]),
    "Barbarian": Class("Barbarian", "1d12", ["Athletics", "Intimidation"], ["Greataxe"]),
    "Sorcerer": Class("Sorcerer", "1d6", ["Arcana", "Persuasion"], ["Dagger"], ["Fire Bolt", "Mage Hand"]),
    "Monk": Class("Monk", "1d8", ["Acrobatics", "Religion"], ["Shortsword"]),
    "Paladin": Class("Paladin", "1d10", ["Religion", "Persuasion"], ["Longsword", "Shield"]),
    "Druid": Class("Druid", "1d8", ["Nature", "Medicine"], ["Wooden Shield", "Scimitar"], ["Druidcraft", "Produce Flame"]),
    "Warlock": Class("Warlock", "1d8", ["Arcana", "Deception"], ["Dagger"], ["Eldritch Blast", "Mage Hand"]),
}
class Background:
    def __init__(self, name, starting_equipment, feature, skills=[], traits=[]):
        self.name = name
        self.skills = skills
        self.starting_equipment = starting_equipment
        self.feature = feature  # Speciální schopnost zázemí 
        self.traits = traits  # Speciální vlastnosti zázemí 
backgrounds = {
    "Noble": Background("Noble", ["History", "Persuasion"], ["Fine Clothes", "Signet Ring"], "Position of Privilege"),
    "Soldier": Background("Soldier", ["Athletics", "Intimidation"], ["Military Gear", "Playing Cards"], "Military Rank"),
    "Criminal": Background("Criminal", ["Stealth", "Deception"], ["Crowbar", "Dark Clothes"], "Criminal Contact"),
    "Sage": Background("Sage", ["Arcana", "History"], ["Ink and Quill", "Scrolls"], "Researcher"),
    "Acolyte": Background("Acolyte", ["Insight", "Religion"], ["Holy Symbol", "Prayer Book"], "Shelter of the Faithful"),
    "Entertainer": Background("Entertainer", ["Performance", "Acrobatics"], ["Musical Instrument", "Costume"], "By Popular Demand"),
    "Folk Hero": Background("Folk Hero", ["Animal Handling", "Survival"], ["Rustic Gear", "Shovel"], "Rustic Hospitality"),
    "Guild Artisan": Background("Guild Artisan", ["Insight", "Persuasion"], ["Artisan Tools", "Letter of Introduction"], "Guild Membership"),
    "Hermit": Background("Hermit", ["Medicine", "Religion"], ["Scrolls", "Herbalism Kit"], "Discovery"),
    "Outlander": Background("Outlander", ["Athletics", "Survival"], ["Staff", "Hunting Trap"], "Wanderer"),
}
hit_dice = {
    "Fighter": "1d10",
    "Wizard": "1d6",
    "Rogue": "1d8",
    "Cleric": "1d8",
    "Bard": "1d8",
    "Ranger": "1d10",
    "Barbarian": "1d12",
    "Sorcerer": "1d6",
    "Monk": "1d8",
    "Paladin": "1d10",
    "Druid": "1d8",
    "Warlock": "1d8",
}
names = {
    "Elf": {"Muž": ["Aerendil", "Thalion", "Legolas"], "Žena": ["Arwen", "Lúthien", "Galadriel"]},
    "Dwarf": {"Muž": ["Thorin", "Balin"], "Žena": ["Dis", "Tana"]},
    "Human": {"Muž": ["Aragorn", "Boromir"], "Žena": ["Eowyn", "Elanor"]},
    "Halfling": {"Muž": ["Frodo", "Bilbo"], "Žena": ["Rosie", "Daisy"]},
    "Kabold": {"Muž": ["Poro", "Koro"], "Žena": ["Saassraa", "Zaassraa"]},
    "Gith": {"Muž": ["Zerthimon", "Vlaak"], "Žena": ["Vlaakith", "Layzel"]},
    "Tiefling": {"Muž": ["Morthos", "Kael"], "Žena": ["Lilith", "Morrigan"]},
    "Dragonborn": {"Muž": ["Bahamut", "Korvax"], "Žena": ["Andarna", "Vey"]},
    "Gnome": {"Muž": ["Rurik", "Boddynock"], "Žena": ["Bimpnottin", "Breena"]}
}
def set_skills(self):
    """Sloučí dovednosti z rasy, povolání a zázemí do jednoho seznamu."""
    # Ověření, zda skills je seznam, pokud ne, vytvoří seznam z jednotlivých dovedností
    race_skills = self.race.skills if isinstance(self.race.skills, list) else [self.race.skills]
    class_skills = self.char_class.skills if isinstance(self.char_class.skills, list) else [self.char_class.skills]
    background_skills = self.background.skills if isinstance(self.background.skills, list) else [self.background.skills]

    # Spojí všechny dovednosti do jednoho seznamu
    return race_skills + class_skills + background_skills

