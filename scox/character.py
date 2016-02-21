#! /usr/bin/env python3

import scox.value as value
import scox.profile as profile

class Character(profile.Profile):
    """Base class for representing characters in scox.
    
    A character is defined as a set of values, ordered by lists depending on
    their types: a list of attributes, a list of skills, a list of powers and a
    list of mandatory values.

    Instance variables:
    __level -- Level of the character in his / her hierarchy (default 0).
    __name -- Name of the character.
    __nature -- Nature of the character; either 'Angel' or 'Demon'.
    __notes -- Speak your mind freely.
    __side_values -- Map of additional character defining values.
    __superior -- Hierarchical superior of the character.

    Methods:
    apply_profile -- Apply the modifications listed in an input profile.
    init_attributes -- Initialize the character's attributes.
    init_skills -- Initialize the character's skills.
    init_values -- Initialize the character's attributes.
    update_values -- Update the base ranks of the skills listed in
        self.__skills and the values of self.__side_values using the current
        ranks of self.__attributes.
    """

    def __init__(self, name, level=0, nature='Demon'):
        """Constructor.

        Arguments:
        name -- Name of the new character.

        Keyword arguments:
        level -- Level of the new character (default 0).
        nature -- Nature of the new character (default 'Demon').
        """
        self.__name = name
        self.__level = level
        self.__nature = nature
        self.__powers = {}
        self.__superior = None
        self.init_attributes()
        self.init_skills()
        self.init_values()

    def init_attributes(self):
        """Initialize the character's attributes."""
        self.__attributes = {}
        self.__attributes["Force"] = value.Attribute(4)
        self.__attributes["Agilite"] = value.Attribute(4)
        self.__attributes["Perception"] = value.Attribute(4)
        self.__attributes["Volonte"] = value.Attribute(4)
        self.__attributes["Presence"] = value.Attribute(4)
        self.__attributes["Foi"] = value.Attribute(4)

    def init_skills(self):
        """Initialize the character's skills."""
        # Primary skills
        self.__primary_skills = {}
        self.__primary_skills["Baratin"] = value.Skill(
            governing_attribute=self.__attributes["Presence"])
        self.__primary_skills["Combat"] = value.Skill(
            governing_attribute=self.__attributes["Agilite"],
            specific=True)
        self.__primary_skills["CaC"] = value.Skill(
            governing_attribute=self.__attributes["Agilite"])
        self.__primary_skills["Defense"] = value.Skill(
            governing_attribute=self.__attributes["Agilite"])
        self.__primary_skills["Discretion"] = value.Skill(
            governing_attribute=self.__attributes["Agilite"])
        self.__primary_skills["Discussion"] = value.Skill(
            governing_attribute=self.__attributes["Volonte"])
        self.__primary_skills["Enquete"] = value.Skill(
            governing_attribute=self.__attributes["Foi"])
        self.__primary_skills["Fouille"] = value.Skill(
            governing_attribute=self.__attributes["Perception"])
        self.__primary_skills["Intrusion"] = value.Skill(acquired=True)
        self.__primary_skills["Medecine"] = value.Skill(acquired=True)
        self.__primary_skills["Seduction"] = value.Skill(
            governing_attribute=self.__attributes["Presence"])
        self.__primary_skills["Tir"] = value.Skill(
            governing_attribute=self.__attributes["Perception"],
            specific=True)
        # Exotic skills
        self.__exotic_skills = {}
        self.__exotic_skills["Contorsionnisme"] = value.Skill(
            governing_attribute=self.__attributes["Agilite"], acquired=True)
        self.__exotic_skills["Humour"] = value.Skill(acquired=True)
        self.__exotic_skills["Hypnotisme"] = value.Skill(
            governing_attribute=self.__attributes["Volonte"], acquired=True)
        self.__exotic_skills["Jeu"] = value.Skill(acquired=True)
        self.__exotic_skills["KamaSutra"] = value.Skill(acquired=True)
        self.__exotic_skills["LangageAnimal"] = value.Skill(
            governing_attribute=self.__attributes["Perception"], acquired=True)
        self.__exotic_skills["Narcolepsie"] = value.Skill(
            governing_attribute=self.__attributes["Volonte"], acquired=True)
        self.__exotic_skills["Pickpocket"] = value.Skill(
            governing_attribute=self.__attributes["Agilite"], acquired=True)
        self.__exotic_skills["Prestidigitation"] = value.Skill(
            governing_attribute=self.__attributes["Agilite"], acquired=True)
        self.__exotic_skills["SixiemeSens"] = value.Skill(
            governing_attribute=self.__attributes["Foi"], acquired=True)
        self.__exotic_skills["Torture"] = value.Skill(acquired=True)
        # Secondary skills
        self.__secondary_skills = {}
        self.__secondary_skills["Acrobaties"] = value.Skill(
            governing_attribute=self.__attributes["Agilite"])
        self.__secondary_skills["AisanceSociale"] = value.Skill(
            governing_attribute=self.__attributes["Presence"])
        self.__secondary_skills["Art"] = value.Skill(
            governing_attribute=self.__attributes["Presence"],
            specific=True, acquired=True)
        self.__secondary_skills["Athletisme"] = value.Skill(
            governing_attribute=self.__attributes["Force"])
        self.__secondary_skills["Conduite"] = value.Skill(
            governing_attribute=self.__attributes["Agilite"], acquired=True)
        self.__secondary_skills["CultureGenerale"] = value.Skill(
            specific=True, acquired=True)
        self.__secondary_skills["Hobby"] = value.Skill(
            specific=True, acquired=True)
        self.__secondary_skills["Informatique"] = value.Skill(acquired=True)
        self.__secondary_skills["Intimidation"] = value.Skill(
            governing_attribute=self.__attributes["Force"])
        self.__secondary_skills["Langues"] = value.Skill(
            multiple=True, invariant=True, acquired=True)
        self.__secondary_skills["Metier"] = value.Skill(
            specific=True, acquired=True)
        self.__secondary_skills["Navigation"] = value.Skill(acquired=True)
        self.__secondary_skills["Pilotage"] = value.Skill(acquired=True)
        self.__secondary_skills["SavoirCriminel"] = value.Skill(
            specific=True, acquired=True)
        self.__secondary_skills["SavoirEspion"] = value.Skill(
            specific=True, acquired=True)
        self.__secondary_skills["SavoirMilitaire"] = value.Skill(
            specific=True, acquired=True)
        self.__secondary_skills["SavoirOcculte"] = value.Skill(
            specific=True, acquired=True)
        self.__secondary_skills["Science"] = value.Skill(
            specific=True, acquired=True)
        self.__secondary_skills["Survie"] = value.Skill(
            governing_attribute=self.__attributes["Perception"],
            specific=True, acquired=True)
        self.__secondary_skills["Technique"] = value.Skill(
            specific=True, acquired=True)

    def init_values(self):
        """Initialize the character's side values."""
        self.__values = {}
        self.__values["PF"] = value.Value(0)
        self.__values["PP"] = value.Value(0)
        self.__values["BL"] = value.Value(0)
        self.__values["BG"] = value.Value(0)
        self.__values["BF"] = value.Value(0)
        self.__values["MS"] = value.Value(0)

    def get_level(self):
        """Return the character's level."""
        return self.__level

    def get_name(self):
        """Return the character's name."""
        return self.__name

    def update_values(self):
        """Compute the character's values and skills."""
        # TODO
