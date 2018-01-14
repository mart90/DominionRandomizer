import logging
from sqlite import sql


class Card(object):
    def __init__(self):
        self.id = None
        self.name = ""
        self.expansion = ""
        self.cost = 0
        self.draw = 0
        self.actions = 0
        self.coins = 0
        self.buys = 0
        self.trasher = 0
        self.types = []

    def set_fields(self, name, expansion, cost, draw, actions, coins, buys, trasher, types=None):
        self.name = name
        self.expansion = expansion
        self.cost = cost
        self.draw = draw
        self.actions = actions
        self.coins = coins
        self.buys = buys
        self.trasher = trasher
        if types is not None:
            self.types = types

        return self

    def to_tuple(self):
        return (
            self.name,
            self.expansion,
            self.cost,
            self.draw,
            self.actions,
            self.coins,
            self.buys,
            self.trasher
        )

    def insert(self):
        sql.query("""
            INSERT INTO card (name, expansion, cost, draw, actions, coins, buys, trasher)
            VALUES (?,?,?,?,?,?,?,?)""", self.to_tuple())

        self.id = sql.last_inserted_id()

    def select_id_by_name(self):
        sql.query("""
            SELECT id FROM card WHERE name = ?""", (self.name,))

        result = sql.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    @staticmethod
    def select_type_by_name(typename):
        sql.query("""
            SELECT id
            FROM cardType
            WHERE name = ?""", (typename,))

        result = sql.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    @staticmethod
    def insert_new_type(typename):
        sql.query("""
            INSERT INTO cardType (name)
            VALUES (?)""", (typename,))

        return sql.last_inserted_id()

    def insert_types(self):
        if not self.types:
            return

        if self.id is None:
            self.id = self.select_id_by_name()
            if self.id is None:
                logging.warning("Card with name <%s> does not exist in database. Can't insert types" % self.name)
                return

        for typename in self.types:
            typeid = self.select_type_by_name(typename)
            if typeid is None:
                typeid = self.insert_new_type(typename)

            sql.query("""
                INSERT INTO cardToTypeMapping
                VALUES (?,?)""", (self.id, typeid,))
