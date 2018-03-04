from alchemy_wrap import *
from player import Player
from sql import sql


class GamePlayer(base):
    __tablename__ = 'gamePlayer'

    id = Column(Integer, primary_key=True)
    gameId = Column(Integer, ForeignKey('game.id'))
    playerId = Column(Integer, ForeignKey('player.id'))
    bid = Column(Integer)
    score = Column(Integer)
    turn = Column(Integer)

    game = relationship('Game', back_populates='players')
    player = relationship('Player', back_populates='games')

    def build_from_dict(self, dct):
        self.playerId = Player.select_id_by_name(dct['name'])
        if self.playerId is None:
            newplayer = Player(name=dct['name'])
            sql.add(newplayer)
            sql.commit()
            self.playerId = newplayer.id
        self.bid = dct['bid']
        self.score = dct['score']
        self.turn = dct['turn']
        return self
