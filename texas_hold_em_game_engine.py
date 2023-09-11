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

    def __init__(self, players = []):
        """Create players and their chips first, add them to a 
        list then create the Game Engine object using the list.
        -------------------------------------------------------
        Shortcuts for accessing class objects:
        _______________________________________________________
        self.table ...................................... Table
        self.revealed_cards .............. Table.revealed_cards
        self.players ............................ Table.players
        self.deck .................................. Table.deck
        self.cards ........................... Table.deck.cards
        self.pool .................................. Table.pool
        self.player_bets ............... Table.pool.player_bets
        self.blinds ......................... Table.pool.blinds
        self.call_value ................. Table.pool.call_value
        self.total_pool_value .......... Table.pool.total_value
        -------------------------------------------------------
        See texas_hold_em.py for information on associated 
        attributes and methods related to each class."""

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
            '3. List Players',
            '4. Set Blinds',
            '5. Set Starting Chips',
            '6. Quit'
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
        self.players_list_menu_submenu = ''
        self.players_list_remove_menu = Menu([
                'PLAYERS:',
                self.players_list_menu_submenu
            ], 'Enter the NUMBER of the Player to remove: ')
        self.add_remove_players_boolean = True
        self.create_players_list()

    def play_game(self):
        """Start the game."""
        if len(self.players) == 0:
            self.menu_response('There are no players at the table...')
            self.stop_game()
            return
        else:
            self.game_running = True

    def stop_game(self):
        """Stop the game."""
        self.game_running = False

    def game_loop(self):
        """ADD CODE AS METHODS AND ATTRIBUTES ARE DEVELOPED."""
        pass

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
        while self.add_remove_players_boolean:
            response = self.add_remove_players_menu()
            if response.isdigit():
                if response == '1':
                    curr_players = len(self.table.players)
                    self.add_player()
                    if len(self.players) > curr_players:
                        self.menu_response(f'Player {self.players[-1].name} added.')
                        self.players_list_menu()
                        self.cls()
                    else:
                        self.menu_response('Add Player failed...')
                elif response == '2':
                    self.cls()
                    curr_players = len(self.players)
                    removed_players_name = self.remove_player()
                    if removed_players_name.strip() == '' or len(self.players) == curr_players:
                        self.menu_response('Remove Player failed...')
                    else:
                        self.cls()
                        self.menu_response(f'Player {removed_players_name} removed.')
                    self.players_list_menu()
                    self.cls()
                elif response == '3':
                    self.add_remove_players_boolean = False
                    self.cls()
            else:
                self.menu_response('Invalid input! Please try again.')

    def add_player(self):
        """Add Players to the table."""
        player_name = input('Enter the Player\'s name: ')
        if player_name.strip() == '':
            return
        elif player_name in self.player_bets:
            self.menu_response(f'Player {player_name} is already at the table!')
            return
        else:
            self.players.append(PlayerTexasHoldEm(player_name, self.table))
            self.pool.add_player(PlayerTexasHoldEm(player_name, self.table))
            self.create_players_list_submenu()
            self.create_players_list()
            self.cls()
            return

    def create_players_list(self):
        """Create the Players List."""
        self.players_list_menu = Menu([
            'PLAYERS:',
            self.players_list_menu_submenu
        ], 'Press ANY key to CONTINUE...')
        self.players_list_remove_menu = Menu([
            'PLAYERS:',
            self.players_list_menu_submenu
        ], 'Enter the NUMBER of the Player to remove:')

    def create_players_list_submenu(self):
        """Create list of Players for the Players List Menu."""
        players_enum = enumerate(self.players)
        self.players_list_menu_submenu = ''
        for player in players_enum:
            self.players_list_menu_submenu += str(player[0]+1)+' '+player[1].name+'\n'

    def remove_player(self):
        """TO BE ADDED"""
        self.create_players_list_submenu()
        self.create_players_list()
        response = self.players_list_remove_menu()
        if response.isdigit() and len(self.players) >= int(response) > 0:
            name = self.players[int(response)-1].name
            self.players.remove(self.players[int(response)-1])
            self.pool.remove_player(name)
            self.create_players_list_submenu()
            self.create_players_list()
            return name
        return ''

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
                    if len(self.players) == 1:
                        self.menu_response('1 Player at the table.')
                    else:
                        self.menu_response(f'{len(self.players)} Players at the table.')
                else:
                    self.menu_response('No players added to the table...')
                self.add_remove_players_boolean = True
            elif response == '3':
                self.create_players_list()
                self.players_list_menu()
            elif response == '4':
                blinds_response = self.blinds_menu()
                if blinds_response.isdigit():
                    if float(blinds_response) >= 0:
                        self.blinds = blinds_response
                        self.menu_response(f'Blinds set to ${self.blinds}.')
                    else:
                        self.menu_response('Blinds value must be non-negative...')
                else:
                    self.menu_response('Blinds value must be a number...')
            elif response == '5':
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
            elif response == '6':
                self.cls()
                self.menu_response('GOODBYE!')
                self.engine_running = False
            else:
                self.menu_response('Invalid input! Please try again.')
            while self.game_running:
                self.game_loop()

engine = TexasHoldEmEngine()
engine.run_engine()
