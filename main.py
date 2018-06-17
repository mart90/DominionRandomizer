import logging
import os
from sql import sql
from randomizer import Randomizer
from misc_functions import init_database, add_games


Format = '[%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s] %(message)s'
logging.basicConfig(filename='dominionRandomizer.log', format=Format, level=logging.DEBUG)

# try:
#     os.remove('dominion.db')
# except FileNotFoundError:
#     pass
#
# init_database()
# add_games()
# sql.commit()

randomizer = Randomizer()
randomizer.build_kingdom()
randomizer.print_kingdom()
randomizer.swap_cards_from_user_input()
