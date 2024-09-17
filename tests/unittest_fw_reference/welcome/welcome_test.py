import unittest


class WelcomeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Welcome -- This will run only one before everything')

    def setUp(self):
        print('Welcome -- This will run before every test')

    def test_welcome_functionality_one(self):
        print('Welcome -- Verifying a functionality in the welcome page')

    def tearDown(self):
        print('Welcome -- This will run after every test')

    @classmethod
    def tearDownClass(cls):
        print('Welcome -- This is running only one after all tests')


if __name__ == '__main__':
    unittest.main(verbosity=2)
