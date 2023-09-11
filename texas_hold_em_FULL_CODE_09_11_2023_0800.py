"""TEXAS HOLD'EM"""
from enum import Enum
import os
import time
import random

 ### CHIPS ###
class Chips:
    """Chips for playing Poker games."""
    def __init__(self, player, table, starting_chip_value: int | float):
        self.player = player
        self.table = table
        self.chip_value = starting_chip_value
        self.current_bet_final = 0
        self.current_bet_draft = 0
        self.last_bet = 0

    def add_current_bet_to_pool(self):
        """Add the final current bet to the Player's bet."""
        self.table.pool.add_player_bet(self.player.name, self.current_bet_final)

    def reset_bets(self):
        """Reset the Player's bets to 0 and set the last bet based
        on the previous final current bet."""
        self.last_bet = 0 + self.current_bet_final
        self.table.pool.player_bets[self.player.name] = 0
        self.current_bet_final = 0
        self.current_bet_draft = 0

    def set_bet(self, amount: int | float):
        """Set bet and confirm."""
        self.current_bet_draft = amount
        user_input = input(f'Confirm your bet of {self.current_bet_draft} (y/n). ')
        if user_input == 'y':
            self.current_bet_final += self.current_bet_draft
            self.current_bet_draft = 0
        elif user_input == 'n':
            self.set_bet(amount)
        else:
            print('Invalid selection!')
            self.set_bet(amount)

 ### POOL ###
class Pool:
    """Chip Pool."""
    def __init__(self, blinds: int | float):
        self.total_value = 0
        self.player_bets = {}
        self.call_value = blinds
        self.blinds = blinds

    def add_player(self, player):
        """Add Player to the Pool."""
        self.player_bets[player.name] = 0

    def add_players(self, players: list):
        """Add multiple Players to the Pool."""
        for player in players:
            self.add_player(player)

    def add_player_bet(self, player: str, amount: int | float):
        """Increase Player bet by an amount."""
        self.player_bets[player] += amount
        self.total_value += amount

    def remove_player(self, player: str):
        """Remove Player from the Pool"""
        if player in self.player_bets:
            self.player_bets.pop(player)

    def raise_bet(self, new_bet: int | float):
        """If new bet is greater than the current call value, set the call
        value to the new bet value. Otherwise, inform the Player betting that
        the bet must be greater than the current call value."""
        if new_bet > self.call_value:
            self.call_value = new_bet
        else:
            print('BET must be greater than current CALL.')

 ### SUIT ###
class Suit(Enum):
    """Card suits"""
    SPADES = 0
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3

 ### CARD ###
class Card:
    """Cards"""
    suits = (Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS)
    values = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')
    suit: Suit
    value: str

    def __init__(self, suit: Suit, value: str | int):
        self.suit = suit
        self.value = str(value)

    def print_card(self):
        """Print card details."""
        print(self.value, self.suit.name)

    def change_value(self, new_value: str | int):
        """Change the value of the card."""
        if isinstance(new_value, int):
            if 0 <= new_value < 14:
                self.value = self.values[new_value]
        elif isinstance(new_value, str):
            for value in self.values:
                if value == new_value:
                    self.value = new_value
                    return
            raise ValueError('Entered value does not match available')

 ### DECK ###
class Deck:
    """Deck of Cards"""
    def __init__(self):
        self.cards = [Card(suit, value) for suit in Card.suits for value in Card.values]

    def print_cards(self):
        """Print each card value and its suit to the console."""
        print('DECK:')
        for item in self.cards:
            print(item.value, item.suit.name)

    def add_card(self, card: Card):
        """Add a card to the deck."""
        self.cards.append(card)

    def flip_top_card(self):
        """Reveal the top card of the deck."""
        print(self.cards[0].value, self.cards[0].suit.name)

    def shuffle(self):
        """Shuffle the Deck"""
        random.shuffle(self.cards)
        return self

 ### PLAYER TEXAS HOLD'EM ###
class PlayerTexasHoldEm:
    """Player"""
    name = None
    hand = (None,None)
    table = None
    chips = 0
    points = 0

    def __init__(self, name: str, table = None, starting_chips: int | float = 100):
        self.name = name
        self.table = table
        self.chips = Chips(self, self.table, starting_chips)

    def raise_bet(self, new_bet: int | float):
        """Raise the bet on the Table."""
        if self.check_table():
            pool = self.table.pool
            pool.player_bets[self.name] = new_bet - pool.player_bets[self.name]
            print(f'{self.name} raises a bet of ${pool.player_bets[self.name]}.')
        else:
            self.check_table_error()

    def check_table_error(self):
        """Raise LookupError if check_table method fails."""
        raise LookupError("""Method check_table() failed. Make sure table attribute
                          contains source Player in its players attribute.""")

    def check_table(self):
        """Check if Player is a member of the Table they're playing on."""
        for player in self.table.players:
            if self == player:
                return True
        return False

    def call(self):
        """Call the current bet."""
        pool = self.table.pool
        if self.check_table():
            pool.add_player_bet(pool.call_value-pool.player_bets[self.name])
            print(f'{self.name} calls.')
        else:
            self.check_table_error()

    def set_table(self, new_table):
        """Set the Table the Player is playing on."""        
        self.table = new_table

    def discard_hand(self, discard_pile=None):
        """Discard the Player's hand. If discard_pile is input, move cards to
        the discard_pile before discarding the Player's hand."""
        if discard_pile is not None:
            discard_pile.extend([self.hand[0], self.hand[1]])
        self.hand = (None, None)

    def draw_cards(self, deck: Deck):
        """Draw the top card from the deck."""
        self.hand = (deck.cards.pop(0), deck.cards.pop(0))

    def print_hand(self):
        """Print the Player's hand to the console."""
        print(self.name+'\'s Hand:')
        for item in self.hand:
            item.print_card()

    def peek_cards(self):
        """View cards for only 1.5 seconds"""
        self.print_hand()
        time.sleep(1.5)
        os.system('clear')

 ### TABLE ###
