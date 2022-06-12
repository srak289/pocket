from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declarative_base, declared_attr

from datetime import datetime

@as_declarative()
class Base(object):

    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        cls_name = ''
        for i,x in enumerate(cls.__name__):
            if i > 0 and x.isupper():
                cls_name += f'_{x.lower()}'
            elif i == 0:
                cls_name += x.lower()
            else:
                cls_name += x
        return cls_name

    @declared_attr
    def timestamp(self):
        return Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

class Network(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    addr = Column(String(24))
    hosts = relationship('Host', backref='network')

class Host(Base):
    id = Column(Integer, primary_key=True)
    ports = relationship('Port', backref='host')
    network_id = Column(String(32), ForeignKey('network.id'))
    addr = Column(String(16))
    name = Column(String(32))

class Port(Base):
    id = Column(Integer, primary_key=True)
    host_id = Column(String, ForeignKey('host.id'))
    port_num = Column(Integer)
    port_stat = Column(String(32))
