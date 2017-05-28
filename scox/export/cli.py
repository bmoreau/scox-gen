#! /usr/bin/env python3
# coding=utf-8


def print_cli(chc_profile):
    """Print the character's complete profile to the command line.

    Args:
        chc_profile: an instance of class scox.character.Character.
    """
    print("\n")
    print("\u250C\u2500\u2500 " +
          chc_profile.get_name() +
          " \u2500 " +
          "Grade " +
          str(chc_profile.get_level()) +
          " \u2500 " +
          chc_profile.get_superior()
          )
    print("\u2502")
    print("\u251c\u2500\u2500 " + "Attributs" +
          " \u2500\u2500\u2500\u2500\u2500"
          "\u2500\u2500\u2500\u2500\u2500\u2500 " +
          "Valeurs annexes")
    print_attributes(chc_profile)
    print("\u2502")
    print("\u251c\u2500\u2500 " +
          "Talents principaux")
    print_skills(chc_profile.get_primary_skills())
    print("\u2502")
    print("\u251c\u2500\u2500 " +
          "Talents exotiques")
    print_skills(chc_profile.get_exotic_skills())
    print("\u2502")
    print("\u251c\u2500\u2500 " +
          "Talents secondaires")
    print_skills(chc_profile.get_secondary_skills())
    print("\u2502")
    print("\u2514\u2500\u2500 " +
          "Pouvoirs")
    print_powers(chc_profile.get_powers())
    print("\n")


def print_attributes(chc_profile):
    """Format and print the input character's attributes and side values.

    Args:
        chc_profile: an instance of scox.character.Character.
    """
    attributes = chc_profile.get_attributes()
    values = chc_profile.get_side_values()
    for a, s in zip(attributes.keys(), values.keys()):
        attr = format_attribute(
            attributes[a].get_name(), attributes[a].get_cli_rank(), 14)
        side = format_attribute(s, values[s].get_cli_rank(), 14)
        if a != 'Foi':
            print('\u2502   \u251c\u2500\u2500 ' + attr +
                  '    \u251c\u2500\u2500 ' + side)
        else:
            print('\u2502   \u2514\u2500\u2500 ' + attr +
                  '    \u2514\u2500\u2500 ' + side)


def print_powers(power_set):
    """Format and print a power set.

    Args:
        power_set: a dictionary of scox.value.Power instances.
    """
    powers = [p for p in power_set.keys()]
    for p in power_set:
        br = "\u251C"
        if p == powers[-1]:
            br = "\u2514"
        print("    " + br + "\u2500\u2500 " +
              format_attribute(p, power_set[p].get_cli_rank(), 37))


def print_skills(skill_set):
    """Format and print a skill set.

    Args:
        skill_set: a dictionary of scox.value.Skill instances.
    """
    last = get_last_usable_skill(skill_set)
    for s in skill_set:
        sk = skill_set[s]
        if sk.is_usable():
            br = "\u251c"  # branch character
            if s == last:
                br = "\u2514"
            print("\u2502   " + br + "\u2500\u2500 " +
                  format_attribute(sk.get_name(), sk.get_cli_rank(), 37))
            if sk.is_specific():
                if s == last:
                    spacing = " "
                else:
                    spacing = "\u2502"
                print("\u2502   " + spacing + "   \u2514\u2500\u2500 " +
                      format_attribute(
                          sk.get_specialization().get_name(),
                          sk.get_specialization().get_cli_rank(), 33)
                      )
            elif sk.is_multiple():
                if s == last:
                    spacing_m = " "
                else:
                    spacing_m = "\u2502"
                for v in sk.varieties:
                    br_m = "\u251c"  # branch character
                    if v == sk.varieties[-1]:
                        br_m = "\u2514"
                    print("\u2502   " + spacing_m + "   " + br_m +
                          "\u2500\u2500 " + v)


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


def get_last_usable_skill(skill_dict):
    """Returns the last usable skill contained by the input dictionary.

    Args:
        skill_dict: an ordered dictionary with scox.value.Skill objects as
        values.

    Returns: the last usable skill in skill_dict.
    """
    usable = []
    for s in skill_dict.keys():
        if skill_dict[s].is_usable():
            usable.append(s)
    if len(usable) > 0:
        return usable[-1]
    else:
        return None
