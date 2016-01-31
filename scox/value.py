#! /usr/bin/env python3

class Value:
    """Base class for representing numerical values for characters and profiles
    in scox.

    Class attributes:
    __rank -- Rank of the value, expressed as an integer.
    """

    def Value(self, rank):
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
