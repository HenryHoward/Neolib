""":mod:`State` -- A class representing the game state in Neoquest

.. module:: State
   :synopsis: A class representing the game state in Neoquest
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>
"""

from collections import OrderedDict
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
    OPTIONS_REGEX = '\s*MUSIC SETTINGS\s*'
    SKILLS_REGEX = '\s*'
    INVENTORY_REGEX = '\s*'
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
        'OPTIONS': 'OPTIONS',
        'SKILLS': 'SKILLS',
        'INVENTORY': 'INVENTORY',
        })


    def __init__(self, page):
        """State is constructed from a Page"""
        self.src_div = page.find(
                "div", class_="contentModule phpGamesNonPortalView"
               ).find('div', class_='frame')
        self.local_actions = []
        self.tiles = [i for i in page.find_all('img') if
            i.attrs.get('height', 0) == "40" and
            i.attrs.get('width', 0) == "40"
        ]

        # NOTE: there's a single grosso unicode char (for some state)
        self.raw_text = self.src_div.get_text().encode('ascii', 'ignore')
        #  - looks like src_div has 2 parts: "before the center tag, and after"
        if 'You are attacked by' in self.raw_text:
            regex = State.BATTLE_SPLASH_REGEX
            self.mode = State.MODES.TRANSITION
            self.match_data = re.findall(regex, re.sub('\n', ' ', self.raw_text), flags=re.DOTALL)

            # Clean up the results
            self.data = [a.strip() for m in self.match_data for a in m if a]
        elif 'defeated' in self.raw_text:
            regex = State.END_FIGHT_REGEX
            self.mode = State.MODES.TRANSITION
            self.match_data = re.findall(regex, re.sub('\n', ' ', self.raw_text), flags=re.DOTALL)
            self.data = [a.strip() for m in self.match_data for a in m if a]

        elif 'Attack' in self.raw_text:
            regex = State.BATTLE_REGEX
            self.mode = State.MODES.BATTLE
            self.match_data = re.findall(regex, re.sub('\n', ' ', self.raw_text), flags=re.DOTALL)
            self.data = [a.strip() for m in self.match_data for a in m if a]

        # TODO: is 'talk' screen part of overworld? Not really...
        elif 'say' in self.raw_text.lower():
            self.mode = State.MODES.TALK
            self.data, self.local_actions = self._parse_talk(self.src_div)

        elif 'MUSIC SETTINGS' in self.raw_text:
            self.mode = State.MODES.OPTIONS
            self.data, self.local_actions = self._parse_options(self.src_div)

        elif 'information about specific skills' in self.raw_text:
            self.mode = State.MODES.SKILLS
            self.data, self.local_actions = self._parse_skills(self.src_div)

        else:
            regex = State.OVERWORLD_REGEX
            self.mode = State.MODES.OVERWORLD
            self.data, self.local_actions = self._parse_overworld(self.src_div)

    def __str__(self):
        text = ' '.join(self.data)
        actions = '\n'.join([' - {}'.format(a.description) for a in self.local_actions])
        return '\n'.join([text, actions])

    def __repr__(self):
        return str(self)

    def _parse_overworld(self, src_div):
        content_table = src_div.find_all('table')[-1]
        content_row = content_table.find_all('tr')[-1]
        content_cells = content_row.find_all('td')
        content = [list(c.children) for c in content_cells]
        content = map(lambda l: filter(lambda t: not is_br(t), l), content)
        content = [item for sublist in content for item in sublist]

        # Things you can DO at the place you're in:
        local_actions = [Action(a) for a in content if a.name=='a']
        # Description/info about the place you're in:
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
    # - enter battle
    # - leave battle
    # well, i know them by the state regex thing but...
    # i dont' really like that.
    def _parse_transition(self, src_div):
        try:
            return self._parse_talk(src_div)
        except:
            match_data = re.findall(regex, re.sub('\n', ' ', self.raw_text), flags=re.DOTALL)
            data = [a.strip() for m in match_data for a in m if a]
            return data, ['Continue thru transition']

    def _parse_options(self, src_div):
        match_data = re.findall(regex, re.sub('\n', ' ', self.raw_text), flags=re.DOTALL)
        data = [a.strip() for m in match_data for a in m if a]
        return data, ["Stupid settings that you don't need"]

    def _parse_skills(self, src_div):
        sdc = src_div.contents[2]

        # this is stupid - also is not presetn if you have no points to spend. :|
        how_many = re.findall('.*(You currently have.*to spend\.).*', sdc.get_text(), flags=re.DOTALL)
        how_many = how_many[0] if how_many else '0'
        skill_tbs = sdc.find('table').find_all('table')

        skills = {}
        for tb in skill_tbs:
            school = tb.contents[0].get_text().split('  ')[-1]
            raw_levels = [t for t in tb.descendants
                    # skill name
                    if t.name =='font' or
                    # skill value, exclude first thing
                    (t.name =='td' and
                        t.attrs.get('align') == 'center' and
                        t.attrs.get('width') != '40'
                        )]
            skills[school] = OrderedDict()
            for i in range(0, len(raw_levels), 2):
                skills[school][raw_levels[i].get_text()] = raw_levels[i+1].get_text()

        # Things you can DO at the place you're in: ie. potentially level up skills
        local_actions = []
        # Description/info about the place you're in:
        content = [', '.join('{}: {}'.format(k,v) for k,v in sk.items()) for _,sk in skills.items()]
        content.insert(0, how_many)
        return content, local_actions

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
        tiles = [i.attrs['src'] for i in self.tiles]
        assert len(tiles) == 49

        ascii_map = []

        row_len = int(math.floor(math.sqrt(len(tiles))))
        row_len = 7

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
