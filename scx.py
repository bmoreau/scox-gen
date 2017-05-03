#! /usr/bin/env python3
# coding=utf-8

import scox.character as chc
import os
import shutil
import json
import click


SCOX_HOME = os.path.join(os.path.expanduser('~'), '.scox-gen')
CONFIG_FILE = os.path.join(SCOX_HOME, 'config.json')


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
@click.pass_obj
def select(cfg, name):
    """Select an existing team."""
    if name in cfg.teams:
        with open(CONFIG_FILE, mode='w') as c:
            json.dump([name, cfg.teams], c)
    else:
        print(name + ' does not exist in current list of teams.')


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
@click.pass_obj
def ls(cfg):
    """Display the list of existing teams."""
    for k in cfg.teams.keys():
        print(k + " (" + cfg.teams[k] + ")")


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
    new = chc.Character(name, nature, archetype, superior)
    filename = name + '.pickle'
    filepath = os.path.join(cfg.teams[cfg.selected], filename)
    new.export_as_pickle(filepath)


@character.command()
@click.argument('name', type=click.STRING)
@click.confirmation_option(help='Skip the confirmation step.')
@click.pass_obj
def delete(cfg, name):
    """Delete an existing character."""
    filepath = os.path.join(cfg.teams[cfg.selected], name + '.pickle')
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print(name + " does not exist in selected team.")


@character.command()
@click.pass_obj
def ls(cfg):
    """Display the list of existing characters."""
    ignored = 0
    for i in os.listdir(cfg.teams[cfg.selected]):
        filepath = os.path.join(cfg.teams[cfg.selected], i)
        try:
            c = chc.load_from_pickle(filepath)
            print(c.get_name() + " - " + c.get_superior())
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
    filepath = os.path.join(cfg.teams[cfg.selected], name + '.pickle')
    if os.path.exists(filepath):
        chc.load_from_pickle(filepath).print_cli()
    else:
        print(name + " does not exist in selected team.")
