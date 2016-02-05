#! /usr/bin/env python3

class Value:
    """Base class for representing numerical values for characters and profiles
    in scox.

    Instance variables:
    __base_rank -- Initial rank of the value, expressed as an integer.
    __rank -- Rank of the value, expressed as an integer.
    """

    def __init__(self, base_rank):
        """Constructor.

        Arguments:
        base_rank -- Base rank of the new value.
        """
        self.__base_rank = rank
        self.__rank = 0

    def get_full_rank(self):
        """Return the full rank of the value.

        The full rank of the value equals the sum of its base rank with its
        rank.
        """
        return self.__rank + self.__base_rank

    def set_rank(self, rank):
        """Set the rank of the value."""
        self.__rank = rank

class Attribute(Value):
    """Value-derived class for representing character's attributes.

    Instance variables:
    __invariant -- Boolean value; True if the attribute's rank cannot be
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
        self.__invariant = invariant

    def increment_rank(self):
        """Increase the rank of the attribute by 1."""
        if not self.__invariant:
          self.__rank += 1

    def decrement_rank(self):
        """Decrease the rank of the attribute by 1."""
        if self.__rank > 0 and not self.__invariant:
            self.__rank -= 1

class Skill(Attribute):
    """Attribute-derived class for representing character's skills.

    Instance variables:
    __governing_attribute -- Attribute governing the skill base rank.
    __varieties -- List of skill varieties, if the skill is multiple.
    __specialization -- Skill instance representing a specialization, if the
        skill is specific.
    __master_skill -- Generic version of the skill; quite the opposite of
        specialization.
    """

    def __init__(self, governing_attribute=None, specific=False,
        multiple=False, invariant=False, master_skill=None):
        """Constructor.

        Keyword arguments:
        governing_attribute -- Governing attribute of the new skill (default
            None).
        specific -- Boolean value; True if the new skill is specific (default
            False).
        multiple -- Boolean value; True if the new skill is multiple (default
            False).
        invariant -- True if the new attribute is an invariant (default False).
        """
        self.__governing_attribute = governing_attribute
        self.__invariant = invariant
        if multiple:
            self.__varieties = []
        if specific:
            self.__specialization = Skill(
                governing_attribute=self.__governing_attribute,
                master_skill=self
                )
        if master_skill is not None:
            self.__master_skill = master_skill

    def compute_base_rank(self):
        """Compute the value of the skill's based rank base on the rank of its
        governing attribute, if any.
        """
        if self.__governing_attribute is not None:
            self.__base_rank = governing_attribute.get_full_rank() / 2
        else:
            self.__base_rank = 2
        # Specialization rank must be computed too, if any
        if self.__specialization is not None:
            self.__specialization.compute_base_rank()

    def increment_rank(self):
        """Increase the rank of the attribute by 1."""
        if not self.__invariant and (self.__specialization is None or
            self.__specialization.get_full_rank() > self.get_full_rank()):
          self.__rank += 1

    def decrement_rank(self):
        """Decrease the rank of the attribute by 1."""
        if self.__rank > 0 and not self.__invariant and (
            self.__master_skill is None or
            self.__master_skill.get_full_rank() < self.get_full_rank()):
            self.__rank -= 1
