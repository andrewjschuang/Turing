import time
from datetime import datetime
from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for)
from sqlalchemy.exc import IntegrityError
from wtforms import (Form, RadioField, StringField, SubmitField, TextAreaField, TextField,
                     validators)


from models.model import User, Project, Task, Questionnaire, Question, Response
from models.shared import db

class SignUp(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[
                      validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[
                         validators.required(), validators.Length(min=3, max=35)])


class Login(Form):
    email = TextField('Email:', validators=[
                      validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[
                         validators.required(), validators.Length(min=3, max=35)])

def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_mapping(config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prod.db'
        app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404


    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = SignUp(request.form)
        if request.method == 'POST':
            if form.validate():
                
                name = request.form['name']
                password = request.form['password']
                email = request.form['email']
                u = User(email=email, name=name, password=password)
                db.session.add(u)
                db.session.commit()
                session['auth'] = {'name': name,
                                'email': email, 'timestamp': time.time()}
                return redirect(url_for('index'))

            else:
                flash('All the form fields are required.', category='error')

        return render_template('signup.html', form=form)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = Login(request.form)
        if request.method == 'POST':
            if form.validate():
                password = request.form['password']
                email = request.form['email']
                user = User.query.filter_by(email=email).first()
                print(user)
                if user:
                    print(user)
                    if user.password == password:
                        session['auth'] = {'name': user.name,
                                        'email': user.email,
                                        'timestamp': time.time()
                                        }
                        return redirect(url_for('index'))
                    else:
                        flash('Authentication failed', category='error')
                else:
                    flash('Authentication failed', category='error')

            else:
                flash('All the form fields are required', category='error')
        return render_template('login.html', form=form)


    @app.route('/', methods=['GET'])
    def index():
        auth = session.get('auth')
        if auth:
            user: User = User.query.filter_by(email=auth.get('email')).first()
            if not user:
                session['auth'] = {}
                return redirect('/login')
            info = user.get_index_data()
            print(info)
            return render_template('index.html', **info)
        return redirect('/login')

    @app.route('/responses')
    def responses():
        auth = session.get('auth')
        if auth:
            user: User = User.query.filter_by(email=auth.get('email')).first()
            User.query.filter_by(email=auth.get('email')).first()
            if not user:
                session['auth'] = {}
                return redirect('/login')
        quests = Questionnaire.query.all()
        return render_template('responses.html', quests=quests)

    @app.route('/respond/<int:ref>', methods=['GET', 'POST'])
    def respond(ref):
        quest = Questionnaire.query.get(ref)
        if not quest:
            print('no questionnaire found with id %s' % ref)
            return abort(404)
        if request.method == 'GET':
            return render_template('feedback.html', name=quest.name, questions=quest.questions)
        elif request.method == 'POST':
            for question_id in request.form:
                question = Question.query.get(question_id)
                resp = Response(question=question.id, rating=request.form.get(question_id))
                db.session.add(resp)
                db.session.commit()
            return render_template('feedback_received.html')

    @app.route('/projects', methods=['GET', 'POST'])
    def projects():
        auth = session.get('auth')
        if auth:
            user: User = User.query.filter_by(email=auth.get('email')).first()
            if not user:
                session['auth'] = {}
                return redirect('/login')
            if request.method == 'POST':
                name = request.form['projectName']
                description = request.form['projectDescription']
                pro = Project(name=name,description=description)
                db.session.add(pro)
                user.project.append(pro)
                db.session.commit()

            grid = user.get_project_grid(3)
            return render_template('projects.html', projectgrid=grid)
        return redirect('/login')


    @app.route('/tasks/user')
    @app.route('/tasks/user/<int:ref>', methods=['GET', 'POST'])
    def user_tasks(ref=None):
        auth = session.get('auth')
        if auth:
            user: User = User.query.filter_by(email=auth.get('email')).first()
            if not user:
                session['auth'] = {}
                return redirect('/login')
            if ref:
                user: User = User.query.filter_by(id=ref).first()
            if not user:
                return abort(404)
            if request.method == 'POST':
                name = request.form.get('taskName')
                description = request.form.get('taskDescription')
                t_time = request.form.get('taskTime')
                if not all((name, description, t_time)):
                    abort(404)
                t_time = datetime.strptime(t_time,'%Y-%m-%dT%H:%M:%S.%fZ')
                n_task: Task = Task(name=name, description=description, end_time=t_time)
                user.tasks.append(n_task)
                db.session.commit()
                return abort(200)
            else:
                return render_template('tasks.html', data=user)

    @app.route('/tasks/project/<int:ref>', methods=['GET', 'POST'])
    def proj_tasks(ref):

        auth = session.get('auth')
        if auth:
            user: User = User.query.filter_by(email=auth.get('email')).first()
            if not user:
                session['auth'] = {}
                return redirect('/login')

            project:Project = Project.query.filter_by(id=ref).first()
            if not project:
                return abort(404)
            if request.method == 'POST':
                name = request.form.get('taskName')
                description = request.form.get('taskDescription')
                t_time = request.form.get('taskDate')
                if not all((name, description, t_time)):
                    abort(404)
                t_time = datetime.strptime(t_time,'%Y-%m-%dT%H:%M:%S.%fZ')
                n_task: Task = Task(name=name, description=description, end_time=t_time)

                project.tasks.append(n_task)
                user.tasks.append(n_task)

                db.session.commit()
                return ('' ,200)
            else:
                return render_template('tasks.html', data=project)

    @app.route('/tasks/task/<int:ref>', methods=['GET', 'POST'])
    def task_tasks(ref):
        auth = session.get('auth')
        if auth:
            user: User = User.query.filter_by(email=auth.get('email')).first()
            if not user:
                session['auth'] = {}
                return redirect('/login')

            task:Task = Task.query.filter_by(id=ref).first()

            if not task:
                return abort(404)
            if request.method == 'POST':
                name = request.form.get('taskName')
                description = request.form.get('taskDescription')
                t_time = request.form.get('taskDate')
                if not all((name, description, t_time)):
                    abort(404)
                t_time = datetime.strptime(t_time,'%Y-%m-%dT%H:%M:%S.%fZ')
                n_task: Task = Task(name=name, description=description, end_time=t_time)

                db.session.add(n_task)
                task.tasks.append(n_task)
                db.session.commit()

                user.tasks.append(n_task)

                db.session.commit()
                print(task, task.tasks)
                print(n_task, n_task.tasks)
                return ('' ,200)
            else:
                print(task, task.tasks)
                return render_template('tasks.html', data=task)

    @app.route('/test', methods=['GET'])
    def test():
        
        return render_template('newQuestionnaire.html')

    @app.route('/questionnaire/<int:ref>', methods=['GET', 'POST'])
    def questionnaire(ref):
        auth = session.get('auth')
        if auth:
            user: User = User.query.filter_by(email=auth.get('email')).first()
            if not user:
                session['auth'] = {}
                return redirect('/login')
            
            task:Task = Task.query.filter_by(id=ref).first()

            if not task:
                return abort(404)
            if request.method == 'POST':
                name = request.form.get('name')
                if not name:
                    return abort(404)
                quest = Questionnaire(name=name,task=task)
                task.questionnaires.append(quest)
                for key, value in request.form.items():
                    if not value or key == 'name':
                        continue
                    else:
                        quest.questions.append(Question(text=value,questionnaire=quest))
                db.session.commit()
        return render_template('newQuestionnaire.html')

    @app.route('/logout', methods=['GET'])
    def logout():
        session.pop('auth')
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    app = create_app()
    db.create_all(app=app)
    app.run(host='localhost', port=3000, debug=True)
