from statistics import mean
from alchemy_wrap import *
from game_player import GamePlayer
from game_card import GameCard
from card_vote import CardVote
from card_buy import CardBuy


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
    cardBuys = relationship('CardBuy', back_populates='game')

    def build_from_dict(self, dct):
        self.datePlayed = dct['date']
        self.withColonies = dct['with colonies']
        self.withPlatinum = dct['with platinum']

        for player in dct['players']:
            self.players.append(GamePlayer().build_from_dict(player))
        self.set_adjusted_scores()

        for vote in dct['votes']:
            self.votes.append(CardVote().build_from_dict(vote))

        for card in dct['cards']:
            gamecard = GameCard().build_from_dict(card)
            self.cards.append(gamecard)

            for buy in card['buys']:
                cardbuy = CardBuy().build_from_dict(buy)
                cardbuy.cardId = gamecard.cardId
                self.cardBuys.append(cardbuy)

        self.winnerId = self.get_winner()
        return self

    def set_adjusted_scores(self):
        avgbid = mean([p.bid for p in self.players])
        for player in self.players:
            player.adjustedScore = player.score + avgbid if player.bid < avgbid else player.score

    def get_winner(self):
        maxscore = max([p.adjustedScore for p in self.players])
        winners = [p for p in self.players if p.adjustedScore == maxscore]
        if len(winners) > 1:
            return winners[0].playerId if winners[0].turn > winners[1].turn else winners[1].playerId

        return winners[0].playerId
