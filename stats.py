from sqlalchemy import create_engine, func, desc, and_
from sqlalchemy.orm import sessionmaker
from data_structure import Program, Person, Casting, Base
from datetime import datetime, timedelta

def long_programs(session):
    persons = session.query(Person).filter(Person.firstname == "jack").all()
    result = (
        session.query(Casting.personid, func.count(Casting.personid).label("count"))
        .group_by(Casting.personid)
        .order_by(func.count(Casting.personid).desc())
        .first()
    )
    long_programs = session.query(func.count(Program.id)).filter(Program.duration >= 600).scalar()
    print(f"the number of programs with a duration >= 10 minutes is:\n{long_programs}\n\n\n")

def special_program(session):

    start_date = datetime(2019, 5, 18)
    end_date = start_date + timedelta(days=1)
    programs = (
        session.query(Program)
        .filter(
            and_(
                Program.start_time >= start_date,
                Program.start_time < end_date
            )
        )
        .order_by(desc(Program.duration))
    )
    program = programs.first()
    print(f"the start time and the title of the program with the biggest duration on 2019-05-18:\ntitle = {program.title}\nstart time = {program.start_time}\n\n\n")


def top_talent(session):
    result = (
        session.query(
            Casting.personid,
            func.count(Casting.personid).label("count"),
        )
        .filter(Casting.function == 'Présentateur')
        .group_by(Casting.personid)
        .order_by(desc(func.count(Casting.personid)) )
        .all()
    )

    print("the first and lastname and number of programs for the 5 Présentateur with the most programs\n")
    for personid, program_count in (item for item in result if item[1] >= 5):
        if program_count >= 5:
            person = session.query(Person).filter(Person.id == personid).first()
            print(f"first name: {person.firstname}\nlast name: {person.lastname}\nnumber of programs: {program_count}\n")
    print("\n\n")

def manuel_blanc(session):
    person = session.query(Person).filter(
        Person.firstname == 'Manuel',
        Person.lastname == 'Blanc'
    ).first()

    program_ids = session.query(Casting.programid).filter(Casting.personid == person.id).all()

    program_ids = [pid for (pid,) in program_ids]

    print("the list of programs with 'Manuel Blanc':")
    programs = session.query(Program).filter(Program.id.in_(program_ids)).order_by(desc(Program.start_time)).all()
    for program in programs:
        print(f"program: {program.title}-{program.start_time}")
    print("\n\n")


engine = create_engine("sqlite:///tv.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

long_programs(session)
special_program(session)
top_talent(session)
manuel_blanc(session)

session.close()
