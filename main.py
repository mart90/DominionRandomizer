import logging
from sqlite import sql
from sqlops import SqlOps


Format = "[%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s] %(message)s"
logging.basicConfig(filename="dominionRandomizer.log", format=Format, level=logging.DEBUG)

sql.connect("dominion.db")
sqlops = SqlOps()

sqlops.create_tables()
sqlops.insert_all_cards()

sql.commit()
sql.close()
