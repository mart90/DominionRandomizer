from alchemy_wrap import *
from orm import Card, Game, GameCard, CardVote
from randomizer_config import config
from sql import sql
import random


class Randomizer(object):
    def __init__(self):
        self.base_cardpool = []
        self.current_cardpool = []
        self.kingdom = []
        self.cards_needed_per_expansion = {}
        self.expansions_satisfied = False

        self.set_cardpool()

    def set_cardpool(self):
        self.set_expansion_requirements()
        expansions = [expansion for expansion in self.cards_needed_per_expansion]
        self.base_cardpool = [card for card in sql.query(Card).filter(Card.expansion.in_(expansions))]
        self.exclude_past_games()
        self.exclude_voted_cards()
        self.apply_popularity_requirements()
        self.current_cardpool = self.base_cardpool.copy()

    def set_expansion_requirements(self):
        for expansion, amount in config['cards per set'].items():
            if amount > 0:
                self.cards_needed_per_expansion[expansion] = amount

    def exclude_past_games(self):
        if config['games to exclude'] == 0:
            return
        gameids = [game.id for game in sql.query(Game).order_by(desc(Game.id)).limit(config['games to exclude'])]
        cardstoexclude = [gamecard.card for gamecard in sql.query(GameCard).filter(GameCard.gameId.in_(gameids))]
        for card in cardstoexclude:
            if card in self.base_cardpool:
                self.base_cardpool.remove(card)

    def exclude_voted_cards(self):
        if config['exclude cards if voted x times'] == 0:
            return
        cardidstoexclude = \
            [cardid[0] for cardid in sql.query(CardVote.cardId)
             .filter(CardVote.result == 1)
             .group_by(CardVote.cardId)
             .having(func.count() >= config['exclude cards if voted x times'])
             .all()]
        cardstoexclude = sql.query(Card).filter(Card.id.in_(cardidstoexclude)).all()
        self.base_cardpool = [card for card in self.base_cardpool if card not in cardstoexclude]

    def apply_popularity_requirements(self):
        if config['popularity']['include null']:
            self.base_cardpool = \
                [card for card in self.base_cardpool
                 if card.popularity is None
                 or config['popularity']['max'] > card.popularity > config['popularity']['min']]
        else:
            self.base_cardpool = \
                [card for card in self.base_cardpool
                 if card.popularity is not None
                 and config['popularity']['max'] > card.popularity > config['popularity']['min']]

    def try_build_kingdom(self, maxtries):
        basecardsneededperexpansion = self.cards_needed_per_expansion.copy()
        tries = 0
        while tries < maxtries:
            try:
                self.kingdom = []
                self.current_cardpool = self.base_cardpool.copy()
                self.cards_needed_per_expansion = basecardsneededperexpansion.copy()
                self.build_kingdom()
                return True
            except ValueError:
                tries += 1

        print("Couldn't build kingdom with these requirements.")
        return False

    def build_kingdom(self):
        for forcedattr, amount in config['forced attributes'].items():
            if amount > 0:
                attrdict = {
                    'attrname': forcedattr,
                    'amount': amount}
                if self.attr_requirement_satisfied(attrdict):
                    continue
                self.randomize_card(None, attrdict)
                if not self.expansions_satisfied:
                    self.check_for_satisfied_expansions()

        for cardtype, amountforced in config['forced types'].items():
            if amountforced > 0:
                while not self.type_requirement_satisfied(cardtype, amountforced):
                    self.randomize_card(cardtype)
                    if not self.expansions_satisfied:
                        self.check_for_satisfied_expansions()

        self.satisfy_expansions()
        self.fill_kingdom()

    def type_requirement_satisfied(self, cardtype, amount=0):
        cards = [card for card in self.kingdom if card.trasher == 1] if cardtype == 'trasher' \
            else [card for card in self.kingdom if cardtype in [cardtype.type for cardtype in card.types]]
        return True if len(cards) >= amount else False

    def attr_requirement_satisfied(self, cardattr):
        attrname = cardattr['attrname']
        forcedamount = cardattr['amount']
        cards = [card for card in self.kingdom if card.cost == forcedamount] if attrname == 'cost' \
            else [card for card in self.kingdom if getattr(card, attrname) >= forcedamount]
        return True if cards else False

    def check_for_satisfied_expansions(self):
        for expansion, cardsneeded in self.cards_needed_per_expansion.items():
            if cardsneeded <= 0:
                self.current_cardpool = [card for card in self.current_cardpool if card.expansion != expansion]

            if not self.current_cardpool:
                self.expansions_satisfied = True
                self.current_cardpool = self.base_cardpool.copy()
                self.current_cardpool = [card for card in self.current_cardpool if card not in self.kingdom]

    def satisfy_expansions(self):
        while len(self.kingdom) < 10 and not self.expansions_satisfied:
            self.randomize_card()
            self.check_for_satisfied_expansions()

    def fill_kingdom(self):
        while len(self.kingdom) < 10:
            self.randomize_card()

    def randomize_card(self, cardtype=None, cardattr=None, expansion=None):
        cardpool = self.current_cardpool

        if expansion is not None:
            cardpool = [card for card in cardpool if card.expansion == expansion]

        if cardtype is not None:
            cardpool = [card for card in cardpool if card.trasher == 1] if cardtype == 'trasher'\
                else [card for card in cardpool if cardtype in [cardtype.type for cardtype in card.types]]

        if cardattr is not None:
            attrname = cardattr['attrname']
            forcedamount = cardattr['amount']
            cardpool = [card for card in cardpool if card.cost == forcedamount] if attrname == 'cost'\
                else [card for card in cardpool if getattr(card, attrname) >= forcedamount]

        randomcard = cardpool[random.randint(0, len(cardpool) - 1)]

        if randomcard is None:
            return

        if 'attack' in [cardtype.type for cardtype in randomcard.types]\
                and config['attack forces reaction']\
                and not self.type_requirement_satisfied('reaction'):
            if len(self.kingdom) == 9:
                # We still need a reaction card but the kingdom would be full after adding this one. Try again
                self.randomize_card(cardtype, cardattr, expansion)
                return
            self.randomize_card('reaction')

        self.current_cardpool.remove(randomcard)
        self.kingdom.append(randomcard)
        self.cards_needed_per_expansion[randomcard.expansion] -= 1

    def replace_card(self, card, forcesameexpansion=True, forcedtype=None):
        try:
            self.randomize_card(forcedtype, None, card.expansion if forcesameexpansion else None)
            self.kingdom.remove(card)
        except ValueError:
            if forcedtype is not None:
                print("No new card of type '%s'. Trying without this requirement\n" % forcedtype)
                self.replace_card(card)
            elif forcesameexpansion:
                print("No new card of the same expansion (%s). Trying with all expansions\n" % card.expansion)
                self.replace_card(card, False)

    def print_kingdom(self):
        for card in self.kingdom:
            print(card.name + ", " + card.expansion)
        print()

    def swap_cards_from_user_input(self):
        while True:
            self.print_kingdom()
            cardname = input("Replace card? ")

            try:
                card = [card for card in self.kingdom if card.name == cardname][0]
            except IndexError:
                print("Card not found\n")
                continue

            if 'reaction' in [cardtype.type for cardtype in card.types]:
                forcereaction = input("Force reaction? (y/n) ")
                if forcereaction == 'y':
                    self.replace_card(card, False, 'reaction')
                    continue

            self.replace_card(card)
