from alchemy_wrap import *


class CardType(base):
    __tablename__ = 'cardType'

    id = Column(Integer, primary_key=True)
    cardId = Column(Integer, ForeignKey('card.id'))
    type = Column(String)

    card = relationship('Card', back_populates='types')
