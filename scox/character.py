#! /usr/bin/env python3
# coding=utf-8

import scox.value as value
import scox.profile as profile


class Character(profile.Profile):
    """Base class for representing characters in scox.
    
    A character is defined as a set of values, ordered by lists depending on
    their types: a list of attributes, a list of skills, a list of powers and a
    list of mandatory values.

    Instance variables:
    level -- Level of the character in his / her hierarchy (default 0).
    lvl_coords -- Coordinates of the character's level on an SVG export.
    name -- Name of the character.
    name_coords -- Coordinates of the character's name on an SVG export.
    notes -- Speak your mind freely.
    side_values -- Map of additional character defining values.
    sup_coords -- Coordinates of the character's superior on an SVG export.

    Methods:
    export -- Serialize the character as a pickle file.
    init_attributes -- Initialize the character's attributes.
    init_skills -- Initialize the character's skills.
    init_values -- Initialize the character's attributes.
    update_values -- Update the base ranks of the skills listed in
        skill attributes and the values of self.side_values using the current
        ranks of self.attributes.
    """

    def __init__(self, name, nature, archetype, superior, level=0):
        """Constructor.

        Arguments:
        name -- Name of the new character.
        nature -- Nature of the new character.
        archetype -- Archetype of the character.
        superior -- Superior of the character.

        Keyword arguments:
        level -- Level of the new character (default 0).
        """
        profile.Profile.__init__(self, nature.capitalize())
        self.name = name
        self.level = level
        self.name_coords = [722, 136] if self.nature == 'Demon' else [1125, 138]
        self.lvl_coords = [1715, 233] if self.nature == 'Demon' else [2253, 236]
        self.sup_coords = [761, 233] if self.nature == 'Demon' else [1163, 236]
        self.init_attributes()
        self.init_skills()
        self.init_values()
        self.load_profile(superior)
        self.load_profile(archetype, True)
        self.draw_from_table(2)
        self.update_values()

    def init_attributes(self):
        """Initialize the character's attributes."""
        self.attributes["Force"] = value.Attribute(
            'Force',
            4, [161, 525] if self.nature == 'Demon' else [837, 653])
        self.attributes["Agilite"] = value.Attribute(
            'Agilité',
            4, [394, 508] if self.nature == 'Demon' else [1245, 653])
        self.attributes["Perception"] = value.Attribute(
            'Perception',
            4, [689, 538] if self.nature == 'Demon' else [1653, 653])
        self.attributes["Volonte"] = value.Attribute(
            'Volonté',
            4, [1021, 540] if self.nature == 'Demon' else [837, 1037])
        self.attributes["Presence"] = value.Attribute(
            'Présence',
            4, [1294, 530] if self.nature == 'Demon' else [1245, 1037])
        self.attributes["Foi"] = value.Attribute(
            'Foi',
            4, [1563, 536] if self.nature == 'Demon' else [1653, 1037])

    def init_skills(self):
        """Initialize the character's skills."""
        # Primary skills
        self.primary_skills["Baratin"] = value.Skill(
            'Baratin',
            [983, 924] if self.nature == 'Demon' else [914, 1277],
            governing_attribute=self.attributes["Presence"])
        self.primary_skills["Combat"] = value.Skill(
            'Combat',
            [942, 987] if self.nature == 'Demon' else [873, 1339.5],
            governing_attribute=self.attributes["Agilite"],
            specific=True)
        self.primary_skills["CaC"] = value.Skill(
            'Corps à corps',
            [983, 1050] if self.nature == 'Demon' else [914, 1402],
            governing_attribute=self.attributes["Agilite"])
        self.primary_skills["Defense"] = value.Skill(
            'Défense',
            [983, 1113] if self.nature == 'Demon' else [914, 1464.5],
            governing_attribute=self.attributes["Agilite"])
        self.primary_skills["Discretion"] = value.Skill(
            'Discrétion',
            [983, 1176] if self.nature == 'Demon' else [914, 1527],
            governing_attribute=self.attributes["Agilite"])
        self.primary_skills["Discussion"] = value.Skill(
            'Discussion',
            [983, 1239] if self.nature == 'Demon' else [914, 1589.5],
            governing_attribute=self.attributes["Volonte"])
        self.primary_skills["Enquete"] = value.Skill(
            'Enquête',
            [983, 1302] if self.nature == 'Demon' else [914, 1652],
            governing_attribute=self.attributes["Foi"])
        self.primary_skills["Fouille"] = value.Skill(
            'Fouille',
            [983, 1365] if self.nature == 'Demon' else [914, 1714.5],
            governing_attribute=self.attributes["Perception"])
        self.primary_skills["Intrusion"] = value.Skill(
            'Intrusion',
            [983, 1428] if self.nature == 'Demon' else [914, 1777],
            acquired=True)
        self.primary_skills["Medecine"] = value.Skill(
            'Médecine',
            [983, 1491] if self.nature == 'Demon' else [914, 1839.5],
            acquired=True)
        self.primary_skills["Seduction"] = value.Skill(
            'Séduction',
            [983, 1554] if self.nature == 'Demon' else [914, 1902],
            governing_attribute=self.attributes["Presence"])
        self.primary_skills["Tir"] = value.Skill(
            'Tir',
            [942, 1617] if self.nature == 'Demon' else [873, 1964.5],
            governing_attribute=self.attributes["Perception"],
            specific=True)
        # Exotic skills
        self.exotic_skills["Contorsionnisme"] = value.Skill(
            'Contorsionnisme',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            governing_attribute=self.attributes["Agilite"], acquired=True)
        self.exotic_skills["Humour"] = value.Skill(
            'Humour',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            acquired=True)
        self.exotic_skills["Hypnotisme"] = value.Skill(
            'Hypnotisme',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            governing_attribute=self.attributes["Volonte"],
            acquired=True)
        self.exotic_skills["Jeu"] = value.Skill(
            'Jeu',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            acquired=True)
        self.exotic_skills["KamaSutra"] = value.Skill(
            'Kama Sutra',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            acquired=True)
        self.exotic_skills["LangageAnimal"] = value.Skill(
            'Langage animal',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            governing_attribute=self.attributes["Perception"], acquired=True)
        self.exotic_skills["Narcolepsie"] = value.Skill(
            'Narcolepsie',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            acquired=True)
        self.exotic_skills["Pickpocket"] = value.Skill(
            'Pickpocket',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            governing_attribute=self.attributes["Agilite"], acquired=True)
        self.exotic_skills["Prestidigitation"] = value.Skill(
            'Prestidigitation',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            governing_attribute=self.attributes["Agilite"], acquired=True)
        self.exotic_skills["SixiemeSens"] = value.Skill(
            'Sixième sens',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            governing_attribute=self.attributes["Foi"], acquired=True)
        self.exotic_skills["Torture"] = value.Skill(
            'Torture',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            acquired=True)
        self.exotic_skills["Ventriloquie"] = value.Skill(
            'Ventriloquie',
            [983, 1800] if self.nature == 'Demon' else [914, 2136],
            acquired=True)
        #  Secondary skills
        self.secondary_skills["Acrobaties"] = value.Skill(
            'Acrobaties',
            [983, 2238] if self.nature == 'Demon' else [2078, 1277],
            governing_attribute=self.attributes["Agilite"])
        self.secondary_skills["AisanceSociale"] = value.Skill(
            'Aisance sociale',
            [983, 2300.5] if self.nature == 'Demon' else [2078, 1339.5],
            governing_attribute=self.attributes["Presence"])
        self.secondary_skills["Art"] = value.Skill(
            'Art',
            [942, 2363] if self.nature == 'Demon' else [2037, 1402],
            governing_attribute=self.attributes["Presence"],
            specific=True, acquired=True)
        self.secondary_skills["Athletisme"] = value.Skill(
            'Athlétisme',
            [983, 2425.5] if self.nature == 'Demon' else [2078, 1464.5],
            governing_attribute=self.attributes["Force"])
        self.secondary_skills["Conduite"] = value.Skill(
            'Conduite',
            [983, 2488] if self.nature == 'Demon' else [2078, 1527],
            governing_attribute=self.attributes["Agilite"], acquired=True)
        self.secondary_skills["CultureGenerale"] = value.Skill(
            'Culture générale',
            [942, 2550.5] if self.nature == 'Demon' else [2037, 1589.5],
            specific=True, acquired=True)
        self.secondary_skills["Hobby"] = value.Skill(
            'Hobby',
            [983, 2613] if self.nature == 'Demon' else [2078, 1652],
            multiple=True, acquired=True)
        self.secondary_skills["Informatique"] = value.Skill(
            'Informatique',
            [983, 2675.5] if self.nature == 'Demon' else [2078, 1714.5],
            acquired=True)
        self.secondary_skills["Intimidation"] = value.Skill(
            'Intimidation',
            [983, 2738] if self.nature == 'Demon' else [2078, 1777],
            governing_attribute=self.attributes["Force"])
        self.secondary_skills["Langues"] = value.Skill(
            'Langues',
            [347, 2800.5] if self.nature == 'Demon' else [1442, 1839.5],
            multiple=True, invariant=True, acquired=True)
        self.secondary_skills["Metier"] = value.Skill(
            'Métier',
            [983, 2863] if self.nature == 'Demon' else [2078, 1902],
            multiple=True, acquired=True)
        self.secondary_skills["Navigation"] = value.Skill(
            'Navigation',
            [983, 2925.5] if self.nature == 'Demon' else [2078, 1964],
            acquired=True)
        self.secondary_skills["Pilotage"] = value.Skill(
            'Pilotage',
            [983, 2988] if self.nature == 'Demon' else [2078, 2027],
            acquired=True)
        self.secondary_skills["SavoirCriminel"] = value.Skill(
            'Savoir criminel',
            [942, 3050.5] if self.nature == 'Demon' else [2037, 2089.5],
            specific=True, acquired=True)
        self.secondary_skills["SavoirEspion"] = value.Skill(
            'Savoir espion',
            [942, 3113] if self.nature == 'Demon' else [2037, 2152],
            specific=True, acquired=True)
        self.secondary_skills["SavoirMilitaire"] = value.Skill(
            'Savoir militaire',
            [942, 3175.5] if self.nature == 'Demon' else [2037, 2214.5],
            specific=True, acquired=True)
        self.secondary_skills["SavoirOcculte"] = value.Skill(
            'Savoir occulte',
            [942, 3238] if self.nature == 'Demon' else [2037, 2277],
            specific=True, acquired=True)
        self.secondary_skills["Science"] = value.Skill(
            'Science',
            [942, 3300.5] if self.nature == 'Demon' else [2037, 2339.5],
            specific=True, acquired=True)
        self.secondary_skills["Survie"] = value.Skill(
            'Survie',
            [942, 3363] if self.nature == 'Demon' else [2037, 2402],
            governing_attribute=self.attributes["Perception"],
            specific=True, acquired=True)
        self.secondary_skills["Technique"] = value.Skill(
            'Technique',
            [942, 3425.5] if self.nature == 'Demon' else [2037, 2464.5],
            specific=True, acquired=True)

    def init_values(self):
        """Initialize the character's side values."""
        self.values["PF"] = value.Value(
            0, [1383, 805] if self.nature == 'Demon' else [1951, 556])
        self.values["PP"] = value.Value(
            0, [1383, 867] if self.nature == 'Demon' else [1951, 641])
        self.values["BL"] = value.Value(
            0, [1373, 945] if self.nature == 'Demon' else [1951, 726])
        self.values["BG"] = value.Value(
            0, [1373, 1009] if self.nature == 'Demon' else [1951, 811])
        self.values["BF"] = value.Value(
            0, [1373, 1073] if self.nature == 'Demon' else [1951, 896])
        self.values["MS"] = value.Value(
            0, [1373, 1137] if self.nature == 'Demon' else [1951, 981])

    def get_attributes(self):
        """Return the character's attributes."""
        return self.attributes

    def get_exotic_skills(self):
        """Return the character's exotic skills."""
        return self.exotic_skills

    def get_level(self):
        """Return the character's level."""
        return self.level

    def get_lvl_coords(self):
        """Return the character's level coordinates."""
        return self.lvl_coords

    def get_name(self):
        """Return the character's name."""
        return self.name

    def get_name_coords(self):
        """Return the character's name coordinates."""
        return self.name_coords

    def get_powers(self):
        """Return the character's powers."""
        return self.powers

    def get_primary_skills(self):
        """Return the character's primary skills."""
        return self.primary_skills

    def get_secondary_skills(self):
        """Return the character's secondary skills."""
        return self.secondary_skills

    def get_side_values(self):
        """Return the character's side values."""
        return self.values

    def get_sup_coords(self):
        """Return the character's superior coordinates."""
        return self.sup_coords

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
