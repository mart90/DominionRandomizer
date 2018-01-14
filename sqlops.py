from sqlite import sql


class SqlOps(object):
    @staticmethod
    def reset_db():
        sql.cursor.executescript("""
            DELETE FROM playerVote;
            DELETE FROM cardVote;
            DELETE FROM gameCard;
            DELETE FROM gamePlayer;
            DELETE FROM game;
            DELETE FROM player;
            DELETE FROM cardToTypeMapping;
            DELETE FROM cardType;
            DELETE FROM card;""")

    @staticmethod
    def create_tables():
        sql.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS card (
                id integer PRIMARY KEY,
                name text,
                expansion text,
                cost integer,
                draw integer,
                actions integer,
                coins integer,
                buys integer,
                trasher integer
            );

            CREATE TABLE IF NOT EXISTS cardType (
                id integer PRIMARY KEY,
                name text
            );

            CREATE TABLE IF NOT EXISTS cardToTypeMapping (
                card integer,
                cardType integer,
                FOREIGN KEY (card) REFERENCES card(id),
                FOREIGN KEY (cardType) REFERENCES cardType(id)
            );

            CREATE TABLE IF NOT EXISTS player (
                id integer PRIMARY KEY,
                name text
            );

            CREATE TABLE IF NOT EXISTS game (
                id integer PRIMARY KEY,
                datePlayed text,
                withColonies integer,
                winner integer,
                FOREIGN KEY (winner) REFERENCES player(id)
            );

            CREATE TABLE IF NOT EXISTS gamePlayer (
                game integer,
                player integer,
                score integer,
                FOREIGN KEY (game) REFERENCES game(id),
                FOREIGN KEY (player) REFERENCES player(id)
            );

            CREATE TABLE IF NOT EXISTS gameCard (
                game integer,
                card integer,
                amountBought integer,
                FOREIGN KEY (game) REFERENCES game(id),
                FOREIGN KEY (card) REFERENCES card(id)
            );

            CREATE TABLE IF NOT EXISTS cardVote (
                id integer PRIMARY KEY,
                game integer,
                card integer,
                initiator integer,
                result integer,
                FOREIGN KEY (game) REFERENCES game(id),
                FOREIGN KEY (card) REFERENCES card(id),
                FOREIGN KEY (initiator) REFERENCES player(id)
            );

            CREATE TABLE IF NOT EXISTS playerVote (
                cardVote integer,
                player integer,
                vote integer,
                FOREIGN KEY (cardVote) REFERENCES cardVote(id),
                FOREIGN KEY (player) REFERENCES player(id)
            );""")

    @staticmethod
    def insert_all_cards():
        from card import Card
        from kingdomcards import kingdomcards

        for card in kingdomcards:
            c = Card()
            c.set_fields(
                card["name"],
                card["expansion"],
                card["cost"],
                card["draw"],
                card["actions"],
                card["coins"],
                card["buys"],
                card["trasher"],
                card["types"]
            )
            c.insert()
            c.insert_types()
