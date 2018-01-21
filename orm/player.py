from alchemy_wrap import *
from sql import sql


class Player(base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    games = relationship('GamePlayer', back_populates='player')
    votesInitiated = relationship('CardVote', back_populates='initiator')
    votes = relationship('PlayerVote', back_populates='player')
    buys = relationship('GameCardBuy', back_populates='player')

    @staticmethod
    def select_id_by_name(name):
        p = sql.query(Player.id).filter_by(name=name).first()
        return p[0] if p is not None else None
