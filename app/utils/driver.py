from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from ..paths import *
from ..models import *
from ..models import Base

class SQLDriver(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SQLDriver, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._engine = create_engine(f"sqlite:///{str(DATA_DIR/'pocket.db')}",connect_args=dict(check_same_thread=False))

        self._session_factory = sessionmaker(bind=self._engine)
        self._session = scoped_session(self._session_factory)

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._session

    def create_all_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_all_tables(self):
        Base.metadata.drop_all(self.engine)

    def close(self):
        self.session.close()

    def flush(self):
        self.session.flush()
        self.session.commit()

    def exec_stmt(self, stmt):
        try:
            self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise(e)
        else:
            self.session.commit()
            
    def create(self, cls, **kwargs):
        try:
            self.session.add(cls(**kwargs))
        except Exception as e:
            self.session.rollback()
            raise(e)
        else:
            self.session.commit()
    
    def add_all(self, *args):
        try:
            self.session.add_all(args)
        except Exception as e:
            self.session.rollback()
            raise(e)
        else:
            self.session.commit()

    def create_all(self, *args):
        try:
            self.session.add_all([cls(**kwargs) for cls,kwargs in args])
        except Exception as e:
            self.session.rollback()
            raise(e)
        else:
            self.session.commit()
        
    def read(self, cls, **kwargs):
        try:
            res = self.session.query(cls).filter_by(**kwargs).all()
            # if res == []:
            #     return None
            return res
        except Exception as e:
            raise(e)

    def join(self, cls_a, cls_b, column, **kwargs):
        try:
            res = self.session.query(cls_a, cls_b).join(column).filter_by(**kwargs).all()
            if res == []:
                return None
            return res
        except Exception as e:
            raise(e)
        
    def update(self, cls, filterkw, **kwargs):
        try:
            self.session.query(cls).filter_by(**filterkw).update(kwargs)
        except Exception as e:
            self.session.rollback()
            raise(e)
        else:
            self.session.commit()

    def delete(self, cls, **kwargs):
        '''
        A basic delete implementation
        '''
        try:
            self.session.query(cls).filter_by(**kwargs).delete()
        except Exception as e:
            self.session.rollback()
            raise(e)
        else:
            self.session.commit()
