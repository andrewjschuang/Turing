from flask_testing import TestCase

from models.shared import db
from models.model import User, Task, Project, Question, Response, Questionnaire
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

    def test_usr_add_tsk2_prj(self):
        user = User(email='em', username='us', password='pass')
        db.session.add(user)
        db.session.commit()
        
        project = Project(name='n',description='desc')
        db.session.add(project)
        user.project.append(project)
        db.session.commit()

        project: Project= User.query.filter_by(email='em').first().project[0]

        task = Task(name='n', description='desc')
        db.session.add(task)

        project.tasks.append(task)
        db.session.commit()

        assert user.project[0].tasks[0] == task


    def test_sub_tasks(self):
        task = Task(name='n', description='desc')
        db.session.add(task)
        assert task in db.session

        s_task = Task(name='n', description='desc')
        db.session.add(s_task)
        assert task in db.session

        db.session.commit()
        task.tasks.append(s_task)

        
        db.session.commit()
        assert task.tasks[0] == s_task
    
    def test_questionnaire(self):
        questionnaire = Questionnaire(name='Questions')
        db.session.add(questionnaire)

        question0 = Question(text="ola ?", questionnaire=questionnaire)
        question1 = Question(text="tudo bem ?", questionnaire=questionnaire)

        questionnaire.questions.append(question0)
        questionnaire.questions.append(question1)

        for i in range(10):
            question0.responses.append(Response(rating=5,question=question0))

        for i in range(10):
            question1.responses.append(Response(rating=5,question=question1))

        rs = [x.rating for x in questionnaire.questions[0].responses]
        assert sum(rs)/len(rs) == 5

        rs = [x.rating for x in questionnaire.questions[1].responses]
        assert sum(rs)/len(rs) == 5

       
        



if __name__ == '__main__':
    unittest.main()
