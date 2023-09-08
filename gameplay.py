from deckbuild import Card, CardType, CardFaction, Deck
import random
from enum import Enum

class Battlefield:
    """Arena in which Summoners fight."""
    def __init__(self, summoner1, summoner2):
        self.s1_deck = summoner1.deck
        self.s2_deck = summoner2.deck
        self.s1_active = []
        self.s1_inactive = []
        self.s1_graveyard = []
        self.s1_traps = []
        self.s1_aura = []
        self.s1_mc = []
        self.s2_active = []
        self.s2_inactive = []
        self.s2_graveyard = []
        self.s2_traps = []
        self.s2_aura = []
        self.s2_mc = []
        self.summoner1 = summoner1
        self.summoner2 = summoner2

    def move_card(self, card, curr_pos: list, new_pos: list):
        """Remove card from one list and add it to another."""
        curr_pos.remove(card)
        new_pos.append(card)

    def make_s1_inactive(self, card):
        """Send card from the summoner 1 active list to the inactive list."""
        self.move_card(card, self.s1_active, self.s1_inactive)

    def make_s2_inactive(self, card):
        """Send card from the summoner 2 active list to the inactive list."""
        self.move_card(card, self.s2_active, self.s2_inactive)

    def check_summoner_set(self, card, summoner, list1: list, list2: list):
        """Check if target summoner is 1 or 2 and then appends the card 
        to the appropriate list."""
        if self.summoner1 == summoner:
            list1.append(card)
        elif self.summoner2 == summoner:
            list2.append(card)

    def check_summoner_move(self, card, summoner, list1a: list, list1b: list, list2a: list, list2b: list):
        """Check if target summoner is 1 or 2 and then moves the card 
        to the appropriate list."""
        if self.summoner1 == summoner:
            self.move_card(card, list1a, list1b)
        elif self.summoner2 == summoner:
            self.move_card(card, list2a, list2b)

    def set_trap(self, card, summoner):
        """Appends the target card to the target summoner's traps list."""
        self.check_summoner_set(card, summoner, self.s1_traps, self.s2_traps)

    def remove_trap(self, card, summoner):
        """Moves the target card to the target summoner's graveyard 
        dlist from the traps list."""
        self.check_summoner_move(card, summoner, self.s1_traps, self.s1_graveyard, self.s2_traps, self.s2_graveyard)

    def set_aura(self, card, summoner):
        """Appends the target card to the target summoner's aura list."""
        self.check_summoner_set(card, summoner, self.s1_aura, self.s2_aura)

    def remove_aura(self, card, summoner):
        """Moves the target card to the target summoner's graveyard list 
        from the aura list."""
        self.check_summoner_move(card, summoner, self.s1_aura, self.s1_graveyard, self.s2_aura, self.s2_graveyard)

    def set_mc(self, card, summoner):
        """Appends the target card to the target summoner's mana crystal 
        list."""
        self.check_summoner_set(card, summoner, self.s1_mc, self.s2_mc)

    def remove_mc(self, card, summoner):
        """Moves the target card to the target summoner's graveyard 
        list from the mana crystal list."""
        self.check_summoner_move(card, summoner, self.s1_mc, self.s1_graveyard, self.s2_mc, self.s2_graveyard)

    def remove_active(self, card, summoner):
        """Moves the target active card from the active list to the 
        graveyard list."""
        self.check_summoner_move(card, summoner, self.s1_active, self.s1_graveyard, self.s2_active, self.s2_graveyard)

    def set_active(self, card, summoner):
        """Appends the target card to the target summoner's active list."""
        self.check_summoner_set(card, summoner, self.s1_active, self.s2_active)

class Phase(Enum):
    """Turn Phases"""
    NONE = 0
    DRAW = 1
    CAST = 2
    ATTACK = 3
    BLOCK = 4
    INTERRUPT = 5
    END = 6

