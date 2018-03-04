from sql import sql
from orm import *


def init_database():
    from sqlops import SqlOps
    from kingdomcards import kingdomcards

    SqlOps().create_tables()

    if sql.query(Card).all():
        # Cards are already in db
        return

    for cdict in kingdomcards:
        sql.add(Card().build_from_dict(cdict))


def add_games():
    from game_dicts import games

    for game in games:
        g = Game()
        g.build_from_dict(game)
        sql.add(g)


# Get a comma separated list of cards for the Google sheets drop down menus
def get_card_names_from_db():
    writer = open('cards.txt', 'w')

    cardnames = sql.query(Card.name).all()
    for cardname in cardnames:
        writer.write(cardname[0] + ',')
