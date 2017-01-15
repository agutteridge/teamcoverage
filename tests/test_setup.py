import unittest
import sqlite3

from app import db_setup, database


class SetupTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SetupTest, self).__init__(*args, **kwargs)
        self.DB_NAME = 'testing.db'

    def setUp(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.c = self.conn.cursor()

    def tearDown(self):
        self.conn.close()
        database.delete_db(self.DB_NAME)

    def testRun(self):
        db_setup.run(True)
        self.c.execute("SELECT Paper FROM types WHERE Name='Scissors';")
        self.assertEqual(self.c.fetchone()[0], 2.0)
        self.c.execute("SELECT Paper FROM types WHERE Name='Paper_Scissors';")
        self.assertEqual(self.c.fetchone()[0], 0.5)

        self.c.execute("SELECT type1,type2 FROM dex WHERE Name='Papermon';")
        self.assertEqual(self.c.fetchone(), ('Paper', '',))
        self.c.execute("SELECT type1,type2 FROM dex WHERE Name='Scissorsmon';")
        self.assertEqual(self.c.fetchone(), ('Scissors', '',))
        self.c.execute("SELECT type1,type2 FROM dex WHERE Name='Combomon';")
        self.assertEqual(self.c.fetchone(), ('Paper', 'Scissors',))
        self.c.execute("SELECT COUNT(*) FROM dex;")
        self.assertEqual(self.c.fetchone()[0], 3)


if __name__ == '__main__':
    unittest.main()
