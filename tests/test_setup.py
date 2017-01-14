import unittest
from unittest import mock
import sqlite3

from app import db_setup


class SetupTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SetupTest, self).__init__(*args, **kwargs)
        self.DB_NAME = 'testing.db'

    def setUp(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.c = self.conn.cursor()
        self.c.execute('DROP TABLE IF EXISTS types;')
        self.c.execute('DROP TABLE IF EXISTS dex;')
        self.conn.commit()

    @mock.patch.multiple('app.db_setup',
                         generate_dex_table=mock.DEFAULT,
                         generate_types_table=mock.DEFAULT)
    def testRun(self,
                generate_dex_table,
                generate_types_table):
        db_setup.run(self.DB_NAME)
        generate_dex_table.assert_called_once()
        generate_types_table.assert_called_once()

    def testGenerateTypesTable(self):
        db_setup.generate_types_table(self.DB_NAME)
        self.c.execute("SELECT Paper FROM types WHERE Name='Scissors';")
        self.assertEqual(self.c.fetchone()[0], 2.0)

    def testGenerateDexTable(self):
        db_setup.generate_dex_table(self.DB_NAME)
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
