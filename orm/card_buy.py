from alchemy_wrap import *
from player import Player


class CardBuy(base):
    __tablename__ = 'cardBuy'

    id = Column(Integer, primary_key=True)
    cardId = Column(Integer, ForeignKey('card.id'))
    gameId = Column(Integer, ForeignKey('game.id'))
    playerId = Column(Integer, ForeignKey('player.id'))
    amountBought = Column(Integer)

    player = relationship('Player', back_populates='buys')
    card = relationship('Card', back_populates='buys')
    game = relationship('Game', back_populates='cardBuys')

    def build_from_dict(self, dct):
        self.playerId = Player.select_id_by_name(dct['player'])
        self.amountBought = dct['amount bought']
        return self
