import unittest
import sqlite3

from app import db_setup


class SetupTest(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect('pokemondata.db')
        self.c = self.conn.cursor()
        self.c.execute('DROP TABLE IF EXISTS types;')
        self.c.execute('DROP TABLE IF EXISTS dex;')
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def testGenerateTypeTable(self):
        db_setup.generate_type_table()
        self.c.execute("SELECT Grass FROM types WHERE Name='Fire';")
        self.assertEqual(self.c.fetchone()[0], 2.0)


    def testGenerateDexTable(self):
        db_setup.generate_dex_table()
        self.c.execute("SELECT type1, type2 FROM dex WHERE Name='Abra';")
        self.assertEqual(self.c.fetchone(), ('Psychic', '',))
        self.c.execute("SELECT type1, type2 FROM dex WHERE Name='Charizard-Mega-X';")
        self.assertEqual(self.c.fetchone(), ('Dragon', 'Fire',))
        self.c.execute("SELECT COUNT(*) FROM dex;")
        self.assertEqual(self.c.fetchone()[0], 942)


if __name__ == '__main__':
    unittest.main()
