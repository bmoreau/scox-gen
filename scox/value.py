#! /usr/bin/env python3
# coding=utf-8

import warnings


class Value:
    """Base class for representing numerical values for characters and profiles
    in scox.

    Instance variables:
    base_rank -- Initial rank of the value, expressed as an integer.
    rank -- Rank of the value, expressed as an integer.
    coordinates -- 2D coordinates of the value on an SVG character sheet.
    """

    def __init__(self, base_rank, coordinates):
        """Constructor.

        Arguments:
        base_rank -- Base rank of the new value.
        coordinates -- 2D coordinates of the nw value.
        """
        self.base_rank = base_rank
        self.rank = 0
        self.coordinates = coordinates

    def get_cli_rank(self):
        """Return the real rank of the represented value as a string of
        characters.
        """
        return str(int(self.get_full_rank()))

    def get_full_rank(self):
        """Return the full rank of the value.

        The full rank of the value equals the sum of its base rank with its
        rank.
        """
        return self.rank + self.base_rank

    def get_x(self):
        """Return the X coordinate of the value."""
        return self.coordinates[0]

    def get_y(self):
        """Return the X coordinate of the value."""
        return self.coordinates[1]

    def increase_rank(self, step):
        """Increase the rank of the value by step.

        Arguments:
        step -- Step by which the rank of the attribute will be increased.
        """
        self.rank += step

    def set_base_rank(self, rank):
        """Set the base rank of the value."""
        self.base_rank = rank

    def set_rank(self, rank):
        """Set the rank of the value."""
        self.rank = rank


class Attribute(Value):
    """Value-derived class for representing character's attributes.

    Instance variables:
    name -- Name of the skill, and how it is displayed.
    invariant -- Boolean value; True if the attribute's rank cannot be
        modified.

    Methods:
    increment_rank -- Increase the rank of the attribute by 1.
    decrement_rank -- Decrease the rank of the attribute by 1.
    """

    def __init__(self, name, base_rank, coordinates, invariant=False):
        """Constructor.

        Arguments:
        name - Human-friendly name of the skill.
        base_rank -- Base rank of the new attribute.
        coordinates -- Coordinates of the attribute on an SVG sheet.

        Keyword arguments:
        invariant -- True if the new attribute is an invariant (default False).
        """
        Value.__init__(self, base_rank, coordinates)
        self.name = name
        self.invariant = invariant

    def increase_rank(self, step):
        """Increase the rank of the attribute by step.
        
        Arguments:
        step -- Step by which the rank of the attribute will be increased.
        """
        if not self.invariant:
            self.rank += step

    def increment_rank(self):
        """Increase the rank of the attribute by 1."""
        if not self.invariant:
            self.rank += 1

    def is_invariant(self):
        """Return True if the attribute is invariant."""
        return self.invariant

    def decrement_rank(self):
        """Decrease the rank of the attribute by 1."""
        if self.rank > 0 and not self.invariant:
            self.rank -= 1

    def get_name(self):
        """Return the name of the skill."""
        return self.name

    def get_real_rank(self):
        """Return the real rank of the represented attribute."""
        return self.get_full_rank() / 2.0

    def get_cli_rank(self):
        """Return the real rank of the represented attribute as a string of
        characters.
        """
        if not self.invariant:
            rank = str(int(self.get_real_rank()))
            rank += ('+' if self.get_full_rank() % 2 != 0 else ' ')
        else:
            rank = None
        return rank

    def set_name(self, name):
        """Set a new name for the skill.

        Args:
            name: a new name for the skill.
        """
        self.name = name


