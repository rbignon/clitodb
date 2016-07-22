from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Database(object):
    def __init__(self, url):
        self.url = url
        self.engine = create_engine(url, pool_recycle=3600)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
