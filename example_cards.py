"""Examples of Cards for deckbuilding."""
from deckbuild import CardFaction, CardType, Card

fireball = Card(
    'Fireball',
    CardFaction.FIRE, 3,
    'Deal 4 damage to an enemy.',
    CardType.SLOW_SPELL,
    flavor='Burn, baby, burn.'
)

firefly = Card(
    'Firefly',
    CardFaction.FIRE, 1,
    'Deal 1 damage to an enemy creature.',
    CardType.CREATURE, 2, 1
)

firebug = Card(
    'Firebug',
    CardFaction.FIRE, 1,
    'Deal 1 damage to a creature you control. If it dies, Firebug gains +2 STR, +2 FOR.',
    CardType.CREATURE, 1, 1
) 