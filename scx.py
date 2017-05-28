#! /usr/bin/env python3
# coding=utf-8

import scox.character as chc
import scox.export.cli as cli
import scox.export.serialize as srl
import scox.export.svg as svg

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
    if category == 'demon':
        folder = DEMON_PROFILE_PATH
    elif category == 'angel':
        folder = ANGEL_PROFILE_PATH
    else:
        folder = ARCHETYPE_PROFILE_PATH
    profile_list = []
    for f in os.listdir(folder):
        if f.endswith('.scx'):
            profile_list.append(f.split('.')[0].title())
    # compact printing
    profile_list.sort()
    it = iter(profile_list)
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
            profile = srl.load_from_pickle(file_path)
            if format == 'svg':
                sheet = 'INS.png' if profile.get_nature() == 'Demon'\
                    else 'MV.png'
                sheet_path = os.path.join(CHARACTER_SHEET_PATH, sheet)
                out_path = os.path.join(cfg.teams[cfg.selected],
                                        profile.get_name() + '.svg')
                svg.export_as_svg(profile, out_path, sheet_path)
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
    srl.export_as_pickle(new, filename)


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
        profile = srl.load_from_pickle(chc_path)
        if format == 'svg':
            sheet = 'INS.png' if profile.get_nature() == 'Demon' else 'MV.png'
            sheet_path = os.path.join(CHARACTER_SHEET_PATH, sheet)
            out_path = os.path.join(cfg.teams[cfg.selected], name + '.svg')
            svg.export_as_svg(profile, out_path, sheet_path)
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
            c = srl.load_from_pickle(file_path)
            clr = (Fore.RED if c.get_nature() == 'Demon' else Fore.CYAN)
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
        cli.print_cli(srl.load_from_pickle(file_path))
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
        profile = srl.load_from_pickle(file_path)
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
        srl.export_as_pickle(profile, file_path)
    else:
        print(name + " does not exist in selected team.")
