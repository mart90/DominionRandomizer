from alchemy_wrap import *
from orm import Card
from randomizer_config import config
from sql import sql
import random


class Randomizer(object):
    def __init__(self):
        self.cardpool = []
        self.kingdom = []
        self.cardsNeededPerExpansion = {}
        self.expansionsSatisfied = False

        self.set_cardpool()

    def set_cardpool(self):
        self.set_expansions()
        expansions = [expansion for expansion in self.cardsNeededPerExpansion]
        self.cardpool = [card for card in sql.query(Card).filter(Card.expansion.in_(expansions))]

    def set_expansions(self):
        for expansion, amount in config['cards per set'].items():
            if amount > 0:
                self.cardsNeededPerExpansion[expansion] = amount

    def build_kingdom(self):
        for forcedattr, amount in config['forced attributes'].items():
            if amount > 0:
                attrdict = {
                    'attrname': forcedattr,
                    'amount': amount}
                if self.requirement_already_satisfied(None, attrdict):
                    continue
                self.randomize_card(None, None, attrdict)
                if not self.expansionsSatisfied:
                    self.check_for_satisfied_expansions()

        for cardtype, forced in config['forced types'].items():
            if forced:
                if self.requirement_already_satisfied(cardtype):
                    continue
                self.randomize_card(None, cardtype)
                if not self.expansionsSatisfied:
                    self.check_for_satisfied_expansions()

        self.satisfy_expansions()
        self.fill_kingdom()

    def requirement_already_satisfied(self, cardtype=None, cardattr=None):
        if cardtype is not None:
            cards = [card for card in self.kingdom if card.trasher == 1] if cardtype == 'trasher' \
                else [card for card in self.kingdom if cardtype in [cardtype.type for cardtype in card.types]]
            return True if cards else False

        if cardattr is not None:
            attrname = cardattr['attrname']
            forcedamount = cardattr['amount']
            cards = [card for card in self.kingdom if card.cost == forcedamount] if attrname == 'cost' \
                else [card for card in self.kingdom if getattr(card, attrname) >= forcedamount]
            return True if cards else False

    def check_for_satisfied_expansions(self):
        for expansion, cardsneeded in self.cardsNeededPerExpansion.items():
            if cardsneeded <= 0:
                self.cardpool = [card for card in self.cardpool if card.expansion != expansion]

        if not self.cardpool:
            self.expansionsSatisfied = True
            self.restore_satisfied_expansions_to_cardpool()

    def restore_satisfied_expansions_to_cardpool(self):
        for expansion, cardsneeded in self.cardsNeededPerExpansion.items():
            if cardsneeded <= 0:
                self.cardpool.extend(sql.query(Card).filter(Card.expansion == expansion))

            for card in [card for card in self.kingdom if card.expansion == expansion]:
                self.cardpool.remove([c for c in self.cardpool if c.name == card.name][0])

    def satisfy_expansions(self):
        while len(self.kingdom) < 10 and not self.expansionsSatisfied:
            self.randomize_card()
            self.check_for_satisfied_expansions()

    def fill_kingdom(self):
        self.restore_satisfied_expansions_to_cardpool()
        while len(self.kingdom) < 10:
            self.randomize_card()

    def randomize_card(self, expansion=None, cardtype=None, cardattr=None):
        cardpool = self.cardpool

        if expansion is not None:
            cardpool = [card for card in cardpool if card.expansion == expansion]

        if cardtype is not None:
            cardpool = [card for card in cardpool if card.trasher == 1] if cardtype == 'trasher' \
                else [card for card in cardpool if cardtype in [cardtype.type for cardtype in card.types]]

        if cardattr is not None:
            attrname = cardattr['attrname']
            forcedamount = cardattr['amount']
            cardpool = [card for card in cardpool if card.cost == forcedamount] if attrname == 'cost' \
                else [card for card in cardpool if getattr(card, attrname) >= forcedamount]

        randomcard = cardpool[random.randint(0, len(cardpool) - 1)]

        if randomcard is None:
            return False

        self.cardpool.remove(randomcard)
        self.kingdom.append(randomcard)
        self.cardsNeededPerExpansion[randomcard.expansion] -= 1

    def replace_card(self, card):
        self.randomize_card(card.expansion)
        self.kingdom.remove(card)

    def print_kingdom(self):
        for card in self.kingdom:
            print(card.name + ", " + card.expansion)
        print()

    def swap_cards_from_user_input(self):
        while True:
            cardname = input("Kaartje swappen?\n")
            if cardname == 'n':
                break
            self.replace_card([card for card in self.kingdom if card.name == cardname][0])
            self.print_kingdom()
