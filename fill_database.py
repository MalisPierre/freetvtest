from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from data_structure import Program, Person, Casting, Base
from datetime import datetime


def get_or_create_person(session, first_name, last_name):
    person = session.query(Person).filter(
        Person.firstname == first_name,
        Person.lastname == last_name
    ).first()

    if person:
        return person
    else:
        person = Person(firstname=first_name, lastname=last_name)
        session.add_all([person])
        session.commit()
        return person

def create_program(session, start_time, title, subtitle, duration, type_str, description):
    program = Program(
        start_time=start_time,
        title=title,
        subtitle=subtitle,
        duration=duration,
        type=type_str,
        description=description
    )
    session.add(program)
    session.commit()
    return program

def create_casting(session, program, person, function):
    casting = Casting(
        programid=program.id, 
        personid=person.id, 
        function=function,
    )
    session.add(casting)
    # SESSION.COMMIT COULD POSSIBLY BE MOVED BEFORE CLOSING PROGRAM, 
    # QUERY OPTIMISATION TALK
    session.commit()
    return casting