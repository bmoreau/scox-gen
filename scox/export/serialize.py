#! /usr/bin/env python3
# coding=utf-8

import pickle


def export_as_pickle(profile, path):
    """Serialize the character as a pickle file.

    Args:
        profile: an instance of scox.character.Character.
        path: path to a folder where to write the resulting pickle file.
    """
    with open(path, mode='wb') as f:
        pickle.dump(profile, f)


def load_from_pickle(filepath):
    """Load a Character instance from a pickle file.

    Args:
        filepath: path to a pickle file containing character information.

    Returns: a Character instance.
    """
    with open(filepath, mode='rb') as f:
        c = pickle.load(f)
        return c
