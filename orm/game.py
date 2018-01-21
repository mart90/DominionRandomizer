from alchemy_wrap import *
from game_player import GamePlayer
from game_card import GameCard
from card_vote import CardVote


class Game(base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    datePlayed = Column(String)
    withColonies = Column(Integer)
    withPlatinum = Column(Integer)
    winnerId = Column(Integer, ForeignKey('player.id'))

    players = relationship('GamePlayer', back_populates='game')
    cards = relationship('GameCard', back_populates='game')
    votes = relationship('CardVote', back_populates='game')

    def build_from_dict(self, dct):
        self.datePlayed = dct['date']
        self.withColonies = dct['with colonies']
        self.withPlatinum = dct['with platinum']

        for player in dct['players']:
            self.players.append(GamePlayer().build_from_dict(player))
        for card in dct['cards']:
            self.cards.append(GameCard().build_from_dict(card))
        for vote in dct['votes']:
            self.votes.append(CardVote().build_from_dict(vote))

        maxscore = max(p.score for p in self.players)
        self.winnerId = [p.playerId for p in self.players if p.score == maxscore][0]

        return self

