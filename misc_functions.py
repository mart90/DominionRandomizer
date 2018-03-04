from orm import *
from sql import sql


def init_database():
    from sqlops import SqlOps
    from sources.kingdomcards import kingdomcards

    SqlOps().create_tables()

    if sql.query(Card).all():
        # Cards are already in db
        return

    for cdict in kingdomcards:
        sql.add(Card().build_from_dict(cdict))


def add_games():
    from sources.game_dicts import games

    for gamedict in games:
        game = Game()
        game.build_from_dict(gamedict)
        sql.add(game)


# Get a comma separated list of cards for the Google sheets drop down menus
def get_card_names_from_db():
    writer = open('cards.txt', 'w')

    cardnames = sql.query(Card.name).all()
    for cardname in cardnames:
        writer.write(cardname[0] + ',')
