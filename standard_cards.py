from deckbuild import Card, CardType, CardFaction, CardRarity, CardTribe

# Card Faction: None
acolyte = Card(
    'Acolyte', CardFaction.NONE, CardTribe.ELDORAN, 1,
    'Give a creature you control +1 STR/+1 FOR until the end of your turn.',
    CardType.CREATURE, CardRarity.RARE, 1, 2
)

master_smith = Card(
    'Master Smith', CardFaction.NONE, CardTribe.ELDORAN, 1,
    'Give all other creatures you control +2 STR until the end of your turn.',
    CardType.CREATURE, CardRarity.LEGEND, 1, 2
)

wisp_of_the_woods = Card(
    'Wisp of the Woods', CardFaction.NONE, CardTribe.NONE, 1,
    None, CardType.CREATURE, CardRarity.UNCOMMON, 2, 2
)

novice_wizard = Card(
    'Novice Wizard', CardFaction.NONE, CardTribe.NONE, 1,
    'SPELL DAMAGE +1 until the end of your turn.',
    CardType.CREATURE, CardRarity.COMMON, 2, 1
)

squire = Card(
    'Squire', CardFaction.NONE, CardTribe.ELDORAN, 1,
    'Give a creature you control +1 STR.',
    CardType.CREATURE, CardRarity.COMMON, 1, 1
)

