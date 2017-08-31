""":mod:`Action` -- A class representing an in-game action in Neoquest

.. module:: Action
   :synopsis: A class representing an in-game action in Neoquest
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>

   :description: More specifically, a non-combat action, usually involving an NPC.
"""

import logging


class Action(object):
    # TODO/NOTE:
    # should be able to make an Action from also a form, maybe?
    def __init__(self, a_tag):
        self.param_string = a_tag.attrs['href'].split('?')[-1]
        self.description = a_tag.text

    def __str__(self):
        return self.description

    def __repr__(self):
        return '<{}: "{}">'.format(self.__class__, str(self))
