#! /usr/bin/env python3
# coding=utf-8

import scox.value as value

import zipfile
import csv
import io
import warnings
import collections
import os
import random


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
    nature -- Nature of the profile; either 'Angel' or 'Demon'.
    superior -- Hierarchical superior of the character.
    power_table -- A map used for drawing random powers for this profile.
    """

    def __init__(self, nature):
        """Constructor.

        Arguments:
        name -- Nature of the profile.
        """
        self.attributes = collections.OrderedDict()
        self.values = collections.OrderedDict()
        self.powers = collections.OrderedDict()
        self.primary_skills = collections.OrderedDict()
        self.secondary_skills = collections.OrderedDict()
        self.exotic_skills = collections.OrderedDict()
        self.nature = nature
        self.superior = None
        self.power_table = None

    def draw_from_table(self, iterations):
        """Draw random elements from the profile power table and apply the
        results.

        Arguments:
        iterations -- Number of successes required before ending the draws.
        """
        if self.power_table is not None:
            it = 0
            coords = [2135, 1357] if self.nature == 'Demon' else [939, 2628]
            shift = 72
            keys = [k for k in self.power_table.keys()]
            while it < iterations:
                roll = self.power_table[random.choice(keys)]
                reroll = False
                for i in roll[0].keys():
                    if i in self.powers:
                        reroll = True  # roll is void if power already exists
                        break
                if not reroll:
                    # update profile's PP value
                    self.values['PP'].increase_rank(int(roll[1]))
                    # add new powers to the profile
                    for k in roll[0].keys():
                        p = roll[0][k]
                        if p[0] == 'True':
                            self.powers[k] = value.Power(
                                k,
                                p[2],
                                [coords[0], coords[1] +
                                 len(self.powers) * shift],
                                invariant=True)
                        else:
                            self.powers[k] = value.Power(
                                k,
                                p[2],
                                [coords[0], coords[1] +
                                 len(self.powers) * shift],
                                base_rank=2 * int(p[1]))
                    it += 1  # current iteration is successful
                else:
                    break  # exit current iteration
        else:
            raise Exception("Power table does not exist; please load an "
                            "archetype profile first.")

    def generate_power_table(self, table):
        """Generate a table from which random powers can be drawn.

        Arguments:
        table -- CSV file containing information for building the table.
        """
        self.power_table = {}
        reader = csv.DictReader(io.TextIOWrapper(table), delimiter=';')
        for row in reader:
            val = row['value'].strip('[]').split(',')
            powers = {}  # building powers dictionary
            power_items = row['powers'].strip('{}').split('|')
            for item in power_items:
                k, v = item.split(':')
                powers[k.strip('"')] = v.strip('[]').replace('"', '').split(',')
            pp = int(row['pp'])
            bonus = {}  # building bonus dictionary
            bonus_str = row['bonus'].strip('{}')
            if len(bonus_str) > 0:
                bonus_items = bonus_str.split(',')
                for item in bonus_items:
                    k, v = item.split(':')
                    bonus[k] = int(v)
            if self.superior.title() in bonus.keys():
                pp = bonus[self.superior.title()]
            for i in val:
                self.power_table[int(i)] = [powers, pp]

    def get_nature(self):
        """Return the profile's nature."""
        return self.nature

    def get_superior(self):
        """Return the profile's nature."""
        return self.superior

    def load_profile(self, profile, archetype=False):
        """Load a profile from the input profile archive.

        Arguments:
        profile -- Name of a profile archive.
        archetype -- True if the loaded profile is an archetype (default:
        False).
        """
        with zipfile.ZipFile(profile) as p:
            with p.open('attributes.csv') as attr:
                self.load_attributes(attr)
            with p.open('values.csv') as val:
                self.load_side_values(val)
            with p.open('primary_skills.csv') as p_skills:
                self.load_primary_skills(p_skills)
            with p.open('secondary_skills.csv') as s_skills:
                self.load_secondary_skills(s_skills)
            with p.open('exotic_skills.csv') as e_skills:
                self.load_exotic_skills(e_skills)
            with p.open('powers.csv') as powers:
                self.load_powers(powers)
            if archetype and self.nature.upper() == 'DEMON':
                with p.open('table_demon.csv') as table:
                    self.generate_power_table(table)
            elif archetype and self.nature.upper() == 'ANGEL':
                with p.open('table_angel.csv') as table:
                    self.generate_power_table(table)
            else:
                self.superior =\
                    profile.split(os.path.sep)[-1].split('.')[0].title()

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
            #  case where skill exists
            if row['Name'] in self.primary_skills:
                self.primary_skills[row['Name']].increase_rank(int(row['Rank']))
            # case where skill is a specialization
            elif (row['Name'].split('_')[0] in self.primary_skills and
                    row['Name'].split('_')[1] == 'spe'):
                self.primary_skills[row['Name'].split('_')[
                    0]].get_specialization().increase_rank(int(row['Rank']))
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
            #  case where skill exists
            if row['Name'] in self.secondary_skills:
                self.secondary_skills[row['Name']].increase_rank(
                    int(row['Rank']))
            # case where skill is a specialization / a variety
            elif row['Name'].split('_')[0] in self.secondary_skills:
                sk = self.secondary_skills[row['Name'].split('_')[0]]
                if sk.is_specific():
                    sk.get_specialization().increase_rank(int(row['Rank']))
                elif sk.is_multiple():
                    sk.add_variety(row['Name'].split('_')[1],
                                   row['Name'].split('_')[0])
                    sk.increase_rank(int(row['Rank']))
                else:
                    warnings.warn("Non specific nor multiple skill; input" +
                                  "specialization or variety is ignored.",
                                  Warning)
            # case where skill does not exist - it is created
            else:
                if not row['Name'] in self.secondary_skills:
                    self.secondary_skills[row['Name']] = value.Skill(
                        row['Name'],
                        [0, 0],  # FIXME: which coordinates for this skill?
                        acquired=True)
                self.secondary_skills[row['Name']].increase_rank(
                    int(row['Rank']))

    def load_powers(self, powers):
        """Load powers from the input power file.

        Arguments:
        powers -- CSV file containing powers.
        """
        reader = csv.DictReader(io.TextIOWrapper(powers))
        coords = [2135, 1357] if self.nature == 'Demon' else [939, 2628]
        shift = 72
        for row in reader:
            if row['Name'] in self.powers:
                raise KeyError("Power " + row['Name'] + " already exists.")
            else:
                if row['Invariant'] == 'True':
                    self.powers[row['Name']] = value.Power(
                        row['Name'],
                        row['Cost'],
                        [coords[0], coords[1] + len(self.powers) * shift],
                        invariant=True)
                else:
                    self.powers[row['Name']] = value.Power(
                        row['Name'],
                        row['Cost'],
                        [coords[0], coords[1] + len(self.powers) * shift],
                        base_rank=2 * int(row['Rank']))

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

    def load_side_values(self, values):
        """Load side values from the input value file.

        Arguments:
        values -- CSV file containing side values.
        """
        reader = csv.DictReader(io.TextIOWrapper(values))
        for row in reader:
            if row['Name'] in self.values:
                self.values[row['Name']].set_rank(int(row['Rank']))
            else:
                raise KeyError("Value " + row['Name'] + " not found.")
