import logging
import os
from sql import sql
from randomizer import Randomizer
from misc_functions import *


Format = '[%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s] %(message)s'
logging.basicConfig(filename='dominionRandomizer.log', format=Format, level=logging.DEBUG)

# try:
#     os.remove('dominion.db')
# except FileNotFoundError:
#     pass
#
# init_database()
#
# add_games()
# sql.commit()
#
# calculate_card_popularity()
# sql.commit()

randomizer = Randomizer()
if randomizer.try_build_kingdom(10000):
    randomizer.swap_cards_from_user_input()
