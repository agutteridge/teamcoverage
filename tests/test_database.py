import unittest
import sqlite3

from app import database, db_setup


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

    def testInsert(self):
        cols = [('First', 'TEXT'), ('Second', 'REAL')]
        database.create_table(self.DB_NAME, 'test', cols)
        data = ('myname', 'hello', 5.2)
        database.insert(self.DB_NAME, 'test', data)
        self.c.execute('SELECT * FROM test;')
        self.assertEqual(self.c.fetchall()[0], data)

    def testInsertMany(self):
        cols = [('First', 'TEXT'), ('Second', 'REAL')]
        database.create_table(self.DB_NAME, 'test', cols)
        data = [
            ('myname', 'hello', 5.2),
            ('aname', 'again', 99.0),
            ('nambo', 'water', 77.2)
        ]
        database.insert(self.DB_NAME, 'test', data, many=True)
        self.c.execute('SELECT * FROM test;')
        self.assertEqual(self.c.fetchall(), data)

    def testDamage(self):
        db_setup.run(True)
        result = database.get_damage(self.DB_NAME, 'Scissors', 'Paper')
        self.assertEqual(result, 2.0)
        result = database.get_damage(self.DB_NAME, 'Paper', 'Paper_Scissors')
        self.assertEqual(result, 0.5)
