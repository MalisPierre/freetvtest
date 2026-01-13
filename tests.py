import unittest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from data_structure import Person, Program, Casting, Base


class TestDatabaseModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_insert_and_query_person(self):
        new_person = Person(firstname="John", lastname="Depp")
        self.session.add(new_person)
        self.session.commit()

        person = self.session.query(Person).filter_by(firstname="John", lastname="Depp").one()
        self.assertEqual(person.firstname, "John")
        self.assertEqual(person.lastname, "Depp")
        self.assertIsNotNone(person.id)
        # pas le temps de bien tester
        # l idée est de d abord faire des insertions valides
        # ensuite trigger des exception / executer des query invalides
        # par exemple Casting sans personid ?

if __name__ == "__main__":
    unittest.main()