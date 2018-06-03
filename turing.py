from flask import Flask, abort, render_template, request, flash, redirect, url_for, session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from sqlalchemy.exc import IntegrityError
from models.shared import db
from models.model import User
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
db.init_app(app)


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUp(request.form)
    if request.method == 'POST':
        if form.validate():
            username = request.form['name']
            password = request.form['password']
            email = request.form['email']
            u = User(email=email, username=username, password=password)
            db.session.add(u)
            db.session.commit()
            session['auth'] = {'name': username,
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
            if user:
                if user.password == password:
                    session['auth'] = {'name': user.username,
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
        return render_template('index.html')
    else:
        return redirect('/login')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('auth')
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all(app=app)
    app.run(host='localhost', port=3000, debug=True)
