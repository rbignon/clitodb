import builtins

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, mapper
from sqlalchemy.schema import MetaData
#import pdb


class BaseTable(object):
    pass


class Database(object):
    def __init__(self, url):
        self.url = url
        self.engine = create_engine(url, pool_recycle=3600)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        builtins.Session = self.Session
        self.reflect()

    def reflect(self):
        metadata = MetaData(self.engine)
        metadata.reflect(self.engine)
        for name, table in metadata.tables.items():
            tableClass = type(str(table.fullname), (BaseTable,), {})
            try:
                mapper(tableClass, table)
            except:
                continue
            else:
                setattr(builtins, name, tableClass)
        #pdb.set_trace()
