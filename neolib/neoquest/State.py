""":mod:`State` -- A class representing the game state in Neoquest

.. module:: State
   :synopsis: A class representing the game state in Neoquest
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>
"""

import re

class State(object):
    """So this object should kind of keep-alive your progress/game state
    - should be able to save/load from file
    - should keep track of location (relative to start area within map, based on teh graph model I'll create
    - should keep track of skills? or at least refresh them each time you start a new session
    - should keep track of milestones in the game (bosses defeated, items collected)
    """
    OVERWORLD_REGEX = '\s*NeoQuest\s*(Name.*Sneaking)\s*Options\s*|\s*Leader\s*Board\s*(.*)'
    BATTLE_SPLASH_REGEX = '\s*NeoQuest\s*(.*)(You are.*)'
    BATTLE_REGEX = '\s*NeoQuest\s*(\w*.*Difficulty: [A-Z][a-z]+)(.*)<.*>(.*)'

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
        elif 'Attack' in self.raw_text:
            regex = State.BATTLE_REGEX
        else:
            regex = State.OVERWORLD_REGEX
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
