"""Texas Hold'Em Game Engine"""
from texas_hold_em import *

class Menu:
    """Menu system for starting and running Texas Hold'Em."""
    user_input = False
    menu_text = ''

    def __init__(self, menu_text: str | list[str], user_input_prompt: str | None = None):
        if isinstance(menu_text, str):
            self.menu_text = menu_text
        elif isinstance(menu_text, list):
            for item in menu_text:
                self.menu_text += item + '\n'
        self.user_input_prompt = user_input_prompt
        if self.user_input_prompt is not None:
            self.user_input = True

    def __call__(self):
        """Display menu text and get user input if prompt is given."""
        self.display()
        return self.get_user_input()

    def get_user_input(self):
        """Get user input."""
        if self.user_input:
            return input(self.user_input_prompt)

    def display(self):
        """Display Menu text to console."""
        print(self.menu_text)

class TexasHoldEmEngine:
    """Game Engine for Texas Hold'Em card game."""
    game_running = False
    engine_running = True

    def __init__(self, players: list[PlayerTexasHoldEm] | None = None):
        """Create players and their chips first, add them to a list,
        then create the Game Engine object using the list.
        
        Shortcuts for accessing objects:
        self.table --------------> Table
        self.revealed_cards -----> Table.revealed_cards
        self.players ------------> Table.players
        self.deck ---------------> Table.deck
        self.cards --------------> Table.deck.cards
        self.pool ---------------> Table.pool
        self.player_bets --------> Table.pool.player_bets
        self.blinds -------------> Table.pool.blinds
        self.call_value ---------> Table.pool.call_value
        self.total_pool_value ---> Table.pool.total_value
        
        See texas_hold_em.py for information on associated attributes
        and methods related to each class."""
        self.table = Table(Deck(), players)
        self.table.pool = Pool(10)
        self.pool = self.table.pool
        self.revealed_cards = self.table.revealed_cards
        self.players = self.table.players
        self.deck = self.table.deck
        self.cards = self.deck.cards
        self.player_bets = self.pool.player_bets
        self.blinds = self.pool.blinds
        self.call_value = self.pool.call_value
        self.total_pool_value = self.pool.total_value
        self.main_menu = Menu([
            'TEXAS HOLD\'EM',
            '1. Play',
            '2. Add/Remove Players',
            '3. Set Blinds',
            '4. Set Starting Chips',
            '5. Quit'
        ], '> ')
        self.blinds_menu = Menu([
            'BLINDS',
        ], 'Set blinds: ')
        self.starting_chips_menu = Menu([
            'STARTING CHIPS'
        ], 'Set Starting Chips value: ')
        self.add_remove_players_menu = Menu([
            'ADD/REMOVE PLAYERS',
            '1. Add Player',
            '2. Remove Player',
            '3. Back'
        ], '> ')

    def play_game(self):
        """Start the game."""
        self.game_running = True

    def game_loop(self):
        """ADD CODE AS METHODS AND ATTRIBUTES ARE DEVELOPED."""
        if self.players is None:
            self.menu_response('There are no players at the table...')
            return

    def menu_response(self, text):
        """Menu response that displays text to the console, waits for 1.2 seconds,
        then clears the screen."""
        print(text)
        self.slp(1.2)
        self.cls()

    def slp(self, amount: int | float):
        """Wait for some amount of seconds."""
        time.sleep(amount)

    def cls(self):
        """Clear the console screen."""
        os.system('clear')

    def add_remove_players(self):
        """Add/Remove Players to the table."""
        response = self.add_remove_players_menu()
        if response.isdigit():
            if response == '1':
                curr_players = len(self.players)
                self.add_player()
                if len(self.players) > curr_players:
                    self.menu_response(f'Player {self.players[-1]} added.')
                else:
                    self.menu_response('Add Player failed...')
            elif response == '2':
                curr_players = len(self.players)
                removed_players_name = self.remove_player()
                if len(self.players) < curr_players:
                    self.menu_response(f'Player {removed_players_name} removed.')
                else:
                    self.menu_response('Remove Player failed...')
            elif response == '3':
                self.cls()
        else:
            self.menu_response('Invalid input! Please try again.')

    def add_player(self):
        """TO BE ADDED"""
        pass

    def remove_player(self):
        """TO BE ADDED"""
        pass

    def run_engine(self):
        """Run Engine."""
        while self.engine_running:
            self.cls()
            response = self.main_menu()
            self.cls()
            if response == '1':
                self.play_game()
            elif response == '2':
                self.add_remove_players()
                if self.players is not None:
                    self.menu_response(f'{len(self.players)} Players added to the table.')
                else:
                    self.menu_response('No players added to the table...')
            elif response == '3':
                blinds_response = self.blinds_menu()
                if blinds_response.isdigit(): 
                    if float(blinds_response) >= 0:
                        self.blinds = blinds_response
                        self.menu_response(f'Blinds set to ${self.blinds}.')
                    else:
                        self.menu_response('Blinds value must be non-negative...')
                else:
                    self.menu_response('Blinds value must be a number...')
            elif response == '4':
                chips_response = self.starting_chips_menu()
                if chips_response.isdigit():
                    if float(chips_response) > 0:
                        if self.players is not None:
                            for player in self.players:
                                player.chips = Chips(player, self.table, chips_response)
                            self.menu_response(f'Starting Chip value set to ${chips_response}.')
                        else:
                            self.menu_response('There are no players at the table...')
                    else:
                        self.menu_response('Starting Chip value must be greater than 0...')
                else:
                    self.menu_response('Starting Chips value must be a number...')
            elif response == '5':
                self.cls()
                self.menu_response('GOODBYE!')
                self.engine_running = False
            else:
                self.menu_response('Invalid input! Please try again.')
            while self.game_running:
                self.game_loop()

engine = TexasHoldEmEngine(None)
engine.run_engine()