class Summoner:
    """Player character."""
    def __init__(self, deck: Deck, faction: CardFaction, battlefield: Battlefield | None = None):
        self.deck = deck
        self.faction = faction
        self.battlefield = battlefield
        self.win = False
        self.turn = False
        self.phase = Phase.NONE
        self.fortitude = 40
        self.max_fortitude = 40
        self.mana = 0
        self.deck_size = len(self.deck.cards)
        self.hand_size = 0
        self.max_hand_size = 10
        self.hand = []

    def set_battlefield(self, battlefield: Battlefield):
        """Set the battlefield the Summoner is a member of."""
        self.battlefield = battlefield

    def move_card(self, card: Card, curr_pos: list, new_pos: list):
        """Move a Card from the hand to another list."""
        curr_pos.remove(card)
        new_pos.append(card)
        if curr_pos == self.hand:
            self.set_hand_numbers()

    def discard_card(self, hand_number: int):
        """Discard a Card from the hand to the appropriate graveyard."""
        for item in self.hand:
            if item.hand_number == hand_number:
                if self.battlefield.summoner1 == self:
                    self.move_card(item, self.hand, self.battlefield.s1_graveyard)
                    print('Summoner 1 discarded', item.name)
                elif self.battlefield.summoner2 == self:
                    self.move_card(item, self.hand, self.battlefield.s2_graveyard)
                    print('Summoner 2 discarded', item.name)
        self.set_hand_numbers()

    def check_hand_size(self):
        """While your hand size is greater than 10, discard cards until you 
        have only 10."""
        while self.hand_size > self.max_hand_size:
            self.display_hand()
            hand_number = input('Choose a card to discard:')
            self.discard_card(hand_number)

    def shuffle(self):
        """Shuffle the summoner's deck."""
        random.shuffle(self.deck.cards)

    def draw_phase(self):
        """Actions for the DRAW Phase of the turn."""
        if self.phase == Phase.DRAW:
            self.add_current_mana()
            self.draw_card()
            self.phase = Phase.CAST

    def draw_card(self):
        """Move a card from the deck.cards to hand."""
        if len(self.deck.cards) != 0:
            self.hand.append(self.deck.cards.pop(-1))
            self.set_hand_numbers()

    def mulligan(self, cards=7):
        """Draw 7 cards and return a card to the deck to shuffle and draw a 
        different card."""
        for i in range(cards):
            self.draw_card()
            self.hand[i].hand_number = i
        self.display_hand()

    def play_card(self, card, battlefield: Battlefield):
        """Remove card from hand and play on active zone of the Battlefield."""
        self.hand.remove(card)
        battlefield.set_active(card)
        self.set_hand_numbers()

    def heal(self, heal: int):
        """Heal Summoner's fortitude by specified amount, but not greater than the 
        Summoner's max_fortitude."""
        if self.fortitude + heal > self.max_fortitude:
            self.fortitude = 40
        else:
            self.fortitude += heal

    def start_turn(self):
        """Start turn"""
        if self.battlefield.summoner1 == self and self.battlefield.summoner2.phase == Phase.END:
            self.battlefield.summoner2.turn = False
        if self.battlefield.summoner2 == self and self.battlefield.summoner1.phase == Phase.END:
            self.battlefield.summoner1.turn = False
        self.turn = True
        self.phase = Phase.DRAW

    def end_cast_phase(self):
        """If Phase is CAST, switch to the ATTACK Phase."""
        if self.phase == Phase.CAST:
            self.phase = Phase.ATTACK

    def check_block_phase(self):
        """Check if opponent is attacking with creatures, if True and
        creatures can be blocked, start BLOCK Phase."""
        if self.battlefield.summoner1 == self and not self.turn and self.battlefield.summoner2.turn and self.battlefield.summoner2.phase == Phase.ATTACK and len(self.battlefield.s2_active) != 0 or self.battlefield.summoner2 == self and not self.turn and self.battlefield.summoner1.turn and self.battlefield.summoner1.phase == Phase.ATTACK and len(self.battlefield.s1_active) != 0:
            self.phase = Phase.BLOCK

    def end_block_phase(self):
        """Change phase from BLOCK to NONE."""
        if self.phase == Phase.BLOCK:
            self.phase = Phase.NONE

    def check_interrupt(self):
        """Check if Phase can INTERRUPT opponent."""
        for item in self.hand:
            if item.card_type == CardType.FAST_SPELL:
                self.phase = Phase.INTERRUPT

    def add_current_mana(self):
        """Add mana at the beginning of your turn based on the number
        of mana crystals in play."""
        if self.turn and self.phase == Phase.DRAW:
            if self.battlefield.summoner1 == self:
                self.mana += len(self.battlefield.s1_mc)
            elif self.battlefield.summoner2 == self:
                self.mana += len(self.battlefield.s2_mc)

    def add_mana_from_mc(self, amount: int):
        """Add specified amount of mana based on a mana crystal that is
        played to the battlefield."""
        self.mana += amount

    def check_cast_mana(self, card: Card):
        """Check if Summoner has enough mana to cast a card."""
        if card.mana_cost <= self.mana:
            self.spend_mana(card)

    def spend_mana(self, cast: Card):
        """Spend mana to cast a card. ONLY USE WITH 
        Summoner.check_cast_mana()"""
        self.mana -= cast.mana_cost

    def check_attack_phase(self, function, argument, target=None):
        """Only allow ATTACK Phase functions while Phase is ATTACK."""
        if self.phase == Phase.ATTACK:
            if target is None:
                function(argument)
            elif target is not None:
                function(argument, target)

    def check_win(self):
        """Check if win condition is met."""
        if self.battlefield.summoner1 == self:
            if self.battlefield.summoner2.fortitude <= 0:
                self.win = True
            elif self.battlefield.summoner1.fortitude <= 0:
                self.battlefield.summoner2.win = True
        elif self.battlefield.summoner2 == self:
            if self.battlefield.summoner1.fortitude <= 0:
                self.win = True
            elif self.battlefield.summoner2.fortitude <= 0:
                self.battlefield.summoner1.win = True
        if self.win:
            print('You won!')
        elif self.battlefield.summoner1 == self and self.battlefield.summoner2.win:
            print('You lose!')
        elif self.battlefield.summoner2 == self and self.battlefield.summoner1.win:
            print('You lose!')

    def take_damage(self, damage: int):
        """Deal damage to Summoner."""
        self.fortitude -= damage
        self.check_win()

    def __display_list(self, list1: list):
        x = 0
        for item in list1:
            if item.card_type is not CardType.CREATURE:
                print(str(x), list1[x].name, '| Mana:', list1[x].mana_cost, '| Ability:', list1[x].ability)
            elif item.card_type is CardType.CREATURE:
                print(str(x), list1[x].name, '| Mana:', list1[x].mana_cost, '| STR/FOR:', str(list1[x].strength)+'/'+str(list1[x].fortitude), '| Ability:', list1[x].ability)
            x += 1

    def set_hand_numbers(self):
        """Set hand numbers for cards in hand."""
        x = 0
        for item in self.hand:
            item.hand_number = x
            x += 1

    def display_creatures(self, battlefield: Battlefield):
        """Print creatures on board to the console."""
        if self == battlefield.summoner1:
            self.__display_list(battlefield.s1_inactive)
        elif self == battlefield.summoner2:
            self.__display_list(battlefield.s2_inactive)

    def display_hand(self):
        """Print cards in hand to the console."""
        self.set_hand_numbers()
        self.__display_list(self.hand)

