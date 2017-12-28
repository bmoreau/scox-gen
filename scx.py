#! /usr/bin/env python3
# coding=utf-8

import scox.character as chc
import os
import shutil
import json
import click
from colorama import Fore, Style

SCOX_HOME = os.path.join(os.path.expanduser('~'), '.scox-gen')
CONFIG_FILE = os.path.join(SCOX_HOME, 'config.json')
ARCHETYPE_PROFILE_PATH = \
    os.path.join(os.path.dirname(__file__), 'scox', 'profiles', 'archetypes')
ANGEL_PROFILE_PATH = \
    os.path.join(os.path.dirname(__file__), 'scox', 'profiles', 'angels')
DEMON_PROFILE_PATH = \
    os.path.join(os.path.dirname(__file__), 'scox', 'profiles', 'demons')
CHARACTER_SHEET_PATH = \
    os.path.join(os.path.dirname(__file__), 'scox', 'sheets')


class Config:
    def __init__(self):
        if os.path.exists(CONFIG_FILE):
            # load existing config file
            with open(CONFIG_FILE, mode='r') as c:
                state = json.load(c)
                self.selected = state[0]
                self.teams = state[1]
        else:
            # create a new empty 'default' folder
            fd = os.path.join(SCOX_HOME, 'default')
            os.makedirs(fd)
            self.selected = 'default'
            self.teams = {'default': os.path.join(SCOX_HOME, 'default')}
            # create a new config file
            with open(CONFIG_FILE, mode='w') as c:
                json.dump([self.selected, self.teams], c)


@click.group()
@click.pass_context
def scx(ctx):
    """A character generator for INS-MV 4."""
    ctx.obj = Config()


@scx.command()
@click.argument('category', type=click.Choice(['demon', 'angel', 'arch']))
def profiles(category):
    """Display the list of all available profiles for a given category."""
    profile_ls = get_profile_list(category)
    it = iter(profile_ls)
    for i in it:
        try:
            print('{:<30}{}'.format(i, next(it)))
        except StopIteration:
            print('{:<30}'.format(i))


@scx.group()
def team():
    """Commands for manipulating teams."""
    pass


@team.command()
@click.option('--name', prompt='Name', type=click.STRING,
              help='Name of the created team.')
@click.option('--location', prompt='Team folder location',
              type=click.Path(file_okay=False, writable=True),
              default=SCOX_HOME, help='Where the team folder should be '
                                      'located.')
@click.pass_obj
def create(cfg, name, location):
    """Create a new team and select it."""
    # new team folder is created
    new_dir = os.path.join(location, name)
    os.makedirs(new_dir)
    # config file is updated, new team is selected
    cfg.teams[name] = new_dir
    with open(CONFIG_FILE, mode='w') as c:
        json.dump([name, cfg.teams], c)


@team.command()
@click.argument('name', type=click.STRING)
@click.confirmation_option(help='Skip the confirmation step.')
@click.pass_obj
def delete(cfg, name):
    """Delete an existing team."""
    if name in cfg.teams:
        location = cfg.teams.pop(name)
        try:
            shutil.rmtree(location)
            print("Team '" + name + "' deleted.")
        except FileNotFoundError:
            print(location + " not found. Entry removed from the list of "
                             "teams.")
        active = None
        if cfg.selected == name:
            for i in cfg.teams.keys():
                active = i
                break
        else:
            active = cfg.selected
        print("Selected team: " + str(active))
        with open(CONFIG_FILE, mode='w') as c:
            json.dump([active, cfg.teams], c)
    else:
        print(name + ' does not exist in current list of teams.')


@team.command()
@click.option('--format', type=click.Choice(['svg', 'txt']),
              help='Format of the exported file(s).', default='svg')
@click.pass_obj
def export(cfg, format):
    """Export all the character's profiles in the selected team as SVG or
    TXT files."""
    ignored = 0
    for i in os.listdir(cfg.teams[cfg.selected]):
        file_path = os.path.join(cfg.teams[cfg.selected], i)
        try:
            profile = chc.load_from_pickle(file_path)
            if format == 'svg':
                sheet = 'INS.png' if profile.get_nature() == 'Demon'\
                    else 'MV.png'
                sheet_path = os.path.join(CHARACTER_SHEET_PATH, sheet)
                out_path = os.path.join(cfg.teams[cfg.selected],
                                        profile.get_name() + '.svg')
                profile.export_as_svg(out_path, sheet_path)
            else:
                pass
        except Exception:
            ignored += 1
    if ignored > 0:
        print(str(ignored) + " file(s) could not be loaded in selected team "
                             "folder.")


@team.command()
@click.pass_obj
def ls(cfg):
    """Display the list of existing teams."""
    for k in cfg.teams.keys():
        print(k + " (" + cfg.teams[k] + ")")


@team.command()
@click.argument('name', type=click.STRING)
@click.pass_obj
def select(cfg, name):
    """Select an existing team."""
    if name in cfg.teams:
        with open(CONFIG_FILE, mode='w') as c:
            json.dump([name, cfg.teams], c)
    else:
        print(name + ' does not exist in current list of teams.')


@scx.group()
def character():
    """Commands for manipulating characters."""
    pass


@character.command()
@click.option('--name', type=click.STRING, prompt='Name',
              help='Name of the character. Be creative.')
