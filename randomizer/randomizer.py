from alchemy_wrap import *
from orm import Card, Game, GameCard
from randomizer_config import config
from sql import sql
import random


class Randomizer(object):
    def __init__(self):
        self.cardpool = []
        self.kingdom = []
        self.cards_needed_per_expansion = {}
        self.expansions_satisfied = False

        self.set_cardpool()

    def set_cardpool(self):
        self.set_expansion_requirements()
        expansions = [expansion for expansion in self.cards_needed_per_expansion]
        self.cardpool = [card for card in sql.query(Card).filter(Card.expansion.in_(expansions))]

        if config['games to exclude'] > 0:
            self.exclude_games(config['games to exclude'])

    def set_expansion_requirements(self):
        for expansion, amount in config['cards per set'].items():
            if amount > 0:
                self.cards_needed_per_expansion[expansion] = amount

    def exclude_games(self, amounttoexclude):
        gameids = [game.id for game in sql.query(Game).order_by(desc(Game.id)).limit(amounttoexclude)]
        cardstoexclude = [gamecard.card for gamecard in sql.query(GameCard).filter(GameCard.gameId.in_(gameids))]
        for card in cardstoexclude:
            if card in self.cardpool:
                self.cardpool.remove(card)

    def build_kingdom(self):
        for forcedattr, amount in config['forced attributes'].items():
            if amount > 0:
                attrdict = {
                    'attrname': forcedattr,
                    'amount': amount}
                if self.requirement_satisfied(None, attrdict):
                    continue
                self.randomize_card(None, attrdict)
                if not self.expansions_satisfied:
                    self.check_for_satisfied_expansions()

        for cardtype, forced in config['forced types'].items():
            if forced:
                if self.requirement_satisfied(cardtype):
                    continue
                self.randomize_card(cardtype)
                if not self.expansions_satisfied:
                    self.check_for_satisfied_expansions()

        self.satisfy_expansions()
        self.fill_kingdom()

    def requirement_satisfied(self, cardtype=None, cardattr=None):
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
        for expansion, cardsneeded in self.cards_needed_per_expansion.items():
            if cardsneeded <= 0:
                self.cardpool = [card for card in self.cardpool if card.expansion != expansion]

        if not self.cardpool:
            self.expansions_satisfied = True
            self.restore_satisfied_expansions_to_cardpool()

            if config['games to exclude'] > 0:
                self.exclude_games(config['games to exclude'])

    def restore_satisfied_expansions_to_cardpool(self):
        for expansion, cardsneeded in self.cards_needed_per_expansion.items():
            if cardsneeded <= 0:
                self.cardpool.extend(sql.query(Card).filter(Card.expansion == expansion))

            for card in [card for card in self.kingdom if card.expansion == expansion]:
                self.cardpool.remove([c for c in self.cardpool if c.name == card.name][0])

    def satisfy_expansions(self):
        while len(self.kingdom) < 10 and not self.expansions_satisfied:
            self.randomize_card()
            self.check_for_satisfied_expansions()

    def fill_kingdom(self):
        while len(self.kingdom) < 10:
            self.randomize_card()

    def randomize_card(self, cardtype=None, cardattr=None, expansion=None):
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
            return

        if 'attack' in randomcard.types \
                and config['attack forces reaction'] \
                and not self.requirement_satisfied('reaction'):
            if len(self.kingdom) == 9:
                # We still need a reaction card but the kingdom would be full after adding this. Try again
                self.randomize_card(cardtype, cardattr, expansion)
                return
            self.randomize_card('reaction')

        self.cardpool.remove(randomcard)
        self.kingdom.append(randomcard)
        self.cards_needed_per_expansion[randomcard.expansion] -= 1

    def replace_card(self, card):
        self.randomize_card(None, None, card.expansion)
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
