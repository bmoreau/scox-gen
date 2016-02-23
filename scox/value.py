#! /usr/bin/env python3

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

    def get_full_rank(self):
        """Return the full rank of the value.

        The full rank of the value equals the sum of its base rank with its
        rank.
        """
        return self.rank + self.base_rank

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

    def get_CLI_rank(self):
        """Return the real rank of the represented attribute as a string of
        characters.
        """
        rank = str(int(self.get_real_rank()))
        if self.get_full_rank()%2 != 0:
            rank += '+'
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
        multiple=False, invariant=False, master_skill=None, acquired=False):
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
        if multiple:
            self.varieties = []
        if specific:
            self.specialization = Skill(
                governing_attribute=self.governing_attribute,
                master_skill=self,
                acquired=self.acquired
                )
        if master_skill is not None:
            self.master_skill = master_skill

    def compute_base_rank(self):
        """Compute the value of the skill's based rank base on the rank of its
        governing attribute, if any.
        """
        if self.governing_attribute is not None:
            self.base_rank = self.governing_attribute.get_full_rank() / 2
        elif not self.invariant:
            self.base_rank = 2

    def increment_rank(self):
        """Increase the rank of the attribute by 1."""
        if not self.invariant and (self.specialization is None or
            self.specialization.get_full_rank() > self.get_full_rank()):
          self.rank += 1

    def decrement_rank(self):
        """Decrease the rank of the attribute by 1."""
        if self.rank > 0 and not self.invariant and (
            self.master_skill is None or
            self.master_skill.get_full_rank() < self.get_full_rank()):
            self.rank -= 1
