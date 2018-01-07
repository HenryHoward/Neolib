""":mod:`Player` -- A class representing an in-game action in Neoquest

.. module:: Player
   :synopsis: A class representing the player in Neoquest
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>

   :description: Player stats, level, items/equipment, etc. Separate and
   more persistent than the state.
"""

import logging


class Player(object):
    """
    Player should actually encompass things that change less frequently than the state.
    Stuff that changes less frequently, like HP, MP (?), inventory (?), skill tree, EXP
    - movement mode? sure, whatever...
    """
    def __init__(self, state):
        self._update(state)


    def __str__(self):
        return self.description


    def _update(self, state):
        sdc = [t for t in state.src_div.contents[2].contents if t.name != 'table']
        self.sdc = sdc

        # based on in-battle, the userful player info is like:
        self.name = sdc[1].string
        self.level = int(sdc[3].string)
        self.current_health = int(sdc[5].string)
        self.max_health = int(sdc[6][1:]) # does NOT need .string because it is a NavigableString
        self.exp = int(filter(lambda c: c.isdigit(), sdc[11].string))

        # TODO: get this to work consistently
        # In overworld, it's 16. in battle, it's 17? wth?
        # could load it once, and not udpate since it doesn't change unless
        # you explicitly change it.
        self.difficulty = sdc[16].string if state.mode == 'BATTLE' else sdc[17]
        # There are separator text elements '|', and if NOT selected, tag is 'a'
        if state.mode == 'OVERWORLD':
            self.movement_mode = [t for t in sdc[22:27] if t.name == 'b'][0].string