@click.option('--nature', type=click.Choice(['angel', 'demon']),
              default='demon', prompt='Nature',
              help='Nature of the character.')
@click.option('--superior', default="Scox", prompt='Superior',
              help='Hierarchical superior of the character. The corresponding'
                   'profile for attributes, powers and skills applies.')
@click.option('--archetype', default="Corrupteur", prompt='Archetype',
              help='Archetype of the character.')
@click.pass_obj
def create(cfg, name, nature, superior, archetype):
    """Create a new character."""
    archetype = os.path.join(ARCHETYPE_PROFILE_PATH,
                             archetype.lower() + '.scx')
    if nature == 'demon':
        superior = os.path.join(DEMON_PROFILE_PATH, superior.lower() + '.scx')
    else:
        superior = os.path.join(ANGEL_PROFILE_PATH, superior.lower() + '.scx')
    new = chc.Character(name, nature, archetype, superior)
    filename = name + '.pickle'
    filename = os.path.join(cfg.teams[cfg.selected], filename)
    new.export_as_pickle(filename)


@character.command()
@click.argument('name', type=click.STRING)
@click.confirmation_option(help='Skip the confirmation step.')
@click.pass_obj
def delete(cfg, name):
    """Delete an existing character."""
    filename = os.path.join(cfg.teams[cfg.selected], name + '.pickle')
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(name + " does not exist in selected team.")


@character.command()
@click.argument('name', type=click.STRING)
@click.option('--format', type=click.Choice(['svg', 'txt']),
              help='Format of the exported file.', default='svg')
@click.pass_obj
def export(cfg, name, format):
    """Export the selected character's profile as an SVG or a TXT file."""
    chc_path = os.path.join(cfg.teams[cfg.selected], name + '.pickle')
    if os.path.exists(chc_path):
        profile = chc.load_from_pickle(chc_path)
        if format == 'svg':
            sheet = 'INS.png' if profile.get_nature() == 'Demon' else 'MV.png'
            sheet_path = os.path.join(CHARACTER_SHEET_PATH, sheet)
            out_path = os.path.join(cfg.teams[cfg.selected], name + '.svg')
            profile.export_as_svg(out_path, sheet_path)
        else:
            pass
    else:
        print(name + " does not exist in selected team.")


@character.command()
@click.pass_obj
def ls(cfg):
    """Display the list of existing characters."""
    ignored = 0
    for i in os.listdir(cfg.teams[cfg.selected]):
        file_path = os.path.join(cfg.teams[cfg.selected], i)
        try:
            c = chc.load_from_pickle(file_path)
            clr = (Fore.RED if c.get_nature() == 'Demon' else Fore.LIGHTBLUE_EX)
            print(clr + Style.BRIGHT + c.get_name() +
                  Style.NORMAL + " - " + c.get_superior() +
                  Style.RESET_ALL)
        except Exception:
            ignored += 1
    if ignored > 0:
        print(str(ignored) + " file(s) could not be loaded in selected team "
                             "folder.")


@character.command()
@click.argument('name', type=click.STRING)
@click.pass_obj
def show(cfg, name):
    """Display the profile of an existing character."""
    file_path = os.path.join(cfg.teams[cfg.selected], name + '.pickle')
    if os.path.exists(file_path):
        print_cli(chc.load_from_pickle(file_path))
    else:
        print(name + " does not exist in selected team.")


@character.group()
def edit():
    """Commands for editing characters."""
    pass


@edit.command()
@click.argument('name', type=click.STRING)
@click.pass_obj
def skills(cfg, name):
    """Edit the character's specializations and skill varieties."""
    file_path = os.path.join(cfg.teams[cfg.selected], name + '.pickle')
    if os.path.exists(file_path):
        profile = chc.load_from_pickle(file_path)
        for p in profile.get_primary_skills().values():
            if p.is_usable() and p.is_specific():
                new = click.prompt(
                    p.get_name(), default=p.get_specialization().get_name())
                p.get_specialization().set_name(new)
        for s in profile.get_secondary_skills().values():
            if s.is_usable():
                if s.is_specific():
                    new = click.prompt(
                        s.get_name(), default=s.get_specialization().get_name())
                    s.get_specialization().set_name(new)
                elif s.is_multiple():
                    for v in range(len(s.get_varieties())):
                        s.get_varieties()[v] = click.prompt(
                            s.get_name(), s.get_varieties()[v])
        profile.export_as_pickle(file_path)
    else:
        print(name + " does not exist in selected team.")


def print_cli(chc_profile):
    """Print the character's complete profile to the command line."""
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
    """Return the last usable skill contained by the input dictionary.

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


def get_profile_list(profile_type):
    """Return the requested list of available profiles.

    Args:
        profile_type: a string value in 'angel', 'demon' or 'arch'.

    Returns: the alphabetically ordered list of profiles corresponding to the
    input profile_type.
    """
    if profile_type == 'demon':
        folder = DEMON_PROFILE_PATH
    elif profile_type == 'angel':
        folder = ANGEL_PROFILE_PATH
    else:
        folder = ARCHETYPE_PROFILE_PATH
    profile_list = []
    for f in os.listdir(folder):
        if f.endswith('.scx'):
            profile_list.append(f.split('.')[0].title())
    profile_list.sort()
    return profile_list
