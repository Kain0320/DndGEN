import random
class Character:
    def __init__(self, name, race, char_class, background,hit_dice, skills=None,traits=None, char_spells=None,inventory=None, generate_items=None):
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
        self.inventory = generate_items(self.char_class.name)
        self.features = []  # Initialize features as an empty list
        
        
        
    
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

        stats = [roll_stat() for _ in range(6)]
        stats.sort(reverse=True)  
        primary_atributes = {
        "Fighter": ["Strength", "Constitution"],
        "Wizard": ["Intelligence", "Dexterity"],
        "Rogue": ["Dexterity", "Charisma"],
        "Cleric": ["Wisdom", "Strength"],
        "Bard": ["Charisma", "Dexterity"],
        "Ranger": ["Dexterity", "Wisdom"],
        "Barbarian": ["Strength", "Constitution"],
        "Sorcerer": ["Charisma", "Constitution"],
        "Monk": ["Dexterity", "Wisdom"],
        "Paladin": ["Strength", "Charisma"],
        "Druid": ["Wisdom", "Constitution"],
        "Warlock": ["Charisma", "Wisdom"],
        }
        class_name = self.char_class.name
        primary = primary_atributes.get(class_name, [])
        attributes = {"Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"}
        stats_dict = {attr:0 for attr in attributes}
        for attr in primary:
            stats_dict[attr] = stats.pop(0)
        for attr in attributes:
            if stats_dict[attr] == 0:
                stats_dict[attr] = stats.pop(0)
        return stats_dict
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
    
    def apply_class_bonus(self, character):
        """Aplikuje unikátní bonusy podle třídy."""
        if self.name == "Barbarian":
            dex_bonus = (character.stats.get("Dexterity", 10) - 10) // 2
            con_bonus = (character.stats.get("Constitution", 10) - 10) // 2
            character.ac = 10 + dex_bonus + con_bonus
            character.features.append("Unarmored Defense: AC = 10 + Dex + Con"),("Rage -  (2/day)")

        elif self.name == "Monk":
            dex_bonus = (character.stats.get("Dexterity", 10) - 10) // 2
            wis_bonus = (character.stats.get("Wisdom", 10) - 10) // 2
            character.ac = 10 + dex_bonus + wis_bonus
            character.features.append("Unarmored Defense: AC = 10 + Dex + Wis"), 
            character.features.append("Martial Arts (1d6 unarmed attacks, bonus attack(bonus action) after attack with weapon)")

        elif self.name == "Rogue":
            character.features.append("Sneak Attack: +1d6 extra damage, when attacking with advantage")
            character.features.append("Thieves' Cant: Secret language known only to rogues")

        elif self.name == "Fighter":
            fighting_styles = ["Defense", "Archery", "Dueling", "Great Weapon Fighting", "Protection", "Two-Weapon Fighting"]
            chosen_style = random.choice(fighting_styles)
            character.features.append(f"Fighting Style: {chosen_style})")
            character.features.append("Second Wind (regain 1d10+1 h.p.)")

        elif self.name == "Wizard":
            character.features.append("Arcane Recovery: Recover spell slots after a short rest")

        elif self.name == "Paladin":
            character.features.append("Divine Sense: Detect celestial, fiend, and undead within 60ft"),
            character.features.append("Lay on Hands: Heal 5x Paladin level HP once per day")

        elif self.name == "Druid":
            character.features.append("Druidic Language: Secret language known only to druids"),
            character.features.append("Wild Shape: Transform into a beast")

        elif self.name == "Ranger":
            character.features.append("Favored Enemy: Gain advantage on survival checks vs chosen enemy")

        elif self.name == "Sorcerer":
            character.features.append("Font of Magic: Gain sorcery points for metamagic")

        elif self.name == "Bard":
            character.features.append("Bardic Inspiration: Grant 1d6 bonus to an ally’s roll")

        elif self.name == "Cleric":
            character.features.append("Divine Domain: Gain extra spells based on chosen deity")

        elif self.name == "Warlock":
            character.features.append("Pact Magic: Unique spellcasting system based on patron’s power")
