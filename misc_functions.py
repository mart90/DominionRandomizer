from orm import *
from alchemy_wrap import *
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


def add_all_games():
    from sources.game_dicts import games

    for gamedict in games:
        add_single_game(gamedict)
    sql.commit()


def add_single_game(gamedict):
    game = Game()
    game.build_from_dict(gamedict)
    sql.add(game)
    sql.commit()


# Get a comma separated list of cards for the Google sheets drop down menus
def get_card_names_from_db():
    writer = open('cards.txt', 'w')

    cardnames = sql.query(Card.name).all()
    for cardname in cardnames:
        writer.write(cardname[0] + ',')


def calculate_card_popularity():
    for card in sql.query(Card).all():
        popularityscorespergame = []

        gamesincludingcard = [gameid[0] for gameid in sql.query(GameCard.gameId).filter(GameCard.cardId == card.id)]
        if not gamesincludingcard:
            continue

        for gameid in gamesincludingcard:
            totalgamebuys = sql.query(func.count(CardBuy.id)).filter(CardBuy.gameId == gameid).all()[0][0]
            cardbuys = sql.query(func.count(CardBuy.id)).filter(CardBuy.gameId == gameid,
                                                                CardBuy.cardId == card.id).all()[0][0]
            popularityscorespergame.append(cardbuys / totalgamebuys)

        popularityscore = sum(popularityscorespergame) / len(popularityscorespergame)
        sql.query(Card).filter(Card.id == card.id).update({
            "popularity": popularityscore})

    sql.commit()