class Table:
    """Table for playing card games/Dealer"""
    def __init__(self, deck: Deck, players = []):
        self.deck = deck
        self.players = players
        if self.players is not None:
            for player in self.players:
                player.set_table(self)
        self.pool = Pool(10)
        self.revealed_cards = []

    def set_blinds(self, blinds: int | float):
        """Set blinds for beginning a hand."""
        self.pool.blinds = blinds

    def shuffle_deck(self):
        """Shuffle Table Deck"""
        self.deck.shuffle()

    def list_players(self):
        """List players and the index associated with each one"""
        p_value = 0
        for player in self.players:
            print(p_value, player.name)
            p_value += 1

    def reveal_card(self):
        """Reveal a single card"""
        self.revealed_cards.append(self.deck.cards.pop(0))

    def reveal_three(self):
        """Initial card reveal"""
        for i in range(3):
            self.reveal_card()
            print(str(i+1), self.revealed_cards[i])

    def reveal_card_and_print(self):
        """Reveal a card and print all revealed cards to the console"""
        self.reveal_card()
        revealed = enumerate(self.revealed_cards)
        print('TABLE:')
        for i in revealed:
            print(str(i[0]+1)+'.', i[1].value, i[1].suit.name)

    def deal_cards(self):
        """Deal cards to each player"""
        for player in self.players:
            player.draw_cards(self.deck)

    def add_card(self, card: Card):
        """Add Card to Deck on Table"""
        self.deck.add_card(card)

    def reform_deck(self):
        """Add cards from Players' hands back to the Deck on the Table"""
        for player in self.players:
            player.discard_hand(self.deck.cards)

 ### TEXAS HOLD'EM POINTS ###
class TexasHoldEmPoints:
    """Point system for figuring out who wins a hand"""
    points = 0
    suit_points = 0
    cards = None
    points_list = {
        'High Card Four': 0.01, # 0.01
        'High Card Ace': 0.12, # 0.12
        'High Card Rules': 'Four is the lowest high card, therefore 4 is 0.01 and A is 0.12',
        'Pair of Twos': (2/100)*7, # 0.14
        'Pair of Aces': (14/100)*7, # 0.98 
        'Pair Rules': 'Value of the card (2)/100, then multiplied by 7',
        'Two Pairs Twos Threes': (2+3)/5, # 1
        'Two Pairs Kings Aces': (13+14)/5, # 27/5 or 5.4
        'Two Pairs Rules': 'Add card values together, then divide by 5.',
        'Three of a Kind Twos': (2+2+2), # 6
        'Three of a Kind Aces': (14+14+14), # 42
        'Three of a Kind Rules': """Multiply the values of all three cards, 
                                 then raise that to the power of 3.""",
        'Straight 2-3-4-5-6': ((2+3+4+5+6)*2)+3, # 43
        'Straight 10-J-Q-K-A': ((10+11+12+13+14)*2)+3, # 123
        'Straight Rules': """Add all values of cards in the straight together, 
                          multiply by 2, then add 3.""",
        'Flush 2-3-4-5-7': 123+7, # 129
        'Flush 2-3-5-10-A': 123+14, # 137
    }
    sorted_values = {
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': [],
        '7': [],
        '8': [],
        '9': [],
        '10': [],
        'J': [],
        'Q': [],
        'K': [],
        'A': []
    }
    sorted_suits = {
        Suit.SPADES: [],
        Suit.HEARTS: [],
        Suit.DIAMONDS: [],
        Suit.CLUBS: []
    }

    def create_card_tuple(self, cards: list):
        """Create a tuple from the """
        self.cards = tuple(cards)

    def assign_value_suit_lists(self):
        """Assign cards to lists to begin counting Player's points"""
        for value in Card.values:
            for card in self.cards:
                if value == card.value:
                    self.sorted_values[value].append(card)
        for suit in Card.suits:
            for card in self.cards:
                if suit == card.suit:
                    self.sorted_suits[suit].append(card)

### Texas Hold'Em Game Engine ###
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