path_classy = {
    "Cleric": ["Life Domain", "Death Domain", "Knowledge Domain", "Nature Domain"],
    "Wizard": ["Evocation", "Conjuration", "Necromancy", "Abjuration"]
}
       
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
    "Wizard": {
        "cantrips": ["Mage Hand", "Fire Bolt", "Prestidigitation", "Ray of Frost", "Minor Illusion", "Message", "Light"],
        "spells": ["Magic Missile", "Shield", "Mage Armor", "Burning Hands", "Detect Magic", "Identify", "Feather Fall", "Chromatic Orb", "Sleep", "Thunderwave"]
    },
    "Cleric": {
        "cantrips": ["Sacred Flame", "Thaumaturgy", "Guidance", "Spare the Dying", "Light", "Resistance"],
        "spells": ["Cure Wounds", "Bless", "Guiding Bolt", "Healing Word", "Detect Magic", "Protection from Evil and Good", "Inflict Wounds", "Command", "Sanctuary", "Create Water"]
    },
    "Sorcerer": {
        "cantrips": ["Fire Bolt", "Mage Hand", "Ray of Frost", "Minor Illusion", "Message", "Shocking Grasp", "Acid Splash"],
        "spells": ["Shield", "Mage Armor", "Magic Missile", "Burning Hands", "Chromatic Orb", "Thunderwave", "Expeditious Retreat", "Witch Bolt", "Disguise Self"]
    },
    "Bard": {
        "cantrips": ["Vicious Mockery", "Mage Hand", "Prestidigitation", "Message", "Dancing Lights", "Light"],
        "spells": ["Healing Word", "Charm Person", "Disguise Self", "Dissonant Whispers", "Tasha's Hideous Laughter", "Faerie Fire", "Sleep", "Identify", "Unseen Servant", "Silent Image"]
    },
    "Warlock": {
        "cantrips": ["Eldritch Blast", "Mage Hand", "Thaumaturgy", "Minor Illusion", "Chill Touch", "Friends"],
        "spells": ["Hex", "Armor of Agathys", "Shield", "Hellish Rebuke", "Detect Magic", "Witch Bolt", "Cause Fear", "Expeditious Retreat"]
    },
    "Druid": {
        "cantrips": ["Druidcraft", "Produce Flame", "Thorn Whip", "Guidance", "Shillelagh", "Mending"],
        "spells": ["Healing Word", "Entangle", "Faerie Fire", "Goodberry", "Cure Wounds", "Speak with Animals", "Thunderwave", "Create Water"]
    },
    "Paladin": {
        "cantrips": [],  # Paladin nemá cantripy
        "spells": ["Bless", "Shield", "Cure Wounds", "Divine Smite", "Wrathful Smite", "Heroism", "Compelled Duel", "Thunderous Smite", "Detect Evil and Good"]
    },
    "Ranger": {
        "cantrips": [],  # Ranger nemá cantripy
        "spells": ["Hunter's Mark", "Cure Wounds", "Detect Magic", "Ensnaring Strike", "Longstrider", "Jump", "Goodberry", "Fog Cloud", "Alarm"]
    }
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
        "Athletics": (102, 421),
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
class_spell_slots = {
    "Wizard": {"cantrips": 3, "spells": 6},
    "Cleric": {"cantrips": 3, "spells": 5},
    "Druid": {"cantrips": 2, "spells": 4},
    "Sorcerer": {"cantrips": 4, "spells": 2},
    "Warlock": {"cantrips": 2, "spells": 2},
    "Bard": {"cantrips": 2, "spells": 4},
    "Paladin": {"cantrips": 0, "spells": 2},
    "Ranger": {"cantrips": 0, "spells": 2},
    "Barbarian": {"cantrips": 0, "spells": 0},
    "Monk": {"cantrips": 0, "spells": 0},
    "Rogue": {"cantrips": 0, "spells": 0},
    "Fighter": {"cantrips": 0, "spells": 0}
}
spells_descriptions = {
    # ✅ 1ST-LEVEL SPELLS
    "Magic Missile": "Creates darts of magical force that hit automatically, dealing 1d4 + 1 force damage each.",
    "Shield": "A magical force surrounds you, granting +5 AC for 1 round.",
    "Mage Armor": "You touch a willing creature and protect them with magical armor, giving them 13 + Dexterity modifier AC for 8 hours.",
    "Burning Hands": "A cone of fire erupts from your hands, dealing 3d6 fire damage to creatures in a 15-foot cone (Dex save for half).",
    "Cure Wounds": "A creature you touch regains hit points equal to 1d8 + your spellcasting modifier.",
    "Healing Word": "A creature of your choice within 60 feet regains hit points equal to 1d4 + your spellcasting modifier.",
    "Bless": "You bless up to three creatures of your choice, granting them a 1d4 bonus to attack rolls and saving throws for up to 1 minute.",
    "Guiding Bolt": "A flash of light streaks toward a creature, dealing 4d6 radiant damage on a hit and granting advantage on the next attack roll against the target.",
    "Protection from Evil and Good": "You protect a creature from certain creatures and types of attacks, giving them advantage on certain saving throws.",
    "Hunter's Mark": "You choose a creature within 90 feet. The target takes an extra 1d6 damage from your weapon attacks.",
    "Detect Magic": "You sense the presence of magic within 30 feet of you for 10 minutes.",
    "Entangle": "You cause plants to grow and ensnare creatures in the area, restraining them. A creature must succeed on a Strength saving throw or be restrained.",
    "Faerie Fire": "You outline creatures in light, granting advantage to attack rolls against them for 1 minute.",
    "Goodberry": "You create up to 10 magical berries that each restore 1 hit point when consumed.",
    "Divine Smite": "You channel divine energy to deal extra radiant damage on a successful melee hit. The damage is 2d8 for a first-level spell slot, plus 1d8 for each level higher.",
    "Wrathful Smite": "You imbue your weapon with divine power, dealing 1d6 psychic damage and potentially frightening the target (Wisdom save to resist).",
    "Thunderwave": "A wave of force erupts from you, dealing 2d8 thunder damage to creatures within 15 feet (Con save for half).",
    "Sleep": "You put creatures in a 20-foot radius to sleep. Affects creatures with the lowest hit points first.",
    "Feather Fall": "Slows the fall of up to five creatures, preventing fall damage.",
    "Identify": "You touch an object and learn its magical properties.",
    "Command": "You speak a one-word command to a creature, which it must obey on its next turn.",
    "Sanctuary": "You ward a creature against attack. Enemies must make a Wisdom save to attack it.",
    "Create Water": "You create 10 gallons of clean water in an open container or cause rain.",
    "Chromatic Orb": "You throw an orb of energy (acid, cold, fire, lightning, poison, or thunder), dealing 3d8 damage of the chosen type.",
    "Witch Bolt": "You create a sustained arc of lightning that deals 1d12 damage and remains connected for up to 1 minute.",
    "Disguise Self": "You alter your appearance for up to 1 hour.",
    "Dissonant Whispers": "You whisper a melody that causes a creature to flee in fear, taking 3d6 psychic damage.",
    "Tasha's Hideous Laughter": "A creature falls into fits of laughter, becoming incapacitated for up to 1 minute (Wis save ends).",
    "Heroism": "A willing creature gains temporary hit points and becomes immune to fear.",
    "Compelled Duel": "You force a creature to duel you. It must make a Wisdom save or only attack you.",
    "Thunderous Smite": "Your next melee attack deals extra 2d6 thunder damage and can push the target away (Strength save to resist).",
    "Expeditious Retreat": "You gain the ability to take the Dash action as a bonus action for up to 10 minutes.",
    "Fog Cloud": "You create a 20-foot-radius sphere of fog that heavily obscures the area.",
    "Alarm": "You create a magical alarm that alerts you when a creature enters an area.",
    "Hex": "You curse a creature. You deal an extra 1d6 necrotic damage to the target each time you hit it with an attack.",
    "Armor of Agathys": "You gain temporary hit points and deal cold damage to attackers.",
    "Hellish Rebuke": "You retaliate against a creature that damages you, dealing 2d10 fire damage.",
    "Detect Evil and Good": "You sense aberrations, celestials, elementals, fey, fiends, or undead within 30 feet of you.",
    "Cause Fear": "You cause a creature to become frightened of you for up to 1 minute (Wis save to resist).",
}
cantripps_descriptions = {
    "Fire Bolt": "A beam of fire shoots toward a creature, dealing 1d10 fire damage on a hit.",
    "Mage Hand": "Creates a spectral hand that can manipulate objects. It can't attack, open doors, or carry more than 10 pounds.",
    "Vicious Mockery": "You unleash a string of insults. The target must succeed on a Wisdom saving throw or take 1d4 psychic damage and have disadvantage on its next attack roll.",
    "Druidcraft": "You create a tiny, harmless sensory effect, such as changing the color of flowers or creating a puff of wind. No damage.",
    "Produce Flame": "You create a flame in your hand. You can throw it at a creature within 30 feet, dealing 1d8 fire damage on a hit.",
    "Sacred Flame": "A flame-like radiance descends upon a creature, dealing 1d8 radiant damage (Dex save for half).",
    "Thaumaturgy": "You create a supernatural effect such as making your voice boom, flames flicker, or doors fly open. No damage.",
    "Guidance": "You touch a creature, giving them a +1d4 bonus to a single ability check within the next minute.",
    "Prestidigitation": "A minor magical trick that creates small sensory effects, cleans or soils objects, lights candles, or chills/warms nonliving material.",
    "Ray of Frost": "A frigid beam of blue-white light strikes a creature, dealing 1d8 cold damage and reducing its speed by 10 feet until your next turn.",
    "Eldritch Blast": "A beam of crackling energy strikes a creature, dealing 1d10 force damage on a hit.",
    "Toll the Dead": "A creature hears a haunting bell. If it has missing hit points, it takes 1d12 necrotic damage (otherwise 1d8).",
    "Shillelagh": "You imbue a wooden weapon with magic. It deals 1d8 damage and uses your spellcasting ability for attack rolls.",
    "Thorn Whip": "You create a magical vine to lash out at a creature, dealing 1d6 piercing damage and pulling the target up to 10 feet closer.",
    "Minor Illusion": "You create a sound or an image within range that lasts up to 1 minute.",
    "Message": "You whisper a message to a target within 120 feet, and only they can hear the reply.",
    "Light": "You touch an object, making it shine bright light for 20 feet and dim light for another 20 feet.",
    "Chill Touch": "You create a ghostly skeletal hand that deals 1d8 necrotic damage and prevents healing until your next turn.",
    "Friends": "For 1 minute, you have advantage on Charisma checks against a target, but they become hostile afterward.",
    "Dancing Lights": "You create up to four floating lights that illuminate an area.",
    "Mending": "You repair a broken object, restoring up to 1 foot of damage.",

}

