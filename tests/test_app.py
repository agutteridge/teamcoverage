import unittest

from app import main


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()
        main.init_db()

    def tearDown(self):
        main.delete_db()

    def testIndex(self):
        rv = self.app.get('/')
        self.assertEqual(rv.mimetype, 'text/html')
        self.assertIn(b'Scissors', rv.data)

    def testResults(self):
        rv = self.app.get(
            '/results?poke1=Scissorsmon&poke2=Papermon&poke3=Combomon')
        self.assertEqual(rv.mimetype, 'text/html')
        self.assertEqual(
            b"[[1.75, 'Scissors'], " +
            b"[3.25, 'Paper_Scissors'], " +
            b"[9.0, 'Paper']]", rv.data)


if __name__ == '__main__':
    unittest.main()
