from os import name
import unittest

from app import app, db, Movie, User

class WatchlistTestCase(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING = True, 
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        )

        db.create_all

        user = User(name = 'Test', username = 'test')
        user.set_password('123')

        movie = Movie(title = 'Test Movie Title', year = 2000)

        db.session.add_all([user,movie])
        db.session.commit()

        self.client = app.test_client() # create client to test
        self.runner = app.test_cli_runner()
        # app.test_cli_runner app.test_client 
        # both of them are built-in test function oin falsk

    def tearDown(self):
        """ close app and clean everything"""
        db.session.remove()

        db.drop_all()


    def test_app_exist(self):
        """ exist_testing by none (if app not exist then the object is nono)"""
        self.assertIsNotNone(app)


    def test_app_is_testing(self):
        """ test_app_is_testing by give app.config"""
        self.assertTrue(app.config['TESTING'])

    