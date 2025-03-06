import random

class Character:
    def __init__(self, name, race, char_class, background,hit_dice, skills=None,traits=None, char_spells=None):
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
        self.char_spells= char_spells
    
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
    def __init__(self, name, hit_dice, starting_equipment,skills=[]):
        self.name = name
        self.hit_dice = hit_dice  # Např. "1d10"
        self.skills = skills  # Seznam dovedností pro povolání
        self.starting_equipment = starting_equipment  # Počáteční vybavení
       
classes = {
    "Fighter": Class("Fighter", "1d10", ["Longsword", "Shield"], ["Athletics", "Intimidation"]),
    "Wizard": Class("Wizard", "1d6", ["Dagger", "Spellbook"], ["Arcana", "History"]),
    "Rogue": Class("Rogue", "1d8", ["Dagger", "Thieves' Tools"],["Stealth", "Deception"]),
    "Cleric": Class("Cleric", "1d8", ["Mace", "Holy Symbol"],["Medicine", "Insight"]),
    "Bard": Class("Bard", "1d8", ["Rapier", "Lute"], ["Performance", "Persuasion"]),
    "Ranger": Class("Ranger", "1d10", ["Longbow", "Arrows"], ["Survival", "Animal Handling"]),
    "Barbarian": Class("Barbarian", "1d12", ["Greataxe"], ["Athletics", "Intimidation"]),
    "Sorcerer": Class("Sorcerer", "1d6", ["Dagger"],["Arcana", "Persuasion"]),
    "Monk": Class("Monk", "1d8", ["Shortsword"],["Acrobatics", "Religion"]),
    "Paladin": Class("Paladin", "1d10", ["Longsword", "Shield"],["Religion", "Persuasion"]),
    "Druid": Class("Druid", "1d8", ["Wooden Shield", "Scimitar"], ["Nature", "Medicine"]),
    "Warlock": Class("Warlock", "1d8", ["Dagger"],["Arcana", "Deception"]),
}
spells_by_class = {
    "Wizard": ["Magic Missile", "Fireball", "Shield"],
    "Cleric": ["Cure Wounds", "Bless", "Guiding Bolt", "Healing Word", 
               "Detect Magic", "Spiritual Weapon", "Sacred Flame", "Protection from Evil and Good"],
    "Sorcerer": ["Fire Bolt", "Mage Hand", "Shield", "Mage Armor", "Burning Hands",
                 "Magic Missile", "Chromatic Orb", "Counterspell", "Detect Magic"],
    "Bard": ["Vicious Mockery", "Healing Word", "Charm Person", "Disguise Self", 
             "Dissonant Whispers", "Tasha's Hideous Laughter", "Cure Wounds", "Faerie Fire", "Heroism"],
    "Warlock": ["Eldritch Blast", "Mage Hand", "Hex", "Armor of Agathys", "Shield",
                "Hellish Rebuke", "Detect Magic", "Burning Hands", "Darkness"],
    "Druid": ["Druidcraft", "Produce Flame", "Healing Word", "Entangle", "Thorn Whip",
              "Faerie Fire", "Goodberry", "Cure Wounds", "Moonbeam", "Barkskin"],
    "Paladin": ["Bless", "Shield", "Cure Wounds", "Divine Smite", "Wrathful Smite"]
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
trait_descriptions = {
    "Versatile": "Humans gain a +1 bonus to all attributes.",
    "Darkvision": "Can see in darkness up to 60 feet, but only in grayscale.",
    "Fey Ancestry": "Advantage against being charmed, immune to magical sleep.",
    "Dwarven Resilience": "Advantage on saving throws against poison, resistance to poison damage.",
    "Lucky": "When rolling a natural 1 on a d20, you can reroll the die.",
    "Brave": "Advantage on saving throws against fear.",
    "Pack Tactics": "Advantage on attack rolls if an ally is within 5 feet.",
    "Telepathy": "Can communicate telepathically within 30 feet.",
    "Githyanki Weapon Training": "Proficiency with longswords, shortswords, and light crossbows.",
    "Hellish Resistance": "Resistance to fire damage.",
    "Draconic Ancestry": "A draconic lineage grants special abilities.",
    "Breath Weapon": "Exhales a breath attack that deals elemental damage.",
    "Gnome Cunning": "Advantage on saving throws against magic that affects Intelligence, Wisdom, or Charisma."
}
spells_descriptions = {
    "Fire Bolt": "A beam of fire shoots toward a creature, dealing 1d10 fire damage on a hit.",
    "Mage Hand": "Creates a spectral hand that can manipulate objects. It can't attack, open doors, or carry more than 10 pounds.",
    "Cure Wounds": "A creature you touch regains hit points equal to 1d8 + your spellcasting modifier.",
    "Magic Missile": "Creates darts of magical force that hit automatically, dealing 1d4 + 1 force damage each.",
    "Bless": "You bless up to three creatures of your choice, granting them a 1d4 bonus to attack rolls and saving throws for up to 1 minute.",
    "Shield": "A magical force surrounds you, granting +5 AC for 1 round and negating Magic Missile's damage.",
    "Vicious Mockery": "You unleash a string of insults. The target must succeed on a Wisdom saving throw or take 1d4 psychic damage and have disadvantage on its next attack roll.",
    "Healing Word": "A creature of your choice within 60 feet regains hit points equal to 1d4 + your spellcasting modifier.",
    "Druidcraft": "You create a tiny, harmless sensory effect, such as changing the color of flowers or creating a puff of wind. No damage.",
    "Produce Flame": "You create a flame in your hand. You can throw it at a creature within 30 feet, dealing 1d8 fire damage on a hit.",
    "Hunter's Mark": "You choose a creature within 90 feet. The target takes an extra 1d6 damage from your weapon attacks.",
    "Burning Hands": "A cone of fire erupts from your hands, dealing 3d6 fire damage to creatures in a 15-foot cone (Dex save for half).",
    "Detect Magic": "You sense the presence of magic within 30 feet of you for 10 minutes.",
    "Sleep": "You put creatures within a 20-foot radius to sleep. The total hit points of creatures affected can't exceed 5d8.",
    "Mage Armor": "You touch a willing creature and protect them with magical armor, giving them 13 + Dexterity modifier AC for 8 hours.",
    "Chromatic Orb": "You create an orb of energy (choose acid, cold, fire, lightning, poison, or thunder), dealing 3d8 damage of the chosen type on a hit.",
    "Guiding Bolt": "A flash of light streaks toward a creature, dealing 4d6 radiant damage on a hit and granting advantage on the next attack roll against the target.",
    "Spiritual Weapon": "You create a floating, magical weapon that strikes at your enemies, dealing 1d8 + your spellcasting modifier force damage.",
    "Sacred Flame": "A flame-like radiance descends upon a creature, dealing 1d8 radiant damage (Dex save for half).",
    "Protection from Evil and Good": "You protect a creature from certain creatures and types of attacks, giving them advantage on certain saving throws.",
    "Charm Person": "You attempt to charm a humanoid within range. It must succeed on a Wisdom saving throw or be charmed for 1 hour.",
    "Disguise Self": "You alter your appearance, including clothing and weapons, for up to 1 hour.",
    "Dissonant Whispers": "You whisper a discordant melody that only the target can hear, dealing 3d6 psychic damage. The target must also flee as far as possible.",
    "Tasha's Hideous Laughter": "You cause a creature to fall into fits of laughter. The target must succeed on a Wisdom saving throw or be incapacitated and unable to take actions for 1 minute.",
    "Hex": "You curse a creature, giving you advantage on attack rolls against it and causing it to take an extra 1d6 necrotic damage from your attacks.",
    "Armor of Agathys": "You surround yourself with magical frost, granting 5 temporary hit points. Any creature that hits you takes 5 cold damage.",
    "Hellish Rebuke": "You retaliate with a fiery blast when damaged by a creature, dealing 2d10 fire damage to the attacker (Dex save for half).",
    "Entangle": "You cause plants to grow and ensnare creatures in the area, restraining them. A creature must succeed on a Strength saving throw or be restrained.",
    "Thorn Whip": "You create a magical vine to lash out at a creature, dealing 1d6 piercing damage and pulling the target up to 10 feet closer.",
    "Faerie Fire": "You outline creatures in light, granting advantage to attack rolls against them for 1 minute.",
    "Goodberry": "You create up to 10 magical berries that each restore 1 hit point when consumed.",
    "Moonbeam": "A silvery beam of light shines down on a creature, dealing 2d10 radiant damage (Constitution save for half).",
    "Barkskin": "You toughen the target's skin, granting them a minimum AC of 16 for up to 1 hour.",
    "Divine Smite": "You channel divine energy to deal extra radiant damage on a successful melee hit. The damage is 2d8 for a first-level spell slot, plus 1d8 for each level higher.",
    "Wrathful Smite": "You imbue your weapon with thunderous power, dealing 1d6 thunder damage and potentially frightening the target (Wisdom save to resist).",
    "Lay on Hands": "You can heal a creature by touch, restoring a number of hit points equal to your Paladin level (maximum 5 times per long rest).",
    "Thunderous Smite": "You imbue your weapon with thunderous power, dealing 2d6 thunder damage and knocking back your target (Strength save to resist).",
    "Absorb Elements": "You capture some of the incoming energy from an elemental attack, reducing damage by 1d6 (up to 3d6 at higher levels).",
    "Spike Growth": "You cause the ground in an area to become covered in sharp thorns, dealing 2d4 piercing damage to creatures that move through it."
}





