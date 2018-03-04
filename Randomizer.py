from alchemy_wrap import *
from sql import sql
from orm import Card
import random
from RandomizerConfig import RandomizerConfig


class Randomizer(object):
    def __init__(self):
        self.cards = sql.query(Card).all()
        self.expansions = [expansion[0] for expansion in sql.query(distinct(Card.expansion)).all()]
        self.sortedCards = {}
        self.chosenCards = []

        self.setSortedCards()

    def randomize10(self):
        for expansion in self.expansions:
            amountToRandomize = RandomizerConfig["amountOfCardsPerSet"][expansion]
            self.chosenCards += self.randomizeCardsByExpansion(expansion, amountToRandomize)

    def randomizeCardsByExpansion(self, expansion, amountToRandomize):
        cardsInExpansion = self.sortedCards[expansion]

        chosenCards = []
        while len(chosenCards) < amountToRandomize:
            randomCard = cardsInExpansion[random.randint(0, len(cardsInExpansion) - 1)]
            if randomCard not in chosenCards:
                chosenCards.append(randomCard)

        return chosenCards

    def setSortedCards(self):
        for expansion in self.expansions:
            self.sortedCards[expansion] = [card for card in self.cards if card.expansion == expansion]

    def replaceCard(self, card):
        newCard = self.randomizeCardsByExpansion(card.expansion, 1)[0]
        while newCard in self.chosenCards:
            newCard = self.randomizeCardsByExpansion(card.expansion, 1)[0]

        self.chosenCards.append(newCard)
        self.chosenCards.remove(card)

    def printChosenCards(self):
        for card in self.chosenCards:
            print(card.name + ", " + card.expansion)
        print()

    def swapCardsFromUserInput(self):
        while True:
            cardName = input("Kaartje swappen?\n")
            self.replaceCard([card for card in self.chosenCards if card.name == cardName][0])
            self.printChosenCards()
