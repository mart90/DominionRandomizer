from sqlite import db


class SqlOps(object):
    def __init__(self):
        db.connect('dominion.db')

    @staticmethod
    def create_tables():
        db.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS card (
                id integer PRIMARY KEY,
                name text UNIQUE,
                expansion text,
                cost integer,
                plusCards integer,
                plusActions integer,
                plusCoins integer,
                plusBuys integer,
                trasher integer,
                popularity float
            );

            CREATE TABLE IF NOT EXISTS cardType (
                id integer PRIMARY KEY,
                cardId integer,
                type text,
                FOREIGN KEY (cardId) REFERENCES card(id)
            );

            CREATE TABLE IF NOT EXISTS player (
                id integer PRIMARY KEY,
                name text UNIQUE
            );

            CREATE TABLE IF NOT EXISTS game (
                id integer PRIMARY KEY,
                datePlayed text,
                withColonies integer,
                withPlatinum integer,
                winnerId integer,
                FOREIGN KEY (winnerId) REFERENCES player(id)
            );

            CREATE TABLE IF NOT EXISTS gamePlayer (
                id integer PRIMARY KEY,
                gameId integer,
                playerId integer,
                bid integer,
                score integer,
                adjustedScore float,
                turn integer,
                FOREIGN KEY (gameId) REFERENCES game(id),
                FOREIGN KEY (playerId) REFERENCES player(id)
            );

            CREATE TABLE IF NOT EXISTS cardBuy(
                id integer PRIMARY KEY,
                cardId integer,
                gameId integer,
                playerId integer,
                amountBought integer,
                FOREIGN KEY (cardId) REFERENCES card(id),
                FOREIGN KEY (gameId) REFERENCES game(id),
                FOREIGN KEY (playerId) REFERENCES player(id)
            );

            CREATE TABLE IF NOT EXISTS gameCard (
                id integer PRIMARY KEY,
                gameId integer,
                cardId integer,
                FOREIGN KEY (gameId) REFERENCES game(id),
                FOREIGN KEY (cardId) REFERENCES card(id)
            );

            CREATE TABLE IF NOT EXISTS cardVote (
                id integer PRIMARY KEY,
                gameId integer,
                cardId integer,
                initiatorId integer,
                result integer,
                FOREIGN KEY (gameId) REFERENCES game(id),
                FOREIGN KEY (cardId) REFERENCES card(id),
                FOREIGN KEY (initiatorId) REFERENCES player(id)
            );

            CREATE TABLE IF NOT EXISTS playerVote (
                id integer PRIMARY KEY,
                cardVoteId integer,
                playerId integer,
                vote integer,
                FOREIGN KEY (cardVoteId) REFERENCES cardVote(id),
                FOREIGN KEY (playerId) REFERENCES player(id)
            );""")
