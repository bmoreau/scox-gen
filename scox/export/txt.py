#! /usr/bin/env python3
# coding=utf-8


def export_as_txt(profile, txt_file):
    """Export the character's profile to a formatted TXT file.

    Args:
        profile: an instance of scox.character.Character.
        txt_file: open TXT file with writing access.
    """
    # identity info
    txt_file.write(profile.get_name() + " - Grade " +
                   str(profile.get_level()) + " - " +
                   profile.get_superior() + "\n")
    # attributes
    txt_file.write("Attributs : ")
    export_attributes_as_txt(profile, txt_file)
    # side values
    txt_file.write("Valeurs annexes : ")
    export_values_as_txt(profile, txt_file)
    # skills
    txt_file.write("Talents : ")
    export_skills_as_txt(profile, txt_file)
    # powers
    txt_file.write("Pouvoirs : ")
    export_powers_as_txt(profile, txt_file)
    txt_file.write("\n")


def export_attributes_as_txt(profile, txt_file):
    """Write the input profile's attributes to the input TXT file.

    Args:
        profile: an instance of scox.character.Character.
        txt_file: open TXT file with writing access.
    """
    attrs = ""
    for a in profile.get_attributes().values():
        attrs += a.get_name() + " " + a.get_cli_rank().rstrip() + ", "
    txt_file.write(attrs.rstrip(', ') + "\n")


def export_powers_as_txt(profile, txt_file):
    """Write the input profile's powers to the input TXT file.

    Args:
        profile: an instance of scox.character.Character.
        txt_file: open TXT file with writing access.
    """
    pows = ""
    for p in profile.get_powers().values():
        pows += p.get_name()
        if not p.is_invariant():
            pows += (" " + p.get_cli_rank()).rstrip()
        pows += ", "
    txt_file.write(pows.rstrip(', ') + "\n")


def export_skills_as_txt(profile, txt_file):
    """Write the input profile's skills to the input TXT file.

    Args:
        profile: an instance of scox.character.Character.
        txt_file: open TXT file with writing access.
    """
    skills = ""
    skill_dict = {}
    skill_dict.update(profile.get_primary_skills())
    skill_dict.update(profile.get_exotic_skills())
    skill_dict.update(profile.get_secondary_skills())
    for s in skill_dict.values():
        if s.is_usable():
            skills += s.get_pretty_string() + ", "
    txt_file.write(skills.rstrip(", ") + "\n")


def export_values_as_txt(profile, txt_file):
    """Write the input profile's values to the input TXT file.

    Args:
        profile: an instance of scox.character.Character.
        txt_file: open TXT file with writing access.
    """
    vals = ""
    vals += (profile.get_side_values()['PP'].get_cli_rank() + " PP, " +
             profile.get_side_values()['PF'].get_cli_rank() + " PF, " +
             "BL " + profile.get_side_values()['BL'].get_cli_rank() +
             " / BG " + profile.get_side_values()['BG'].get_cli_rank() +
             " / BF " + profile.get_side_values()['BF'].get_cli_rank() +
             " / MS " + profile.get_side_values()['MS'].get_cli_rank() + "\n")
    txt_file.write(vals)
