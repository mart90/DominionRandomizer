from alchemy_wrap import *
from card import Card
from card_buy import CardBuy


class GameCard(base):
    __tablename__ = 'gameCard'

    id = Column(Integer, primary_key=True)
    gameId = Column(Integer, ForeignKey('game.id'))
    cardId = Column(Integer, ForeignKey('card.id'))

    card = relationship('Card', back_populates='games')
    game = relationship('Game', back_populates='cards')

    def build_from_dict(self, dct):
        self.cardId = Card.select_id_by_name(dct['name'])
        return self
