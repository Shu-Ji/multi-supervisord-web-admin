# coding: u8

from tornado.util import ObjectDict

from sqlalchemy import create_engine
from sqlalchemy import (Column, Integer, Text, String, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute

import settings
import utils


params = dict(
    encoding='utf8',
    echo=False,
    pool_recycle=7200,
)

conn_str = 'sqlite:///%s' % settings.DB_PATH
engine = create_engine(conn_str, **params)


db_factory = lambda: sessionmaker(bind=engine)()
_Base = declarative_base()


class Base(_Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    def as_dict(self):
        r = {c: getattr(self, c) for c in self.columns()}
        return ObjectDict(r)

    @classmethod
    def get_columns(cls):
        c = {}
        for k, v in vars(cls).iteritems():
            if type(v) is InstrumentedAttribute:
                c[k] = v
        return ObjectDict(c)

    @classmethod
    def columns(cls):
        return cls.get_columns().keys()


class User(Base):
    __tablename__ = 'user'

    name = Column(Text, index=True)
    pwd = Column(String(32))

    @staticmethod
    def reset_password(handler, old, new):
        db = handler.db
        user = db.query(User).filter_by(name=handler.username).first()
        if user.pwd != utils.md5(old):
            return False
        user.pwd = utils.md5(new)
        return True


class Host(Base):
    __tablename__ = 'host'

    user = Column(Text)
    pwd = Column(Text)
    host = Column(Text)
    port = Column(Integer)
    is_active = Column(Boolean, server_default='1')

    @staticmethod
    def delete(db, id):
        return bool(db.query(Host).filter_by(id=id).delete())

    @staticmethod
    def update(db, id, user, pwd, host, port):
        return bool(db.query(Host).filter_by(id=id).update(
            {'user': user, 'pwd': pwd, 'host': host, 'port': port}
        ))

    @staticmethod
    def add(handler, user, pwd, host, port):
        db = handler.db

        if db.query(Host).filter_by(host=host, port=port).first() is not None:
            return False

        db.add(Host(user=user, pwd=pwd, host=host, port=port))
        return True

    @staticmethod
    def get_all_active_hosts(handler):
        return handler.db.query(Host).filter_by(is_active=True)

    @staticmethod
    def get_one_host_info_by_id(db, id):
        return db.query(Host).filter_by(id=id).first()

    @staticmethod
    def get_one_host_info(handler, host, port):
        return handler.db.query(Host).filter_by(host=host, port=port).first()

    @staticmethod
    def get_all_hosts(handler):
        return handler.db.query(Host)


if __name__ == '__main__':
    metadata = Base.metadata
    metadata.create_all(engine)

    db = db_factory()
    db.merge(User(id=1, name='admin', pwd=utils.md5('AdminDemo')))
    db.commit()
    db.close()
