""":mod:`Player` -- A class representing an in-game action in Neoquest

.. module:: Player
   :synopsis: A class representing the player in Neoquest
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>

   :description: Player stats, level, items/equipment, etc. Separate and
   more persistent than the state.
"""

import logging


class Player(object):
    def __init__(self, state):
        """src_div as in the same one used for States"""
        self._update(state)


    def __str__(self):
        return self.description


    def _update(self, state):
        src_div = state.src_div
        sdc = src_div.contents[2].contents
        # based on in-battle, the userful player info is like:
        player_stuff = sdc[:18]
        self.name = sdc[1].string
        self.level = int(sdc[3].string)
        self.current_health = int(sdc[5].string)
        self.max_health = int(sdc[6][1:]) # does NOT need .string because it is a NavigableString
        self.exp = int(sdc[11].string)

        # In overworld, it's 16. in battle, it's 17? wth?
        # could load it once, and not udpate since it doesn't change unless
        # you explicitly change it.
        self.difficulty = sdc[17].string
