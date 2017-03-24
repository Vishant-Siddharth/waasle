from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String

from sqlalchemy import create_engine

Base = declarative_base()


class Subscribe(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    email = Column(String(80), nullable=False, unique=True)


engine = create_engine('sqlite:///blockriti.db')
Base.metadata.create_all(engine)
