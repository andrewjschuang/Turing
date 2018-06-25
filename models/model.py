from models.shared import db
from datetime import datetime


class Task(db.Model):
    __tablename__ = 'task'

    """Task class contains subTasks"""
    id = db.Column(db.Integer, primary_key=True)
    changed_at = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    end_time = db.Column(db.Date())
    supertask = db.Column(db.Integer, db.ForeignKey('task.id'))
    tasks = db.relationship('Task',
                        # cascade deletions
                        cascade="all",

                        # many to one + adjacency list - remote_side
                        # is required to reference the 'remote' 
                        # column in the join condition.
                        backref=db.backref("parent", remote_side='Task.id'),

                    ) 

    


user_tasks = db.Table('task_user',
                      db.Column('task_id', db.Integer, db.ForeignKey(
                          'task.id'), primary_key=True),
                      db.Column('user_id', db.Integer, db.ForeignKey(
                          'user.id'), primary_key=True)
                      )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    changed_at = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    tasks = db.relationship('Task', secondary=user_tasks, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def add_task(self, id):
        task = Task.query.filter_by(id=id).first()
        if task:
            self.tasks.append(task)
            db.session.update(self)
            db.session.commit()
        else:
            raise Exception()
    
    def get_project_grid(self, n):
        grid = []
        for i in range(0, len(self.project), n):
            grid.append(self.project[i:i + n])
        return grid


    def get_index_data(self):
        tasks = []
        projects = []
        for count, task in enumerate(sorted(self.tasks, key=(lambda x:x.end_time))):
            if count >= 5:
                break
            else:
                tasks.append(task)
        for count, project in enumerate(sorted(self.project, key=(lambda x:x.name))):
            if count >= 5:
                break
            else:
                projects.append(project)
        return {'tasks': tasks, 'projects': projects}


project_tasks = db.Table('project_tasks',
                         db.Column('project_id', db.Integer, db.ForeignKey(
                             'project.id'), primary_key=True),
                         db.Column('task_id', db.Integer, db.ForeignKey(
                             'task.id'), primary_key=True)
                         )

project_users = db.Table('project_users',
                         db.Column('project_id', db.Integer, db.ForeignKey(
                             'project.id'), primary_key=True),
                         db.Column('user_id', db.Integer, db.ForeignKey(
                             'user.id'), primary_key=True)
                         )


class Project(db.Model):
    """Project Class contains link to the user that interact with this project,
        the top level tasks related to id"""
    id = db.Column(db.Integer, primary_key=True)
    changed_at = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())
    name = db.Column(db.String(80))
    description = db.Column(db.String(250))
    tasks = db.relationship('Task', secondary=project_tasks, lazy='subquery',
                            backref=db.backref('project', lazy=True))
    users = db.relationship('User', secondary=project_users, lazy='subquery',
                            backref=db.backref('project', lazy=True))

    def add_task(self, name, description, end_time):
        """Adds a new Task to this Project"""
        self.tasks.append(
            Task(name=name, description=description, end_time=end_time)
        )
        db.session.update(self)
        db.session.commit()

    def add_user(self, em_usname):
        """Adds existing user to thihs project"""
        user = User.query.filter_by(email=em_usname).first()
        if not user:
            user = User.query.filter_by(username=em_usname).first()
        if user:
            self.users.append(user)
            db.session.update(self)
            db.session.commit()
        else:
            raise Exception()