class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value
    def describe(self):
        return f"{self.name} - Weight: {self.weight} lbs, Value: {self.value} gp"    
class Weapon(Item):
    def __init__(self, name, weight, value, damage, weapon_type, reach=False):
        super().__init__(name, weight, value)
        self.damage = damage
        self.weapon_type = weapon_type  # Např. "melee", "ranged"
        self.reach = reach  # True, pokud má zbraň delší dosah
    def __str__(self):
        return f"{self.name} ({self.damage})"
    def describe(self):
        reach_text = " (Reach)" if self.reach else ""
        return f"{self.name} (Weapon) - {self.damage} damage, Type: {self.weapon_type}{reach_text}, Weight: {self.weight} lbs, Value: {self.value} gp"
class Armor(Item):
    def __init__(self, name, weight, value, ac, armor_type):
        super().__init__(name, weight, value)
        self.ac = ac
        self.armor_type = armor_type  # "light", "medium", "heavy"
    def __str__(self):
        return f"{self.name} ({self.armor_class})"

    def describe(self):
        return f"{self.name} (Armor) - AC: {self.ac}, Type: {self.armor_type}, Weight: {self.weight} lbs, Value: {self.value} gp"
class Potion(Item):
    def __init__(self, name, value, effect):
        super().__init__(name, 0.5, value)  # Většina lektvarů je lehká
        self.effect = effect
    def describe(self):
        return f"{self.name} (Potion) - Effect: {self.effect}, Value: {self.value} gp"
    def __str__(self):
        return f"{self.name} ({self.effect})"
