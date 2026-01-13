from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Program(Base):
    __tablename__ = "program"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    title = Column(String)
    subtitle = Column(String)
    duration = Column(Integer)
    type = Column(String)
    description = Column(String)


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)


class Casting(Base):
    __tablename__ = "casting"

    id = Column(Integer, primary_key=True)
    personid = Column(Integer, ForeignKey("person.id"))
    programid = Column(Integer, ForeignKey("program.id"))
    function = Column(String)


