"""Basic classes for the building-blocks of the deckbuilding part of the game."""
from enum import Enum

class CardTribe(Enum):
    """Card tribe for the Card class."""
    NONE = 0
    PROTAR = 1 # Technologically advanced civilization. Use their technological might to best opponents.
    YTTORAX = 2 # Underground cult serving unknown dark powers and God-like entities.
    UDUNN = 3 # A race of created beings similar to orcs. Rule over the lands of MIRDUNN.
    DRAXAR = 4 # A brutish human-like race that prefers fighting and bladecraft to magic. Very tough.
    ZANTONYR = 5 # Civilizations that rule over the badlands and favor dark and fire magick.
    ELDORAN = 6 # Civilizations that rule over the mainland and favor light and ice magick.

class CardFaction(Enum):
    """Card faction(s) that represent the types of cards the deck plays."""
    NONE = 0 # GRAY
    LIGHT = 1 # White
    DARK = 2 # Black
    FIGHTING = 3 # Green
    BLADE = 4 # Yellow
    FIRE = 5 # Red
    ICE = 6 # Blue

class CardRarity(Enum):
    """Card Rarity for the Card class"""
    COMMON = 0 # White
    UNCOMMON = 1 # Blue
    RARE = 2 # Red
    LEGEND = 3 # Gold

class CardType(Enum):
    """Card Type for the Card class"""
    CREATURE = 1
    SLOW_SPELL = 2
    FAST_SPELL = 3
    TRAP = 4
    AURA = 5
    MANA_CRYSTAL = 0

class Card:
    """Card and the """
    def __init__(self, name: str, faction: CardFaction, tribe: CardTribe, mana: int, ability: str | None, card_type: CardType, rarity: CardRarity, strength: int | None = None, fortitude: int | None = None, flavor: str | None = None):
        self.name = name
        self.flavor_text = flavor
        self.faction = faction
        self.tribe = tribe
        self.mana_cost = mana
        self.ability = ability
        self.card_type = card_type
        self.card_rarity = rarity
        self.strength = strength
        self.fortitude = fortitude
        self.max_fortitude = fortitude
        self.hand_number = None

    def set_flavor_text(self, flavor: str):
        """Set the Card.flavor_text"""
        self.flavor_text = flavor

    def set_faction(self, faction: CardFaction):
        """Set the Card.faction in the form of a CardFaction"""
        self.faction = faction

    def set_card_type(self, card_type: CardType):
        """Set the Card.card_type in the form of a CardType"""
        self.card_type = card_type

    def set_mana_str_for(self, mana: int, strength: int | None, fortitude: int | None):
        """Set the Card.mana_cost, Card.strength and Card.fortitude"""
        self.mana_cost = mana
        self.strength = strength
        self.fortitude = fortitude

    def set_ability(self, ability: str):
        """Set the Card.ability"""
        self.ability = ability

    def print_card(self):
        """Prints card information to console."""
        print(self.name)
        if self.flavor_text is not None:
            print('Flavor Text:', self.flavor_text)
        print('Cost:', self.mana_cost)
        print('Card Faction:', self.faction.name)
        print('Card Type:', self.card_type.name)
        if self.ability is not None:
            print('Ability:', self.ability)
        if self.card_type == CardType.CREATURE:
            print('STR:', self.strength, 'FOR:', self.fortitude)

class Deck:
    """Decks consist of between 40 and 60 cards before being playable.
    Only 3 duplicates of each card can be in a playable deck."""
    def __init__(self, name: str):
        self.name = name
        self.cards = []
        self.playable = False
        self.card_max = 60
        self.card_min = 40
        self.card_faction = None

    def add_card(self, card: Card):
        """Add a Card to the Deck"""
        self.cards.append(card)

    def remove_card(self, card: Card):
        """Remove a Card from the Deck"""
        self.cards.remove(card)