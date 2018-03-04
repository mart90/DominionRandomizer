import logging
from sqlops import SqlOps
from sql import sql
from kingdomcards import kingdomcards
from orm import *
from game_dicts import games
from Randomizer import Randomizer


def init_database():
    SqlOps().create_tables()

    for cdict in kingdomcards:
        sql.add(Card().build_from_dict(cdict))

    sql.commit()


def add_games():
    for game in games:
        g = Game()
        g.build_from_dict(game)
        sql.add(g)

    sql.commit()


def print_cards():
    for card in cards:
        print(card.name + ", " + card.expansion)


def get_card_names_from_db():
    writer = open('cards.txt', 'w')

    cardnames = sql.query(Card.name).all()
    for cardname in cardnames:
        writer.write(cardname[0] + ',')


Format = '[%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s] %(message)s'
logging.basicConfig(filename='dominionRandomizer.log', format=Format, level=logging.DEBUG)

# init_database()
add_games()

randomizer = Randomizer()
cards = randomizer.randomize()
print_cards()

while True:
    cardName = input("Kaartje swappen?\n")
    cards = randomizer.replaceCard([card for card in cards if card.name == cardName][0])
    print_cards()
