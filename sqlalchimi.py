from sqlalchemy import (create_engine,
                        text,
                        Column,
                        Text, String, Integer, INT,
                        )
from sqlalchemy.orm import declarative_base, sessionmaker
from tabulate import tabulate

db_url = 'database.db'

engine = create_engine(f'sqlite:///{db_url}', echo=True)
Base = declarative_base()


# conn = engine.connect()
# query = ("CREATE TABLE IF NOT EXISTS people("
#          "id integer primary key autoincrement,"
#          "name text,age integer)")
# conn.execute(text(query))
# conn.execute(text("INSERT INTO people (name, age) VALUES ('Alex', 25);"))
# conn.commit()

class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.name!r}, {self.age})'

    @property
    def is_adult(self):
        return self.age >= 18

    @property
    def greating(self):
        return f"Hello {self.name}"

    @classmethod
    def display(cls, session):
        people = session.query(cls).all()
        people = [(p, p.is_adult, p.greating) for p in people]
        header = ["Обьект", "is_adult", "greating"]
        print(tabulate(people, header, tablefmt="simple_grid"))
        return people

    def save(self, session):
        session.add(self)
        session.commit()

    @classmethod
    def delete(cls, session, id_):
        obj = session.query(cls).filter(id_ == cls.id)
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
print(People.display(session))



