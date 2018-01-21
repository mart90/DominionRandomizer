from alchemy_wrap import *
from card import Card
from game_card_buy import GameCardBuy


class GameCard(base):
    __tablename__ = 'gameCard'

    id = Column(Integer, primary_key=True)
    gameId = Column(Integer, ForeignKey('game.id'))
    cardId = Column(Integer, ForeignKey('card.id'))

    card = relationship('Card', back_populates='games')
    game = relationship('Game', back_populates='cards')
    buys = relationship('GameCardBuy', back_populates='gameCard')

    def build_from_dict(self, dct):
        self.cardId = Card.select_id_by_name(dct['name'])

        for buy in dct['buys']:
            if buy['amount bought'] != 0:
                self.buys.append(GameCardBuy().build_from_dict(buy))

        return self
