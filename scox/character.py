#! /usr/bin/env python3

import value
import profile

class Character(Profile):
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
        self.__primary_skills = {}
        self.__exotic_skills = {}
        self.__secondary_skills = {}
        # TODO: populate the map

    def init_values(self):
        """Initialize the character's side values."""
        self.__values = {}
        self.values["PF"] = value.Value(0)
        self.values["PP"] = value.Value(0)
        self.values["BL"] = value.Value(0)
        self.values["BG"] = value.Value(0)
        self.values["BF"] = value.Value(0)
        self.values["MS"] = value.Value(0)

    def get_level(self):
        """Return the character's level."""
        return self.__level

    def get_name(self):
        """Return the character's name."""
        return self.__name

    def update_values(self):
        """Compute the character's values and skills."""
        # TODO
