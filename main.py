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

try:
    randomizer.build_kingdom()
except ValueError as e:
    print("Couldn't build a kingdom with these requirements")
    exit(1)

randomizer.print_kingdom()
randomizer.swap_cards_from_user_input()