class PlayedCard(Card):
    """Card that is played, can be moved around the battlefield and 
    modified."""
    def __init__(self, battlefield: Battlefield, summoner: Summoner):
        self.alive = True
        self.ready_to_attack = False
        self.battlefield = battlefield
        self.position = None
        self.summoner = summoner
        self.attacking = False
        self.blocked = False
        self.blocker = None
        if self.battlefield.summoner1 == self.summoner:
            if self.card_type == CardType.CREATURE or self.card_type == CardType.FAST_SPELL or self.card_type == CardType.SLOW_SPELL:
                self.battlefield.s1_active.append(self)
                self.position = self.battlefield.s1_active
            elif self.card_type == CardType.TRAP:
                self.battlefield.s1_traps.append(self)
                self.position = self.battlefield.s1_traps
            elif self.card_type == CardType.AURA:
                self.battlefield.s1_aura.append(self)
                self.position = self.battlefield.s1_aura
            elif self.card_type == CardType.MANA_CRYSTAL:
                self.battlefield.s1_mc.append(self)
                self.position = self.battlefield.s1_mc
        elif self.battlefield.summoner2 == self.summoner:
            if self.card_type == CardType.CREATURE or self.card_type == CardType.FAST_SPELL or self.card_type == CardType.SLOW_SPELL:
                self.battlefield.s2_active.append(self)
                self.position = self.battlefield.s2_active
            elif self.card_type == CardType.TRAP:
                self.battlefield.s2_traps.append(self)
                self.position = self.battlefield.s2_traps
            elif self.card_type == CardType.AURA:
                self.battlefield.s2_aura.append(self)
                self.position = self.battlefield.s2_aura
            elif self.card_type == CardType.MANA_CRYSTAL:
                self.battlefield.s2_mc.append(self)
                self.position = self.battlefield.s2_mc

    def take_damage(self, damage: int):
        """Decrease the fortitude attribute."""
        self.fortitude -= damage

    def heal(self, heal: int):
        """Increase the fortitude attribute. If the fortitude would become
        greater than the max_fortitude, increase the attribute only by
        enough to make fortitude equal to max_fortitude."""
        if self.fortitude + heal > self.max_fortitude:
            self.fortitude += ((self.fortitude+heal)-self.max_fortitude)
        else:
            self.fortitude += heal

    def check_alive(self):
        """Check if a creature is alive or not. If not, set booleans and 
        send the PlayedCard to the graveyard."""
        if self.fortitude <= 0 and self.card_type == CardType.CREATURE:
            self.alive = False
            self.ready_to_attack = False
            self.send_to_graveyard()

    def send_to_graveyard(self):
        """Remove PlayedCard from current position and send to the
        graveyard of the PlayedCard's summoner."""
        self.position.remove(self)
        if self.summoner == self.battlefield.summoner1:
            self.battlefield.s1_graveyard.append(self)
        elif self.summoner == self.battlefield.summoner2:
            self.battlefield.s2_graveyard.append(self)

    def __attack_creature(self, item, target, damage):
        if item == target:
            target.take_damage(damage)
            target.check_alive()

    def attack_creature(self, damage: int, target):
        """Check which summoner is associated with the PlayedCard,
        then search the opposing summoner's inactive list for the
        target and deal damage to the target. Use check_alive()."""
        if self.battlefield.summoner1 == self.summoner:
            for i in self.battlefield.s2_inactive:
                self.__attack_creature(i, target, damage)
        elif self.battlefield.summoner2 == self.summoner:
            for i in self.battlefield.s1_inactive:
                self.__attack_creature(i, target, damage)

    def set_unblock(self):
        """Set PlayedCard.blocked to False."""
        self.blocked = False

    def set_block(self):
        """Set PlayedCard.blocked to True."""
        self.blocked = True

    def check_block(self, target):
        """If target is attacking, set target.blocked to True, otherwise
        if target isn't attacking, set target.blocked to False."""
        if target.attacking:
            target.set_block()
            target.blocker = self
        elif not target.attacking:
            target.set_unblock()

    def block(self, attacker):
        """Block an attack against your summoner from a creature."""
        self.check_block(attacker)
        self.fortitude -= attacker.strength
        attacker.blocked = False

    def attack(self):
        """Attack the enemy summoner"""
        if self.card_type == CardType.CREATURE:
            if not self.blocked:
                if self.summoner == self.battlefield.summoner1:
                    self.battlefield.summoner2.fortitude -= self.strength
                elif self.summoner == self.battlefield.summoner2:
                    self.battlefield.summoner1.fortitude -= self.strength
            elif self.blocked:
                self.blocker.block(self)
