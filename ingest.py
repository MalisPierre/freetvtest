import requests
from data_structure import Program, Person, Casting, Base
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
import xml.etree.ElementTree as ET
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fill_database import get_or_create_person, create_program, create_casting
from datetime import datetime


def download_xml():
    url = "https://testepg.r0ro.fr/epg.xml"
    response = requests.get(url, verify='my_ca.pem')
    if response.status_code == 200:
        with open("epg.xml", "wb") as f:
            f.write(response.content)
        print("File downloaded successfully!")


def create_database():
    engine = create_engine("sqlite:///tv.db", echo=False)
    Base.metadata.create_all(engine)
    print("DATABASE CREATED")

def parse_xml():
    print("POPULATING DATABASE PENDING ...")
    # XML STUFF
    tree = ET.parse('epg.xml')
    root = tree.getroot()

    # DATABASE STUFF
    engine = create_engine("sqlite:///tv.db", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    # LOPPING READ XML
    for program in root.findall('program'):        
        start_time_str = program.get("start_time")
        start_time = datetime.fromisoformat(start_time_str)
        title = program.find("title").text
        subtitle = program.find("subtitle").text
        duration = int(program.find("duration").text)
        type_str = program.find("type").text
        description = program.find("description").text

        # 1 CREATE A PROGRAM
        program_data = create_program(session, start_time, title, subtitle, duration, type_str, description)

        casting = program.find("casting")
        persons = casting.findall("person")
        for person in persons:
            firstname = person.get("firstname")
            lastname = person.get("lastname")
            # 2 GET OR CREATE A PERSON (loop)
            person_data = get_or_create_person(session, firstname, lastname)

            function = person.get("function")
            # 3 CREATE A CASTING (loop)
            casting_data = create_casting(session, program_data, person_data, function)    

    session.close()



download_xml()
create_database()
parse_xml()
print("POPULATING DATABASE TERMINATED :)")