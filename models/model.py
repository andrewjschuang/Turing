from models.shared import db


sub_tasks = db.Table('sub_tasks',
                     db.Column('task_id', db.Integer, db.ForeignKey(
                         'task.id'), primary_key=True),
                     db.Column('task_id', db.Integer, db.ForeignKey(
                         'task.id'), primary_key=True)
                     )


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    end_time = db.Column(db.Date())
    tasks = db.relationship('Task', secondary=sub_tasks, lazy='subquery',
                            backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.email


user_tasks = db.Table('task_user',
                      db.Column('task_id', db.Integer, db.ForeignKey(
                          'task.id'), primary_key=True),
                      db.Column('user_email', db.Integer, db.ForeignKey(
                          'page.id'), primary_key=True)
                      )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    tasks = db.relationship('Task', secondary=user_tasks, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.email


project_tasks = db.Table('project_tasks',
                         db.Column('project_id', db.Integer, db.ForeignKey(
                             'project.id'), primary_key=True),
                         db.Column('task_id', db.Integer, db.ForeignKey(
                             'task.id'), primary_key=True)
                         )


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    tasks = db.relationship('Task', secondary=project_tasks, lazy='subquery',
                            backref=db.backref('project', lazy=True))

    def add_task(self, name, description, end_time):
        self.tasks.append(
            Task(name=name, description=description, end_time=end_time)
        )
        db.session.update(self)
        db.session.commit()
