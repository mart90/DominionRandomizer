from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


class Sql(object):

    def __init__(self):
        self.engine = create_engine('sqlite:///dominion.db', echo=False)  # Set echo to true for SQL logging
        sessionfactory = sessionmaker(bind=self.engine)
        self.session = sessionfactory()

sql = Sql().session
