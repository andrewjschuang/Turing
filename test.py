from flask_testing import TestCase

from models.shared import db
from models.model import User, Task, Project
from turing import create_app

import unittest


class MyTest(TestCase):
    def create_app(self):
        config = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
            'TESTING': True,
            'SECRET_KEY': 'secret',
            'SQLALCHEMY_TRACK_MODIFICATIONS': True
        }
        return create_app(config)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_nothing(self):
        assert True

    def test_user(self):
        user = User(email='em', username='us', password='pass')
        db.session.add(user)
        db.session.commit()
        assert user in db.session

    def test_project(self):
        project = Project(name='n',description='desc')
        db.session.add(project)
        db.session.commit()
        assert project in db.session
        

    def test_task(self):
        task =  Task(name='n', description='desc')
        db.session.add(task)
        db.session.commit()
        assert task in db.session


if __name__ == '__main__':
    unittest.main()
