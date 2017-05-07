#! /usr/bin/env python3
# coding=utf-8

import warnings


def format_attribute(name, val, lng):
    """Format a string for displaying the name and value of an attribute.

    Args:
        name: name of the attribute to display.
        val: value of the attribute to display.
        lng: length of the string to be returned, in number of
        characters. Blank space will be padded with '-' characters.

    Returns: a string.
    """
    name += ' '
    if val is not None:
        val = ' ' + val
        lng -= len(val)
        return '{:-<{pad}.{trunc}}{}'.format(
            name, val, pad=lng, trunc=lng)
    else:
        return '{:<{pad}.{trunc}}'.format(name, pad=lng, trunc=lng)


class Value:
    """Base class for representing numerical values for characters and profiles
    in scox.

    Instance variables:
    base_rank -- Initial rank of the value, expressed as an integer.
    rank -- Rank of the value, expressed as an integer.
    """

    def __init__(self, base_rank):
        """Constructor.

        Arguments:
        base_rank -- Base rank of the new value.
        """
        self.base_rank = base_rank
        self.rank = 0

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
    invariant -- Boolean value; True if the attribute's rank cannot be
        modified.

    Methods:
    increment_rank -- Increase the rank of the attribute by 1.
    decrement_rank -- Decrease the rank of the attribute by 1.
    """

    def __init__(self, base_rank, invariant=False):
        """Constructor.

        Arguments:
        base_rank -- Base rank of the new attribute.

        Keyword arguments:
        invariant -- True if the new attribute is an invariant (default False).
        """
        Value.__init__(self, base_rank)
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

    def decrement_rank(self):
        """Decrease the rank of the attribute by 1."""
        if self.rank > 0 and not self.invariant:
            self.rank -= 1

    def get_real_rank(self):
        """Return the real rank of the represented attribute."""
        return self.get_full_rank() / 2.0

    def get_cli_rank(self):
        """Return the real rank of the represented attribute as a string of
        characters.
        """
        if not self.invariant:
            rank = str(int(self.get_real_rank()))
            if self.get_full_rank() % 2 != 0:
                rank += '+'
            else:
                rank += ' '
        else:
            rank = None
        return rank


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

    def __init__(self, governing_attribute=None, specific=False,
                 multiple=False, invariant=False, master_skill=None,
                 acquired=False):
        """Constructor.

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
        Attribute.__init__(self, 0, invariant=invariant)
        self.governing_attribute = governing_attribute
        self.invariant = invariant
        self.acquired = acquired
        self.specialization = None
        self.varieties = None
        if multiple:
            self.varieties = []
        if specific:
            self.specialization = Skill(
                governing_attribute=self.governing_attribute,
                master_skill=self,
                acquired=self.acquired
                )
        self.master_skill = master_skill

    def add_variety(self, variety):
        """Append the input variety to the list of this skill's varieties, if
        the skill is multiple.

        Arguments:
        variety -- A variety of this skill.
        """
        try:
            self.varieties.append(variety)
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

    def get_specialization(self):
        """Return the specialization of the skill, if it exists."""
        if not self.invariant:
            return self.specialization
        else:
            warnings.warn("Non-specific skill.", Warning)

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
        elif (self.specialization is not None and
                self.specialization.is_usable()):
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

    def __init__(self, cost, base_rank=0, invariant=False):
        """Constructor.

        Arguments:
        cost -- Cost for activating the power.

        Keyword arguments:
        invariant -- True if the new attribute is an invariant (default False).
        base_rank -- Base rank of the new attribute (default 0).
        """
        Attribute.__init__(self, base_rank, invariant=invariant)
        self.cost = cost

    def get_cost(self):
        """Return the cost for activating the power."""
        return self.cost
