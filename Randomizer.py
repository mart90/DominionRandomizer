from alchemy_wrap import *
from sql import sql
from orm import Card
import random
from RandomizerConfig import RandomizerConfig


class Randomizer(object):
    def __init__(self):
        self.cards = sql.query(Card).all()
        self.sortedCards = {}
        self.setSortedCards()
        self.chosenCards = []

    def randomize(self):
        self.chosenCards = self.choose10cards()
        return [card for card in self.chosenCards]

    def choose10cards(self):
        for key, value in self.sortedCards.items():
            amountOfCardsInSet = len(value)
            chosenCardsInSet = []

            while len(chosenCardsInSet) < RandomizerConfig["amountOfCardsPerSet"][key]:
                randomCard = value[random.randint(0, amountOfCardsInSet - 1)]

                if randomCard not in chosenCardsInSet:
                    chosenCardsInSet.append(randomCard)

            self.chosenCards += chosenCardsInSet
        return self.chosenCards

    def setSortedCards(self):
        expansions = ["base", "intrigue", "dark ages", "prosperity"]
        for expansion in expansions:
            self.sortedCards[expansion] = [card for card in self.cards if card.expansion == expansion]

    def replaceCard(self, card):
        self.addNewCardFromExpansion(card.expansion)
        self.chosenCards.remove(card)
        return self.chosenCards

    def addNewCardFromExpansion(self, expansion):
        expansionCards = self.sortedCards[expansion]
        newCard = expansionCards[random.randint(0, len(expansionCards) - 1)]
        while newCard in self.chosenCards:
            newCard = expansionCards[random.randint(0, len(expansionCards) - 1)]
        self.chosenCards.append(newCard)
