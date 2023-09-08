"""TEXAS HOLD'EM"""
from enum import Enum
import os
import time
import random

class Suit(Enum):
    """Card suits"""
    SPADES = 0
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3

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

class Deck:
    """Deck of Cards"""

    def __init__(self):
        self.cards = [Card(suit, value) for suit in Card.suits for value in Card.values]

    def print_cards(self):
        """Print each card value and its suit to the console."""
        print('DECK:')
        for item in self.cards:
            print(item.value, item.suit.name)

    def flip_top_card(self):
        """Reveal the top card of the deck."""
        print(self.cards[0].value, self.cards[0].suit.name)

    def shuffle(self):
        """Shuffle the Deck"""
        random.shuffle(self.cards)
        return self

class PlayerTexasHoldEm:
    """Player"""
    hand = (None,None)
    points = 0

    def __init__(self, name: str):
        self.name = name

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

class Table:
    """Table for playing card games/Dealer"""
    def __init__(self, deck: Deck, players: list):
        self.deck = deck
        self.players = players
        self.revealed_cards = []

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

class TexasHoldEmPoints:
    """Point system for figuring out who wins a hand"""
    points = 0
    cards = None
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

    def assign_points_lists(self):
        """Assign cards to lists to begin counting Player's points"""
        for value in Card.values:
            for card in self.cards:
                if value == card.value:
                    self.sorted_values[value].append(card)
        for suit in Card.suits:
            for card in self.cards:
                if suit == card.suit:
                    self.sorted_suits[suit].append(card)

deck1 = Deck().shuffle()
evan = PlayerTexasHoldEm('Evan')
table = Table(deck1, [evan])
