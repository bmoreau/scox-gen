#! /usr/bin/env python3

class Value:
    """Base class for representing numerical values for characters and profiles
    in scox.

    Instance variables:
    __rank -- Rank of the value, expressed as an integer.
    """

    def __init__(self, rank):
        """Constructor.

        Arguments:
        rank -- Rank of the new value.
        """
        self.__rank = rank

    def get_rank(self):
        """Return the rank of the value."""
        return self.__rank

    def set_rank(self, rank):
        """Set the rank of the value."""
        self.__rank = rank

def Attribute(Value):
    """Value-derived class for representing character's attributes.
    
    Methods:
    increment_rank -- Increase the rank of the attribute by 1.
    decrement_rank -- Decrease the rank of the attribute by 1.
    """

    def increment_rank(self):
        """Increase the rank of the attribute by 1."""
        self.__rank += 1

    def decrement_rank(self):
        """Decrease the rank of the attribute by 1."""
        if self.__rank > 0:
            self.__rank -= 1

def Skill(Attribute):
    """Attribute-derived class for representing character's skills.

    Instance variables:
    __governing_attribute -- Attribute governing the skill base rank.
    __specific -- Boolean value; true if the skill is specific.
    __multiple -- Boolean value; true if the skill is multiple.
    __specialization -- Skill instance representing a specialization, if the
        skill is specific.
    """

    def __init__(self, governing_attribute=None, specific=False,
        multiple=False, specialization=None):
      """Constructor.

      Keyword arguments:
      governing_attribute -- Governing attribute of the new skill (default
          None).
      specific -- Boolean value; True if the new skill is specific (default
          False).
      multiple -- Boolean value; True if the new skill is multiple (default
          False).
      specialization -- Specialization of the skill (default None).
      """
      self.__governing_attribute = governing_attribute
      self.__specific = specific
      self.__multiple = multiple
      self.__specialization = specialization
      if self.__governing_attribute is not None:
        self.__rank = governing_attribute.get_rank() / 2
      else:
        self.__rank = 2
