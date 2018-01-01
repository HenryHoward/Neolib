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
        player_stuff = sdc[:17]
        self.name = sdc[1].text
        self.level = int(sdc[3].text)
        self.current_health = int(sdc[5].text)
        self.max_health = int(sdc[6][1:]) # does NOT need .text because it is a NavigableString
        self.exp = int(sdc[11].text)
        self.difficulty = sdc[16].text
