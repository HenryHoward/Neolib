""":mod:`Neoquest` -- Provides an interface for playing neoquest

.. module:: Neoquest
   :synopsis: Provides an interface for playing neoquest
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>
"""
NORMAL, EVIL, INSANE = 0, 1, 2  # difficulty codes
FIRE, ICE, SHOCK, SPECTRAL, LIFE = 1, 2, 3, 4, 5  # skill codes
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

    # Functions this should have:
    # - start game
    # - grind until (level)
    # - play/beat game
    # - beat milestones
    
    # We navigate the game by using the root url and query params.

    def start_game(self, difficulty=NORMAL, skill_build=None):
        """Start a new game with the given difficulty and skill build"""
        # TODO: Should skill_build be a class, or a dict?
        if skill_build is None:
            skill_build = DEFAULT_SKILL_BUILD

        # Create new game
        # NOTE/TODO: I can try to use postData to try to set query params.
        # Else- need to strformat them onto the URL. which is fine.
        result = self.action('create', game_diff=difficulty)

    def action(self, action_type, action_value=1, **kwargs):
        if action_type is None or action_type.lower() == 'noop':
            action_type = ''
        if action_value is None:
            action_value = ''
        params = {action_type: action_value}

        if kwargs:
            params.update(kwargs)
        return self.usr.getPage(NQ_URL, postData={action_type: action_value})

    def parse_game_state(self, page):
        game_state = page.find(
                "div", class_="contentModule phpGamesNonPortalView"
               ).find('div', class_='frame')
        return game_state
