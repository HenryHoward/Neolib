""":mod:`Neoquest` -- Provides an interface for playing neoquest

.. module:: Neoquest
   :synopsis: Provides an interface for playing neoquest
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>
"""

import logging
from munch import Munch

from State import State
from Player import Player

MV_MODE = Munch(zip(['Normal', 'Hunting', 'Sneaking'], range(1, 4)))
NORMAL, EVIL, INSANE = 0, 1, 2  # difficulty codes
FIRE, ICE, SHOCK, SPECTRAL, LIFE = 1, 2, 3, 4, 5  # skill codes
DIR = Munch(zip(['NW', 'N', 'NE', 'W', 'E', 'SW', 'S', 'SE'], range(1,9)))

# OK, I'm gonna say this is a list of skill improvements to take. ie. ordered
DEFAULT_SKILL_BUILD = []
NQ_URL = 'http://www.neopets.com/games/neoquest/neoquest.phtml'


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

        # If we keep these two parameters updated, that'd be convenient.
        self._update()

    # Functions this should have:
    # - start game
    # - grind until (level)
    # - play/beat game
    # - beat milestones
    
    # We navigate the game by using the root url and query params.
    def _update(self, path='', params=None):
        self.page = self.usr.getPage(NQ_URL+path, params=params)
        self.state = State(self.page)
        self.player = Player(self.state)

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
        Shorthand variables: DIR dict.
        """
        self.action('action', action_value='move', movedir=direction)
        return self.state

    def movement_mode(self, mode):
        """Change movement mode:
        Possible values - 'Normal', 'Hunting', 'Sneaking'
        - 1, 2, 3
        Shorthand variables: MV_MODE dict.
        """
        if mode == self.player.movement_mode:
            logging.warn('Already in movement mode "{}"'.format(self.player.movement_mode))
        self.action('action', action_value='movetype', movetype=MV_MODE[mode])
        return self.state

    def attack(self, atk_type=0):
        """Just do a plain attack
        """
        # fields: 'fact' and 'type' (probably for different attack types)
        # basic moves are 'attack, 0', 'flee, 0', and 'noop, 0'
        attack_form = self.page.form(name='ff', method='post', action='neoquest.phtml')

        # Plain attack?
        attack_form['fact'] = 'attack' # attack, flee, noop, etc... (spell?)
        attack_form['type'] = atk_type # pretty sure this indicates "intensity/level" of attack
        attack_form.submit()
        self._update()
        return self.state

    def flee(self):
        """Attempt to flee from battle
        """
        attack_form = self.page.form(name='ff', method='post', action='neoquest.phtml')

        attack_form['fact'] = 'flee' # attack, flee, noop, etc... (spell?)
        attack_form['type'] = 0
        attack_form.submit()
        self._update()
        return self.state

    # NOTE/TODO: this is a pretty general use command...
    def transition(self):
        """ When to use:
         - When you've won a battle, to pass the 'You won!' screen
         - When you're entering battle, to pass the 'You are attacked by x' screen
         - When you've just leveled up, 'YOU GAIN A NEW LEVEL'
        """
        # NOTE: if i had to guess, end_fight is actually not necessary
        # (since it's only for, presumably, ending fights)
        end_fight_form = self.page.form(action='neoquest.phtml', method='post')
        end_fight_form['end_fight'] = 1
        end_fight_form.submit()
        self._update()
        return self.state

    def action(self, action_type, action_value=1, **kwargs):
        """Perform an 'action' in the game context.
         - action_type is the text name of the action to take
           (I've added a 'noop'/None type which moves in place)
         - action_value=1 indicates y/T
        """
        # If you've explicitly set it to None istead of '' for some reason
        if action_type is None or action_type.lower() == 'noop':
            action_type = ''

        params = {action_type: action_value}
        if kwargs: # params override kwargs
            kwargs.update(params) 
            params = kwargs
        self._update(params=params)
        return self.state

    def local_action(self, index=0):
        """Attempt to perform a local action based on the current state
         - specify the index to perform a specific, non-first action
        """
        if self.state.local_actions:
            # Don't forget to re-add the question mark!
            url_params = '?' + self.state.local_actions[index].param_string
        else:
            return 'No possible local actions'

        self._update(path=url_params) # Since it gives them url encoded.
        return self.state

    def auto_battle(self, threshold=5):
        """Try to auto battle. Call this when you first enter the battle splash
        """
        while self.state.mode != 'OVERWORLD':
            if self.state.mode == 'TRANSITION':
                self.transition()
                logging.warn('Transitioning...')
            elif self.state.mode == 'BATTLE':
                # battle loop: should only use a few basic criterion
                if self.player.current_health <= threshold:
                    # try to flee. this should work for now.. but i should think about using potions & stuff
                    logging.warn('Attempting to flee...')
                    self.flee()
                else:
                    logging.warn('Attacking...')
                    self.attack()

    def skills(self):
        """Access the skills menu - ie. see your skill levels"""
        state = self.action('action', action_value='skill')
        return state

    def skill_up(self, skill_code):
        """Use a skill code (1001, 3004, etc) and I'll try to apply it
        - only works if you HAVE a skill point free
        - only works if the skill is available wrt. the skill tree
        """
        state = self.action('action', action_value='skill', skillchoice=skill_code, confirm='1')
        return state
