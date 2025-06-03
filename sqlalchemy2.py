from config import password,host,port,user,db_name

from sqlalchemy import (create_engine,
                        text,
                        Column,
                        Text, String, Integer, INT,
                        )
from sqlalchemy.orm import declarative_base, sessionmaker
from tabulate import tabulate



db_url = 'posts.db'

engine = create_engine(f'postgresql+psycopg2://postgres:oldGidra@localhost:5432/posts', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)
    email = Column(String(100))

    def add(self,session):
        session.add(self)
        session.commit()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
# u = User(name="daun")
# session.add(u)
# session.commit()