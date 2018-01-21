from alchemy_wrap import *
from player import Player


class GameCardBuy(base):
    __tablename__ = 'gameCardBuy'

    id = Column(Integer, primary_key=True)
    gameCardId = Column(Integer, ForeignKey('gameCard.id'))
    playerId = Column(Integer, ForeignKey('player.id'))
    amountBought = Column(Integer)

    player = relationship('Player', back_populates='buys')
    gameCard = relationship('GameCard', back_populates='buys')

    def build_from_dict(self, dct):
        self.playerId = Player.select_id_by_name(dct['player'])
        self.amountBought = dct['amount bought']
        return self
