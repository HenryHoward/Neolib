""":mod:`Neoquest` -- Provides an interface for playing neoquest

.. module:: Neoquest
   :synopsis: Provides an interface for playing neoquest
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>
"""

from munch import Munch

NORMAL, EVIL, INSANE = 0, 1, 2  # difficulty codes
FIRE, ICE, SHOCK, SPECTRAL, LIFE = 1, 2, 3, 4, 5  # skill codes
DIR = Munch(zip(['NW', 'N', 'NE', 'W', 'E', 'SW', 'S', 'SE'], range(1,9)))
NQ_URL = 'http://www.neopets.com/games/neoquest/neoquest.phtml'

from State import State

class Neoquest(object):

    """Provides an interface for playing neoquest

    Attributes

    Initialization

    Example
      >>> nq = Neoquest(usr)
      >>> nq.grind_until(level=25)  # or sth like that
    """

    usr = None

    def __init__(self, usr):
        self.usr = usr

    # Functions this should have:
    # - start game
    # - grind until (level)
    # - play/beat game
    # - beat milestones
    
    # We navigate the game by using the root url and query params.

    def start_game(self, difficulty=NORMAL, skill_build=None):
        """Start a new game with the given difficulty and skill build"""
        # TODO: Should skill_build be a class, or a dict?
        # NOTE: does nothing so far
        if skill_build is None:
            skill_build = DEFAULT_SKILL_BUILD

        # Create new game
        result = self.action('create', game_diff=difficulty)

    def move(self, direction=''):
        """Move one step in the given direction. If no direction is given, move in place.
        """
        params = {'action': 'move', 'movedir': direction}
        return State(self.usr.getPage(NQ_URL, params=params))

    def attack(self):
        """Just do a plain attack
        """
        # TODO: NOT DONE - needs to submit a form on the page
        # form name : ff
        # fields: 'fact' and 'type' (probably for different attack types)
        # basic moves are 'attack, 0', 'flee, 0', and 'noop, 0'


    # This doesn't even work how I want it to. I think it works for setting options.
    # (movetype, etc.)
    def action(self, action_type, action_value=1, **kwargs):
        """Perform an 'action' in the game context.
         - action_type is the text name of the action to take
           (I've added a 'noop'/None type which moves in place)
         - action_value=1 indicates y/T
         - kwargs are passed thru onto params
        """
        if action_type is None or action_type.lower() == 'noop':
            action_type = ''

        # If you've explicitly set it to None istead of '' for some reason
        if action_value is None:
            action_value = ''

        params = {action_type: action_value}
        if kwargs:
            params.update(kwargs)
        return State(self.usr.getPage(NQ_URL, params=params))
