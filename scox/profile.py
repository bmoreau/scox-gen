#! /usr/bin/env python3

import zipfile
import scox.value as value

class Profile:
    """Base class for representing a character's numerical values.

    This class can be used either as a superior or an archetype profile.
    Profiles are used as templates to be applied to characters in the context
    of quick character creation.

    Instance variables:
    attributes -- Map of profile defining attributes.
    powers -- Map of profile defining powers.
    primary_skills -- Map of profile's defining skills.
    secondary_skills -- Map of profile's slightly less defining skills.
    exotic_skills -- Map of profile's unusual skills.
    """

    def __init__(self):
        """Constructor."""
        self.attributes = {}
        self.powers = {}
        self.primary_skills = {}
        self.secondary_skills = {}
        self.exotic_skills = {}

    def load_profile(self, profile):
        """Load a profile from the input profile archive.

        Arguments:
        profile -- Path to a profile.scx archive.
        """
        with zipfile.ZipFile(profile) as p:
            with p.open('attributes.csv') as attr:
                self.load_attributes(attr)
            with p.open('primary_skills.csv') as p_skills:
                self.load_primary_skills(p_skills)
            with p.open('secondary_skills.csv') as s_skills:
                self.load_secondary_skills(s_skills)
            with p.open('exotic_skills.csv') as e_skills:
                self.load_exotic_skills(e_skills)
            with p.open('powers.csv') as powers:
                self.load_powers(powers)

    def load_attributes(self, attr):
        """Load attributes from the input attribute file.

        Arguments:
        attr -- CSV file containing attributes.
        """
        reader = csv.DictReader(attr)
        for row in reader:
            self.attributes[row['Name']] = value.Attribute(row['Rank'])

    def load_primary_skills(self, p_skills):
        """Load primary skills from the input skill file.

        Arguments:
        p_skills -- CSV file containing skills.
        """
        print("TODO") # TODO

    def load_secondary_skills(self, s_skills):
        """Load secondary skills from the input skill file.

        Arguments:
        s_skills -- CSV file containing skills.
        """
        print("TODO") # TODO

    def load_exotic_skills(self, e_skills):
        """Load exotic skills from the input skill file.

        Arguments:
        e_skills -- CSV file containing skills.
        """
        print("TODO") # TODO

    def load_powers(self, powers):
        """Load powers from the input power file.

        Arguments:
        powers -- CSV file containing powers.
        """
        print("TODO") # TODO
