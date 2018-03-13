from alchemy_wrap import *
from orm import Card
from randomizer_config import config
from sql import sql
import random


class Randomizer(object):
    def __init__(self):
        self.cardpool = []
        self.chosenCards = []

        self.set_cardpool()

    def set_cardpool(self):
        expansions = []
        for expansion, amount in config['cards per set'].items():
            if amount > 0:
                expansions.append(expansion)

        self.cardpool = [card for card in sql.query(Card).all() if card.expansion in expansions]

    def randomize_all(self):
        for forcedattr, amount in config['forced attributes'].items():
            if amount > 0:
                self.randomize_one(None, None, {
                    'attrname': forcedattr,
                    'amount': amount})

        for cardtype, forced in config['forced types'].items():
            if forced:
                self.randomize_one(None, cardtype)

        self.fill_chosen_cards()

    def fill_chosen_cards(self):
        for expansion, amount in config['cards per set'].items():
            amounttorandomize = amount - len([card for card in self.chosenCards if card.expansion == expansion])
            for i in range(0, amounttorandomize):
                if len(self.chosenCards) == 10:
                    return
                self.randomize_one(expansion)

    def randomize_one(self, expansion=None, cardtype=None, cardattr=None):
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
        self.cardpool.remove(randomcard)
        self.chosenCards.append(randomcard)

    def replace_card(self, card):
        self.randomize_one(card.expansion)
        self.chosenCards.remove(card)

    def print_chosen_cards(self):
        for card in self.chosenCards:
            print(card.name + ", " + card.expansion)
        print()

    def swap_cards_from_user_input(self):
        while True:
            cardname = input("Kaartje swappen?\n")
            if cardname == 'n':
                break
            self.replace_card([card for card in self.chosenCards if card.name == cardname][0])
            self.print_chosen_cards()
