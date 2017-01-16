import unittest
import sqlite3

from app import database


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
