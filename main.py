import logging
from sqlops import SqlOps
from sql import sql
from kingdomcards import kingdomcards
from orm import *
from game_form import game


Format = '[%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s] %(message)s'
logging.basicConfig(filename='dominionRandomizer.log', format=Format, level=logging.DEBUG)

SqlOps().create_tables()

for cdict in kingdomcards:
    sql.add(Card().build_from_dict(cdict))

sql.commit()

g = Game()
g.build_from_dict(game)
sql.add(g)

sql.commit()
