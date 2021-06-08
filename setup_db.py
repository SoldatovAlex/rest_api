from datetime import date


from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()
engine = create_engine( 'sqlite:///sqlite3.db', connect_args={'check_same_thread': False})


# create table in db
class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(250))
    last_name = Column(String(250))
    email = Column(String(250))


# create table in db
class Transaction(Base):
    __tablename__ = 'Transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    amount = Column(Integer)
    date = Column(DateTime, default=date.today())

Base.metadata.create_all(engine)