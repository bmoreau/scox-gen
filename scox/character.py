#! /usr/bin/env python3

import scox.value as value
import scox.profile as profile

class Character(profile.Profile):
    """Base class for representing characters in scox.
    
    A character is defined as a set of values, ordered by lists depending on
    their types: a list of attributes, a list of skills, a list of powers and a
    list of mandatory values.

    Instance variables:
    level -- Level of the character in his / her hierarchy (default 0).
    name -- Name of the character.
    nature -- Nature of the character; either 'Angel' or 'Demon'.
    notes -- Speak your mind freely.
    side_values -- Map of additional character defining values.
    superior -- Hierarchical superior of the character.

    Methods:
    apply_profile -- Apply the modifications listed in an input profile.
    init_attributes -- Initialize the character's attributes.
    init_skills -- Initialize the character's skills.
    init_values -- Initialize the character's attributes.
    update_values -- Update the base ranks of the skills listed in
        skill attributes and the values of self.side_values using the current
        ranks of self.attributes.
    """

    def __init__(self, name, level=0, nature='Demon'):
        """Constructor.

        Arguments:
        name -- Name of the new character.

        Keyword arguments:
        level -- Level of the new character (default 0).
        nature -- Nature of the new character (default 'Demon').
        """
        profile.Profile.__init__(self)
        self.name = name
        self.level = level
        self.nature = nature
        self.superior = None
        self.init_attributes()
        self.init_skills()
        self.init_values()
        self.update_values()

    def init_attributes(self):
        """Initialize the character's attributes."""
        self.attributes["Force"] = value.Attribute(4)
        self.attributes["Agilite"] = value.Attribute(4)
        self.attributes["Perception"] = value.Attribute(4)
        self.attributes["Volonte"] = value.Attribute(4)
        self.attributes["Presence"] = value.Attribute(4)
        self.attributes["Foi"] = value.Attribute(4)

    def init_skills(self):
        """Initialize the character's skills."""
        # Primary skills
        self.primary_skills["Baratin"] = value.Skill(
            governing_attribute=self.attributes["Presence"])
        self.primary_skills["Combat"] = value.Skill(
            governing_attribute=self.attributes["Agilite"],
            specific=True)
        self.primary_skills["CaC"] = value.Skill(
            governing_attribute=self.attributes["Agilite"])
        self.primary_skills["Defense"] = value.Skill(
            governing_attribute=self.attributes["Agilite"])
        self.primary_skills["Discretion"] = value.Skill(
            governing_attribute=self.attributes["Agilite"])
        self.primary_skills["Discussion"] = value.Skill(
            governing_attribute=self.attributes["Volonte"])
        self.primary_skills["Enquete"] = value.Skill(
            governing_attribute=self.attributes["Foi"])
        self.primary_skills["Fouille"] = value.Skill(
            governing_attribute=self.attributes["Perception"])
        self.primary_skills["Intrusion"] = value.Skill(acquired=True)
        self.primary_skills["Medecine"] = value.Skill(acquired=True)
        self.primary_skills["Seduction"] = value.Skill(
            governing_attribute=self.attributes["Presence"])
        self.primary_skills["Tir"] = value.Skill(
            governing_attribute=self.attributes["Perception"],
            specific=True)
        # Exotic skills
        self.exotic_skills["Contorsionnisme"] = value.Skill(
            governing_attribute=self.attributes["Agilite"], acquired=True)
        self.exotic_skills["Humour"] = value.Skill(acquired=True)
        self.exotic_skills["Hypnotisme"] = value.Skill(
            governing_attribute=self.attributes["Volonte"], acquired=True)
        self.exotic_skills["Jeu"] = value.Skill(acquired=True)
        self.exotic_skills["KamaSutra"] = value.Skill(acquired=True)
        self.exotic_skills["LangageAnimal"] = value.Skill(
            governing_attribute=self.attributes["Perception"], acquired=True)
        self.exotic_skills["Narcolepsie"] = value.Skill(acquired=True)
        self.exotic_skills["Pickpocket"] = value.Skill(
            governing_attribute=self.attributes["Agilite"], acquired=True)
        self.exotic_skills["Prestidigitation"] = value.Skill(
            governing_attribute=self.attributes["Agilite"], acquired=True)
        self.exotic_skills["SixiemeSens"] = value.Skill(
            governing_attribute=self.attributes["Foi"], acquired=True)
        self.exotic_skills["Torture"] = value.Skill(acquired=True)
        self.exotic_skills["Ventriloquie"] = value.Skill(acquired=True)
        # Secondary skills
        self.secondary_skills["Acrobaties"] = value.Skill(
            governing_attribute=self.attributes["Agilite"])
        self.secondary_skills["AisanceSociale"] = value.Skill(
            governing_attribute=self.attributes["Presence"])
        self.secondary_skills["Art"] = value.Skill(
            governing_attribute=self.attributes["Presence"],
            specific=True, acquired=True)
        self.secondary_skills["Athletisme"] = value.Skill(
            governing_attribute=self.attributes["Force"])
        self.secondary_skills["Conduite"] = value.Skill(
            governing_attribute=self.attributes["Agilite"], acquired=True)
        self.secondary_skills["CultureGenerale"] = value.Skill(
            specific=True, acquired=True)
        self.secondary_skills["Hobby"] = value.Skill(
            multiple=True, acquired=True)
        self.secondary_skills["Informatique"] = value.Skill(acquired=True)
        self.secondary_skills["Intimidation"] = value.Skill(
            governing_attribute=self.attributes["Force"])
        self.secondary_skills["Langues"] = value.Skill(
            multiple=True, invariant=True, acquired=True)
        self.secondary_skills["Metier"] = value.Skill(
            specific=True, acquired=True)
        self.secondary_skills["Navigation"] = value.Skill(acquired=True)
        self.secondary_skills["Pilotage"] = value.Skill(acquired=True)
        self.secondary_skills["SavoirCriminel"] = value.Skill(
            specific=True, acquired=True)
        self.secondary_skills["SavoirEspion"] = value.Skill(
            specific=True, acquired=True)
        self.secondary_skills["SavoirMilitaire"] = value.Skill(
            specific=True, acquired=True)
        self.secondary_skills["SavoirOcculte"] = value.Skill(
            specific=True, acquired=True)
        self.secondary_skills["Science"] = value.Skill(
            specific=True, acquired=True)
        self.secondary_skills["Survie"] = value.Skill(
            governing_attribute=self.attributes["Perception"],
            specific=True, acquired=True)
        self.secondary_skills["Technique"] = value.Skill(
            specific=True, acquired=True)

    def init_values(self):
        """Initialize the character's side values."""
        self.values["PF"] = value.Value(0)
        self.values["PP"] = value.Value(0)
        self.values["BL"] = value.Value(0)
        self.values["BG"] = value.Value(0)
        self.values["BF"] = value.Value(0)
        self.values["MS"] = value.Value(0)

    def get_level(self):
        """Return the character's level."""
        return self.level

    def get_name(self):
        """Return the character's name."""
        return self.name

    def print_CLI(self):
        """Print the character's complete profile to the command line."""
        print(self.get_name() + " - Grade " + str(self.level))
        print(" \u251c\u2500 Attributs")
        for a in self.attributes:
            print(" \u2502    \u2514\u2500 " + a + " " +
                self.attributes[a].get_CLI_rank())
        print(" \u251c\u2500 Valeurs annexes")
        for v in self.values:
            print(" \u2502    \u2514\u2500 " + v + " " +
                self.values[v].get_CLI_rank())
        print(" \u251c\u2500 Talents principaux")
        self.print_primary_skills()
        print(" \u251c\u2500 Talents exotiques")
        self.print_exotic_skills()
        print(" \u251c\u2500 Talents secondaires")
        self.print_secondary_skills()
        print(" \u2514\u2500 Pouvoirs")
        self.print_powers()

    def print_exotic_skills(self):
        """Print the character's usable exotic skills."""
        for e in self.exotic_skills:
            if self.exotic_skills[e].is_usable():
                print(" \u2502    \u2514\u2500 " + e +
                    self.exotic_skills[e].get_CLI_rank())

    def print_powers(self):
        """Print the character's powers."""
        for p in self.powers:
            print("      \u2514\u2500 " + p + " " +
                self.powers[p].get_CLI_rank() + " " +
                self.powers[p].get_cost())

    def print_primary_skills(self):
        """Print the character's usable primary skills."""
        for p in self.primary_skills:
            sk = self.primary_skills[p]
            if sk.is_usable():
                print(" \u2502    \u2514\u2500 " + p + " " +
                    sk.get_CLI_rank())
                if sk.is_specific():
                    print(" \u2502        \u2514\u2500 " + p + "_spe " +
                        sk.get_specialization().get_CLI_rank())

    def print_secondary_skills(self):
        """Print the character's usable secondary skills."""
        for s in self.secondary_skills:
            sk = self.secondary_skills[s]
            if sk.is_usable():
                print(" \u2502    \u2514\u2500 " + s + " " +
                    sk.get_CLI_rank())
                if sk.is_specific():
                    print(" \u2502        \u2514\u2500 " + s + "_spe " +
                        sk.get_specialization().get_CLI_rank())
                elif sk.is_multiple():
                    for v in sk.varieties:
                        print(" \u2502        \u2514\u2500 " + v)

    def update_values(self):
        """Compute the character's values and skills."""
        # update primary skills base rank
        for p in self.primary_skills.values():
            p.compute_base_rank()
        # update secondary skills base rank
        for s in self.secondary_skills.values():
            s.compute_base_rank()
        # update exotic skills base rank
        for e in self.exotic_skills.values():
            e.compute_base_rank()
        # update side values
        self.values["PF"].set_base_rank(
            int(self.attributes['Force'].get_real_rank() +
                self.attributes['Volonte'].get_real_rank()))
        self.values["PP"].set_base_rank(
            int(self.attributes['Foi'].get_real_rank() +
                self.attributes['Volonte'].get_real_rank()))
        wound = self.attributes['Force'].get_real_rank()
        if self.nature == 'Demon':
            wound += 2
        elif self.nature == 'Angel':
            wound += 3
        self.values["BL"].set_base_rank(int(wound))
        self.values["BG"].set_base_rank(int(2 * wound))
        self.values["BF"].set_base_rank(int(3 * wound))
        self.values["MS"].set_base_rank(int(4 * wound))
