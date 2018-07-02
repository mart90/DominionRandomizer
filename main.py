import logging
import os
from randomizer import Randomizer
from misc_functions import *
from sources.single_game_dict import game as gamedict


# PARAMETERS #
reinitiate_database = False
insert_game = True
randomizer_maxtries = 10000
# ---------- #

Format = '[%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s] %(message)s'
logging.basicConfig(filename='dominionRandomizer.log', format=Format, level=logging.DEBUG)

if reinitiate_database:
    try:
        os.remove('dominion.db')
    except FileNotFoundError:
        pass

    init_database()
    add_all_games()
    calculate_card_popularity()

if insert_game and gamedict:
    add_single_game(gamedict)
    calculate_card_popularity()
    singlegamedict = open('sources/single_game_dict.py', 'w')
    singlegamedict.write("game = {}")
    singlegamedict.close()

randomizer = Randomizer()
if randomizer.try_build_kingdom(randomizer_maxtries):
    randomizer.swap_cards_from_user_input()
