#! /usr/bin/env python3

import zipfile
import scox.value as value

class Profile:
    """Base class for representing a character's numerical values.

    This class can be used either as a superior or an archetype profile.
    Profiles are used as templates to be applied to characters in the context
    of quick character creation.

    Instance variables:
    __attributes -- Map of profile defining attributes.
    __powers -- Map of profile defining powers.
    __primary_skills -- Map of profile's defining skills.
    __secondary_skills -- Map of profile's slightly less defining skills.
    __exotic_skills -- Map of profile's unusual skills.
    """

    def __init__(self, profile):
        """Constructor.

        Arguments:
        profile -- Path to a profile.scx archive.
        """
        self.__attributes = {}
        self.__powers = {}
        self.__primary_skills = {}
        self.__secondary_skills = {}
        self.__exotic_skills = {}
        with zipfile.ZipFile(profile) as p:
            with p.open('attributes.csv') as attr:
                self.__load_attributes(attr)
            with p.open('primary_skills.csv') as p_skills:
                self.__load_primary_skills(p_skills)
            with p.open('secondary_skills.csv') as s_skills:
                self.__load_secondary_skills(s_skills)
            with p.open('exotic_skills.csv') as e_skills:
                self.__load_exotic_skills(e_skills)
            with p.open('powers.csv') as powers:
                self.__load_powers(powers)

    def __load_attributes(self, attr):
        """Load attributes from the input attribute file.

        Arguments:
        attr -- CSV file containing attributes.
        """
        reader = csv.DictReader(attr)
        for row in reader:
            self.__attributes[row['Name']] = value.Attribute(row['Rank'])

    def __load_primary_skills(self, p_skills):
        """Load primary skills from the input skill file.

        Arguments:
        p_skills -- CSV file containing skills.
        """
        print("TODO") # TODO

    def __load_secondary_skills(self, s_skills):
        """Load secondary skills from the input skill file.

        Arguments:
        s_skills -- CSV file containing skills.
        """
        print("TODO") # TODO

    def __load_exotic_skills(self, e_skills):
        """Load exotic skills from the input skill file.

        Arguments:
        e_skills -- CSV file containing skills.
        """
        print("TODO") # TODO

    def __load_powers(self, powers):
        """Load powers from the input power file.

        Arguments:
        powers -- CSV file containing powers.
        """
        print("TODO") # TODO
