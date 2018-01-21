from alchemy_wrap import *
from player import Player


class PlayerVote(base):
    __tablename__ = 'playerVote'

    id = Column(Integer, primary_key=True)
    cardVoteId = Column(Integer, ForeignKey('cardVote.id'))
    playerId = Column(Integer, ForeignKey('player.id'))
    vote = Column(Integer)

    cardVote = relationship('CardVote', back_populates='votes')
    player = relationship('Player', back_populates='votes')

    def build_from_dict(self, dct):
        self.playerId = Player.select_id_by_name(dct['player'])
        self.vote = dct['vote']
        return self
