import random

class Character:
    def __init__(self, name, race, char_class, background,hit_dice, skills=None,traits=None):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.background = background
        self.stats = self.generate_stats()
        self.stats = self.race.apply_modifiers(self.stats)  # Aplikuje bonusy rasy
        self.hit_dice = hit_dice[char_class.name]
        self.max_hp = random.randint(1, int(self.hit_dice[0]))  
        self.skills = self.set_skills()
        self.trait = self.set_traits()

    def set_skills(self):
        """Spojí dovednosti z rasy, povolání a zázemí do jednoho seznamu."""
        background_skills = self.background.skills if isinstance(self.background.skills, list) else [self.background.skills]
        class_skills = self.char_class.skills if isinstance(self.char_class.skills, list) else [self.char_class.skills]
        return  background_skills + class_skills
    
    def set_traits(self):
        race_traits = self.race.traits if isinstance(self.race.traits, list) else [self.race.traits]
        
        return race_traits

                                                                                                     
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

    def __str__(self):
        """Vrací statblock postavy jako text."""
        stats = "\n".join(f"{key}: {value}" for key, value in self.stats.items())
        return f"Name: {self.name}\nRace: {self.race.name}\nClass: {self.char_class.name}\nBackground: {self.background.name}\nStats:\n{stats}"
    class Race:
        def __init__(self, name, stat_modifiers, traits=[]):
            self.name = name
            self.stat_modifiers = stat_modifiers  # Bonusy k atributům (např. {"Strength": +2})
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
    "Human": Character.Race("Human", {"All": +1},["Versatile"]),
    "Elf": Character.Race("Elf", {"Dexterity": +2},["Darkvision", "Fey Ancestry"]),
    "Dwarf": Character.Race("Dwarf", {"Constitution": +2},["Darkvision", "Dwarven Resilience"]),
    "Halfling": Character.Race("Halfling", {"Dexterity": +2}, ["Lucky", "Brave"]),
    "Kabold": Character.Race("Kabold", {"Strength": -2, "Dexterity": +2},["Darkvision", "Pack Tactics"]),
    "Gith": Character.Race("Gith", {"Intelligence": +1}, ["Telepathy", "Githyanki Weapon Training"]),
    "Tiefling": Character.Race("Tiefling", {"Charisma": +2}, ["Darkvision", "Hellish Resistance"]),
    "Dragonborn": Character.Race("Dragonborn", {"Strength": +2}, ["Draconic Ancestry", "Breath Weapon"]),
    "Gnome": Character.Race("Gnome", {"Intelligence": +2},["Darkvision", "Gnome Cunning"]),
}
class Class:
    def __init__(self, name, hit_dice, starting_equipment, spellcasting=None, skills=[]):
        self.name = name
        self.hit_dice = hit_dice  # Např. "1d10"
        self.skills = skills  # Seznam dovedností pro povolání
        self.starting_equipment = starting_equipment  # Počáteční vybavení
        self.spellcasting = spellcasting  # Seznam kouzel pro castery (může být None)
classes = {
    "Fighter": Class("Fighter", "1d10", ["Longsword", "Shield"], None, ["Athletics", "Intimidation"]),
    "Wizard": Class("Wizard", "1d6", ["Dagger", "Spellbook",], ["Fire Bolt", "Mage Hand"], ["Arcana", "History"]),
    "Rogue": Class("Rogue", "1d8", ["Dagger", "Thieves' Tools"], None, ["Stealth", "Deception"]),
    "Cleric": Class("Cleric", "1d8", ["Mace", "Holy Symbol"], ["Cure Wounds", "Sacred Flame"], ["Medicine", "Insight"]),
    "Bard": Class("Bard", "1d8", ["Rapier", "Lute"], ["Vicious Mockery", "Healing Word"], ["Performance", "Persuasion"]),
    "Ranger": Class("Ranger", "1d10", ["Longbow", "Arrows"], None, ["Survival", "Animal Handling"]),
    "Barbarian": Class("Barbarian", "1d12", ["Greataxe"], None, ["Athletics", "Intimidation"]),
    "Sorcerer": Class("Sorcerer", "1d6", ["Dagger"], ["Fire Bolt", "Mage Hand"], ["Arcana", "Persuasion"]),
    "Monk": Class("Monk", "1d8", ["Shortsword"], None, ["Acrobatics", "Religion"]),
    "Paladin": Class("Paladin", "1d10", ["Longsword", "Shield"], None, ["Religion", "Persuasion"]),
    "Druid": Class("Druid", "1d8", ["Wooden Shield", "Scimitar"], ["Druidcraft", "Produce Flame"], ["Nature", "Medicine"]),
    "Warlock": Class("Warlock", "1d8", ["Dagger"], ["Eldritch Blast", "Mage Hand"], ["Arcana", "Deception"]),
}
class Background:
    def __init__(self, name, starting_equipment, feature,skills=[]):
        self.name = name
        self.skills = skills
        self.starting_equipment = starting_equipment
        self.feature = feature  # Speciální schopnost zázemí 
backgrounds = {
    "Noble": Background("Noble", ["Fine Clothes", "Signet Ring"], "Position of Privilege",["History", "Persuasion"]),
    "Soldier": Background("Soldier",["Military Gear", "Playing Cards"], "Military Rank", ["Athletics", "Intimidation"]),
    "Criminal": Background("Criminal",["Crowbar", "Dark Clothes"], ["Criminal Contact"], ["Stealth", "Deception"]),
    "Sage": Background("Sage",["Ink and Quill", "Scrolls"], "Researcher", ["Arcana", "History"]),
    "Acolyte": Background("Acolyte", ["Holy Symbol", "Prayer Book"], "Shelter of the Faithful", ["Insight", "Religion"]),
    "Entertainer": Background("Entertainer", ["Musical Instrument", "Costume"], "By Popular Demand", ["Performance", "Acrobatics"]),
    "Folk Hero": Background("Folk Hero", ["Rustic Gear", "Shovel"], "Rustic Hospitality", ["Animal Handling", "Survival"]),
    "Guild Artisan": Background("Guild Artisan", ["Artisan Tools", "Letter of Introduction"], "Guild Membership",["Insight", "Persuasion"]),
    "Hermit": Background("Hermit", ["Scrolls", "Herbalism Kit"], "Discovery",["Medicine", "Religion"]),
    "Outlander": Background("Outlander",["Staff", "Hunting Trap"], "Wanderer",["Athletics", "Survival"]),
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
        "Nature": (102, 326),
        "Perception": (102, 308),
        "Performance": (102, 300),
        "Persuasion": (102, 286),
        "Religion": (102, 273),
        "Sleight of Hand": (102, 257),
        "Stealth": (102, 246),
        "Survival": (102, 233)
    }


