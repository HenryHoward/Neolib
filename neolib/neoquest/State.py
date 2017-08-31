""":mod:`State` -- A class representing the game state in Neoquest

.. module:: State
   :synopsis: A class representing the game state in Neoquest
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>
"""

from munch import Munch
import re
import math
import logging

from Action import Action

def is_br(bs_tag):
    try:
        return bs_tag.is_empty_element
    except AttributeError:
        return False


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
        'TALK': 'TALK',
        'BATTLE': 'BATTLE',
        'TRANSITION': 'TRANSITION',
        })


    def __init__(self, page):
        """State is constructed from a Page"""
        source_div = page.find(
                "div", class_="contentModule phpGamesNonPortalView"
               ).find('div', class_='frame')
        self.src_div = source_div
        self.local_actions = []

        # NOTE: there's a single grosso unicode char (for some state)
        self.raw_text = source_div.get_text().encode('ascii', 'ignore')
        if 'attacked by' in self.raw_text:
            regex = State.BATTLE_SPLASH_REGEX
            self.mode = State.MODES.TRANSITION
            self.match_data = re.findall(regex, re.sub('\n', ' ', self.raw_text), flags=re.DOTALL)

            # Clean up the results
            self.data = [a.strip() for m in self.match_data for a in m if a]
        elif 'defeated' in self.raw_text:
            regex = State.END_FIGHT_REGEX
            self.mode = State.MODES.TRANSITION
            self.match_data = re.findall(regex, re.sub('\n', ' ', self.raw_text), flags=re.DOTALL)

            # Clean up the results
            self.data = [a.strip() for m in self.match_data for a in m if a]
        elif 'Attack' in self.raw_text:
            regex = State.BATTLE_REGEX
            self.mode = State.MODES.BATTLE

            self.match_data = re.findall(regex, re.sub('\n', ' ', self.raw_text), flags=re.DOTALL)

            # Clean up the results
            self.data = [a.strip() for m in self.match_data for a in m if a]

        # TODO: is 'talk' screen part of overworld? Not really...
        elif 'say' in self.raw_text.lower():
            print("I AM IN THE TALK MODE, so at least there's that")
            self.mode = State.MODES.TALK
            self.data, self.local_actions = self._parse_talk(self.src_div)

        else:
            regex = State.OVERWORLD_REGEX
            self.mode = State.MODES.OVERWORLD
            self.data, self.local_actions = self._parse_overworld(self.src_div)

    def __str__(self):
        # nice_data = [
        #         re.sub('View.*', '', stats)
        #         for stats in self.data
        #         ]
        # nice_data = [
        #         re.sub('\.', '. ', flavor)
        #         for flavor in nice_data
        #         ]
        return ' '.join(self.data)

    def __repr__(self):
        return str(self)

    def _parse_overworld(self, src_div):
        content_table = src_div.find_all('table')[-1]
        content_row = content_table.find_all('tr')[-1]
        content_cells = content_row.find_all('td')
        content = [list(c.children) for c in content_cells]
        content = map(lambda l: filter(lambda t: not is_br(t), l), content)
        content = [item for sublist in content for item in sublist]

        # NOTE/TODO: perhaps, convert the "a" tags into some meaningful little pieces
        # of data???
        local_actions = [Action(a) for a in content if a.name=='a']
        content = map(
                lambda c: c.text
                if (not type(c) == unicode and hasattr(c, 'text'))
                else c,
                content)
        return content, local_actions

    def _parse_talk(self, src_div):
        content = src_div.find('div', attrs={'align':'center'})
        content = list(content.children)
        content = filter(lambda t: not is_br(t), content)

        local_actions = [
                Action(a) for a in content
                if ((not type(a) == unicode) and (a.name=='a'))
                ]
        content = map(
                lambda c: c.text.encode('ascii', 'ignore')
                if (not type(c) == unicode and hasattr(c, 'text'))
                else c,
                content)
        return content, local_actions

    def _parse_battle(self, src_div):
        pass

    # Let's hope 1 function could cover both of these:
    def _parse_transition(self, src_div):
        pass


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
