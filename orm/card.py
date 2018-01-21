from alchemy_wrap import *
from card_type import CardType
from sql import sql


class Card(base):
    __tablename__ = 'card'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    expansion = Column(String)
    cost = Column(Integer)
    draw = Column(Integer)
    plusActions = Column(Integer)
    plusCoins = Column(Integer)
    plusBuys = Column(Integer)
    trasher = Column(Integer)

    types = relationship('CardType', back_populates='card')
    games = relationship('GameCard', back_populates='card')
    votes = relationship('CardVote', back_populates='card')

    @staticmethod
    def select_id_by_name(name):
        c = sql.query(Card.id).filter_by(name=name).first()
        return c[0] if c is not None else None

    def build_from_dict(self, dct):
        self.name = dct['name']
        self.expansion = dct['expansion']
        self.cost = dct['cost']
        self.draw = dct['draw']
        self.plusActions = dct['actions']
        self.plusCoins = dct['coins']
        self.plusBuys = dct['buys']
        self.trasher = dct['trasher']

        for t in dct['types']:
            self.types.append(CardType(type=t))

        return self