class Skill(Attribute):
    """Attribute-derived class for representing character's skills.

    Instance variables:
    governing_attribute -- Attribute governing the skill base rank.
    varieties -- List of skill varieties, if the skill is multiple.
    specialization -- Skill instance representing a specialization, if the
        skill is specific.
    master_skill -- Generic version of the skill; quite the opposite of
        specialization.
    acquired -- Whether the attribute needs to be invested ranks before it
        can be used (default False).
    """

    def __init__(self, name, coordinates,
                 governing_attribute=None, specific=False,
                 multiple=False, invariant=False, master_skill=None,
                 acquired=False):
        """Constructor.

        Arguments:
        name - Human-friendly name of the skill.
        coordinates -- Coordinates of the skill on an SVG sheet.

        Keyword arguments:
        governing_attribute -- Governing attribute of the new skill (default
            None).
        specific -- Boolean value; True if the new skill is specific (default
            False).
        multiple -- Boolean value; True if the new skill is multiple (default
            False).
        invariant -- True if the new attribute is an invariant (default False).
        master_skill -- A skill instance representing the generic version of 
            self (default None).
        acquired -- True if the new attribute requires a rank investment before
        it can be used (default False).
        """
        Attribute.__init__(self, name, 0, coordinates, invariant=invariant)
        self.governing_attribute = governing_attribute
        self.invariant = invariant
        self.acquired = acquired
        self.specialization = None
        self.varieties = None
        if multiple:
            self.varieties = []
        if specific:
            self.specialization = Skill(
                'Spécialité',
                [coordinates[0] + 63, coordinates[1]],
                governing_attribute=self.governing_attribute,
                master_skill=self,
                acquired=self.acquired
                )
        self.master_skill = master_skill

    def add_variety(self, variety, parent):
        """Append the input variety to the list of this skill's varieties, if
        the skill is multiple.

        Arguments:
        variety -- A variety of this skill.
        parent -- Name of the skill the variety belongs to.
        """
        try:
            if not self.is_invariant() and len(self.varieties) >= 1:
                # case of 'Métier' and 'Hobby' skills which behave like
                # specific skills without master skill; they therefore accept
                # only one variety (ok, maybe 'multiple' was not a good word)
                pass
            elif variety not in self.varieties:
                self.varieties.append(variety)
            else:
                self.varieties.append(parent.rstrip('s') + '_' +
                                      str(len(self.varieties) + 1))
        except AttributeError:
            warnings.warn("Non-multiple skill.", Warning)

    def compute_base_rank(self):
        """Compute the value of the skill's based rank base on the rank of its
        governing attribute, if any.
        """
        if self.governing_attribute is not None:
            self.base_rank = int(self.governing_attribute.get_full_rank() / 2)
        elif not self.invariant:
            self.base_rank = 2
        if self.specialization is not None:
            self.specialization.compute_base_rank()

    def decrement_rank(self):
        """Decrease the rank of the attribute by 1."""
        if self.rank > 0 and not self.invariant and (
                self.master_skill is None or
                self.master_skill.get_full_rank() < self.get_full_rank()):
            self.rank -= 1

    def get_governing_attribute(self):
        """Return the governing attribute of the skill."""
        return self.governing_attribute

    def get_pretty_string(self):
        """Return a string representing the skill for output purposes."""
        skill = self.get_name()
        if self.is_specific():
            skill += (" " + self.get_cli_rank().rstrip() + " (" +
                      self.get_specialization().get_name() + " " +
                      self.get_specialization().get_cli_rank().rstrip() + ")")
        elif self.is_multiple():
            varieties = " ("
            for v in self.get_varieties():
                varieties += v + ", "
            skill += (varieties.rstrip(", ") + ")")
            if not self.is_invariant():
                skill += " " + self.get_cli_rank().rstrip()
        else:
            skill += " " + self.get_cli_rank().rstrip()
        return skill

    def get_specialization(self):
        """Return the specialization of the skill, if it exists."""
        if self.is_specific():
            return self.specialization
        else:
            warnings.warn("Non-specific skill.", Warning)

    def get_varieties(self):
        """Return the varieties of the skill, if they exist."""
        if self.is_multiple():
            return self.varieties
        else:
            warnings.warn("Non-multiple skill.", Warning)

    def increment_rank(self):
        """Increase the rank of the attribute by 1."""
        if not self.invariant and (
                self.specialization is None or
                self.specialization.get_full_rank() > self.get_full_rank()):
            self.rank += 1

    def is_multiple(self):
        """Return True if this skill is multiple."""
        if self.varieties is not None:
            return True
        else:
            return False

    def is_specific(self):
        """Return True if this skill is specific."""
        if self.specialization is not None:
            return True
        else:
            return False

    def is_usable(self):
        """Return True if this skill can be used by the character.
        
        A skill is usable if one of those conditions is true:
        - it is not acquired;
        - if acquired, at least one rank was invested in it;
        - if specific with a usable specialization;
        - is multiple with at least one variety.
        """
        if not self.acquired or self.rank != 0:
            return True
        elif self.is_specific() and self.specialization.is_usable():
            return True
        elif self.varieties is not None and len(self.varieties) != 0:
            return True
        else:
            return False


class Power(Attribute):
    """Attribute-derived class for representing character's powers.

    Instance variables:
    cost -- String; short description of the cost for using the power (usually
        expressed in PP, per time unit or not).
    """

    def __init__(self, name, cost, coordinates, base_rank=0,
                 invariant=False):
        """Constructor.

        Arguments:
        name -- Human-friendly name of the power.
        cost -- Cost for activating the power.
        coordinates -- Coordinates of the skill on an SVG sheet.

        Keyword arguments:
        invariant -- True if the new attribute is an invariant (default False).
        base_rank -- Base rank of the new attribute (default 0).
        """
        Attribute.__init__(self, name, base_rank, coordinates,
                           invariant=invariant)
        self.cost = cost

    def get_cost(self):
        """Return the cost for activating the power."""
        return self.cost
