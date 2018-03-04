import logging
from sql import sql
from Randomizer import Randomizer
from misc_functions import init_database, add_games


Format = '[%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s] %(message)s'
logging.basicConfig(filename='dominionRandomizer.log', format=Format, level=logging.DEBUG)

# init_database()
# add_games()

randomizer = Randomizer()
randomizer.randomize10()
randomizer.printChosenCards()
randomizer.swapCardsFromUserInput()

sql.commit()