class MagicItem(Item):
    def __init__(self, name, weight, value, special_effect):
        super().__init__(name, weight, value)
        self.special_effect = special_effect
    def __str__(self):
        return f"{self.name} ({self.effect})"
    def describe(self):
        return f"{self.name} (Magic Item) - Effect: {self.special_effect}, Weight: {self.weight} lbs, Value: {self.value} gp"
class_items = {
    "Fighter": {
        "weapons": [Weapon("Longsword", 3, 15, "1d8 slashing", "melee"), Weapon("Greatsword", 6, 50, "2d6 slashing", "melee")],
        "armor": [Armor("Chainmail", 20, 75, 16, "medium"), Armor("Plate", 65, 1500, 18, "heavy")]
    },
    "Wizard": {
        "weapons": [Weapon("Dagger", 1, 2, "1d4 piercing", "melee"), Weapon("Quarterstaff", 4, 0.2, "1d6 bludgeoning", "melee")],
        "armor": []
    },
    "Rogue": {
        "weapons": [Weapon("Dagger", 1, 2, "1d4 piercing", "melee"), Weapon("Shortsword", 2, 10, "1d6 piercing", "melee")],
        "armor": [Armor("Leather", 10, 10, 11, "light")]
    },
    "Cleric": {
        "weapons": [Weapon("Mace", 4, 5, "1d6 bludgeoning", "melee"), Weapon("Warhammer", 2, 15, "1d8 bludgeoning", "melee")],
        "armor": [Armor("Chainmail", 20, 75, 16, "medium")]
    },
    "Bard": {
        "weapons": [Weapon("Rapier", 2, 25, "1d8 piercing", "melee"), Weapon("Shortsword", 2, 10, "1d6 piercing", "melee")],
        "armor": [Armor("Leather", 10, 10, 11, "light")]
    },
    "Ranger": {
        "weapons": [Weapon("Longbow", 2, 50, "1d8 piercing", "ranged"), Weapon("Shortsword", 2, 10, "1d6 piercing", "melee")],
        "armor": [Armor("Leather", 10, 10, 11, "light"), Armor("Studded Leather", 13, 45, 12, "light")]
    },
    "Barbarian": {
        "weapons": [Weapon("Greataxe", 7, 30, "1d12 slashing", "melee"), Weapon("Handaxe", 2, 5, "1d6 slashing", "melee")],
        "armor": []
    },
    "Sorcerer": {
        "weapons": [Weapon("Dagger", 1, 2, "1d4 piercing", "melee"), Weapon("Quarterstaff", 4, 0.2, "1d6 bludgeoning", "melee")],
        "armor": []
    },
    "Monk": {
        "weapons": [Weapon("Shortsword", 2, 10, "1d6 piercing", "melee"), Weapon("Quarterstaff", 4, 0.2, "1d6 bludgeoning", "melee")],
        "armor": []
    },
    "Paladin": {
        "weapons": [Weapon("Longsword", 3, 15, "1d8 slashing", "melee"), Weapon("Warhammer", 2, 15, "1d8 bludgeoning", "melee")],
        "armor": [Armor("Chainmail", 20, 75, 16, "medium"), Armor("Shield", 6, 10, 2, "shield")]
    },
    "Druid": {
        "weapons": [Weapon("Scimitar", 3, 25, "1d6 slashing", "melee"), Weapon("Quarterstaff", 4, 0.2, "1d6 bludgeoning", "melee")],
        "armor": [Armor("Leather", 10, 10, 11, "light"), Armor("Hide", 12, 10, 12, "medium")]
    },
    "Warlock": {
        "weapons": [Weapon("Dagger", 1, 2, "1d4 piercing", "melee"), Weapon("Quarterstaff", 4, 0.2, "1d6 bludgeoning", "melee")],
        "armor": [Armor("Leather", 10, 10, 11, "light")]
    }
}
potions_list = [
    Potion("Healing Potion",  10 , "Restores 2d4+2 HP",),
    Potion("Antidote", 10, "Cures one poison effect"),
    Potion("Potion of Climbing",10, "Advantage on climbing checks for 1 hour"),
    Potion("Potion of Resistance",10, "Resist one random damage type for 10 min"),
    Potion("Potion of Night Vision",10, "Gain darkvision (18m) for 1 hour"),   
]
magic_items_list = [
    MagicItem("Amulet of Protection", 0.5, 20, "+1 AC for 1 hour"),
    MagicItem("Ring of Minor Invisibility",0.1,35, "Turn invisible for 1 minute (1/day)"),
    MagicItem("Wand of Sparks",0.2,20, "Shoot a small electric bolt (1d4 lightning, 3/day)"),
    MagicItem("Feather Token",0.1, 25, "Activate Feather Fall once per day"),
    MagicItem("Ring of Mind Read ",0.1,300, "Read surface thoughts of a creature (1/day)"),
]



