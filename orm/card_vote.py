from alchemy_wrap import *
from card import Card
from player import Player
from player_vote import PlayerVote


class CardVote(base):
    __tablename__ = 'cardVote'

    id = Column(Integer, primary_key=True)
    gameId = Column(Integer, ForeignKey('game.id'))
    cardId = Column(Integer, ForeignKey('card.id'))
    initiatorId = Column(Integer, ForeignKey('player.id'))
    result = Column(Integer)

    card = relationship('Card', back_populates='votes')
    game = relationship('Game', back_populates='votes')
    initiator = relationship('Player', back_populates='votesInitiated')
    votes = relationship('PlayerVote', back_populates='cardVote')

    def build_from_dict(self, dct):
        self.cardId = Card.select_id_by_name(dct['card'])
        self.initiatorId = Player.select_id_by_name(dct['initiator'])
        self.result = 1  # Pass

        for vote in dct['votes']:
            playervote = PlayerVote().build_from_dict(vote)
            if playervote.vote == 0:
                self.result = 0

            self.votes.append(playervote)

        return self
