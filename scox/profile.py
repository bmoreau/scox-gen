#! /usr/bin/env python3

import scox.value as value
import zipfile
import csv
import io
import warnings

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
        reader = csv.DictReader(io.TextIOWrapper(attr))
        for row in reader:
            if row['Name'] in self.attributes:
                self.attributes[row['Name']].increase_rank(int(row['Rank']))
            else:
                raise KeyError("Attribute " + row['Name'] + " not found.")

    def load_primary_skills(self, p_skills):
        """Load primary skills from the input skill file.

        Arguments:
        p_skills -- CSV file containing skills.
        """
        reader = csv.DictReader(io.TextIOWrapper(p_skills))
        for row in reader:
            # case where skill exists
            if row['Name'] in self.primary_skills:
                self.primary_skills[row['Name']].increase_rank(int(row['Rank']))
            # case where skill is a specialization
            elif (row['Name'].split('_')[0] in self.primary_skills and
              row['Name'].split('_')[1] == 'spe'):
                self.primary_skills[row['Name'].split('_')[0]].get_specialization().increase_rank(int(row['Rank']))
            # case where skill does not exist
            else:
                raise KeyError("Skill " + row['Name'] + " not found.")

    def load_secondary_skills(self, s_skills):
        """Load secondary skills from the input skill file.

        Arguments:
        s_skills -- CSV file containing skills.
        """
        reader = csv.DictReader(io.TextIOWrapper(s_skills))
        for row in reader:
            # case where skill exists
            if row['Name'] in self.secondary_skills:
                self.secondary_skills[row['Name']].increase_rank(int(row['Rank']))
            # case where skill is a specialization / a variety
            elif (row['Name'].split('_')[0] in self.secondary_skills):
                sk = self.secondary_skills[row['Name'].split('_')[0]]
                if sk.is_specific():
                    sk.get_specialization().increase_rank(int(row['Rank']))
                elif sk.is_multiple():
                    sk.add_variety(row['Name'].split('_')[1])
                    sk.increase_rank(int(row['Rank']))
                else:
                    warnings.warn("Non specific nor multiple skill; input" +
                        "specialization or variety is ignored.", Warning)
            # case where skill does not exist - it is created
            else:
                if not row['Name'] in self.secondary_skills:
                    self.secondary_skills[row['Name']] = value.Skill(
                        acquired=True)
                self.secondary_skills[row['Name']].increase_rank(
                    int(row['Rank']))

    def load_exotic_skills(self, e_skills):
        """Load exotic skills from the input skill file.

        Arguments:
        e_skills -- CSV file containing skills.
        """
        reader = csv.DictReader(io.TextIOWrapper(e_skills))
        for row in reader:
            if row['Name'] in self.exotic_skills:
                self.exotic_skills[row['Name']].increase_rank(int(row['Rank']))
            else:
                raise KeyError("Skill " + row['Name'] + " not found.")

    def load_powers(self, powers):
        """Load powers from the input power file.

        Arguments:
        powers -- CSV file containing powers.
        """
        print("TODO") # TODO
