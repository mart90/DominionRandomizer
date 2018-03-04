from alchemy_wrap import *
from game_player import GamePlayer
from game_card import GameCard
from card_vote import CardVote
from statistics import mean


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

    def __init__(self):
        self.realScores = []

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

        # TODO build player votes

        self.winnerId = self.get_winner()
        return self

    def set_real_scores(self):
        avgbid = mean([p.bid for p in self.players])

        for player in self.players:
            score = player.score + avgbid if player.bid < avgbid else player.score
            self.realScores.append({
                'player': player,
                'score': score
            })

    def get_winner(self):
        if not self.realScores:
            self.set_real_scores()

        maxscore = max([rs['score'] for rs in self.realScores])
        winners = [rs['player'] for rs in self.realScores if rs['score'] == maxscore]
        if len(winners) > 1:
            return winners[0].playerId if winners[0].turn > winners[1].turn else winners[1].playerId
        else:
            return winners[0].playerId
