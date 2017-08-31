""":mod:`State` -- A class representing the game state in Neoquest

.. module:: State
   :synopsis: A class representing the game state in Neoquest
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>
"""

from munch import Munch
import re
import math
import logging


class State(object):
    """So this object should kind of keep-alive your progress/game state
    - should be able to save/load from file
    - should keep track of location (relative to start area within map, based on teh graph model I'll create
    - should keep track of skills? or at least refresh them each time you start a new session
    - should keep track of milestones in the game (bosses defeated, items collected)
    """
    OVERWORLD_REGEX = '\s*NeoQuest\s*(Name.*Sneaking)\s*Options\s*|\s*Leader\s*Board\s*(.*)'
    BATTLE_SPLASH_REGEX = '\s*NeoQuest\s*(.*)(You are.*)'
    END_FIGHT_REGEX = '\s*NeoQuest\s*(.*)(You defeated.*)'
    BATTLE_REGEX = '\s*NeoQuest\s*(\w*.*Difficulty: [A-Z][a-z]+)(.*)<.*>(.*)'
    ASCII_MAP = {
        'grassland': '.',
        'mountain': '^',
        'swamp': 'w',
        'forest': 'T',
        'city': 'X',
        'castle': '#',
        'hills': 'h',
        'desert': '_',
        'lupe': '@',
        'water': ' ',
        }
    MODES = Munch({
        'OVERWORLD': 'OVERWORLD',
        'MENU': 'MENU',
        'BATTLE': 'BATTLE',
        'TRANSITION': 'TRANSITION',
        })


    def __init__(self, page):
        """State is constructed from a Page"""
        source_div = page.find(
                "div", class_="contentModule phpGamesNonPortalView"
               ).find('div', class_='frame')
        self.src_div = source_div

        # NOTE: there's a single grosso unicode char
        self.raw_text = source_div.get_text().encode('ascii', 'ignore')
        if 'attacked by' in self.raw_text:
            regex = State.BATTLE_SPLASH_REGEX
            self.mode = State.MODES.TRANSITION
        elif 'defeated' in self.raw_text:
            regex = State.END_FIGHT_REGEX
            self.mode = State.MODES.TRANSITION
        elif 'Attack' in self.raw_text:
            regex = State.BATTLE_REGEX
            self.mode = State.MODES.BATTLE
        else:
            regex = State.OVERWORLD_REGEX
            self.mode = State.MODES.OVERWORLD
        self.match_data = re.findall(regex, re.sub('\n', ' ', self.raw_text), flags=re.DOTALL)

        # Clean up the results
        self.data = [a.strip() for m in self.match_data for a in m if a]

    def __str__(self):
        nice_data = [
                re.sub('View.*', '', stats)
                for stats in self.data
                ]
        nice_data = [
                re.sub('\.', '. ', flavor)
                for flavor in nice_data
                ]
        return '\n'.join(nice_data)

    def __repr__(self):
        return str(self)

    def _create_ascii_map(self):
        def url_to_ascii(img_url):
            terrain = img_url.split('/')[-1] # Remove path
            terrain = terrain.split('.')[0] # Remove extension
            if terrain.startswith('lupe_'):
                terrain = 'lupe'
            if 'water' in terrain: # untraversable terrain is highest pri?
                terrain = 'water'
            return State.ASCII_MAP.get(terrain, '?')

        """For debugging and console fun, let's create a nethack-kinda map!"""
        tiles = [
                i.attrs['src'] for i in
                self.src_div.find_all('img')
                if i['height']=='40' and i['width']=='40'
                ]

        ascii_map = []

        # I *could* hardcode this to 49 and 7 - but what's the fun in that?
        row_len = int(math.floor(math.sqrt(len(tiles))))
        for row_idx in range(len(tiles)/row_len):
            ascii_map.append(map(
                url_to_ascii,
                tiles[row_idx*row_len:(row_idx+1)*row_len]
                ))
        return ascii_map

    def _print_ascii_map(self, ascii_map):
        for row in ascii_map:
            print ''.join(row)

    def map(self):
        if self.mode != State.MODES.OVERWORLD:
            # TODO: use proper logging
            logging.warn("Can't create ascii map when not in overworld mode")
            return
        self._print_ascii_map(self._create_ascii_map())
