from flask import Flask, abort, render_template, request, flash, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from sqlalchemy.exc import IntegrityError
from models.shared import db
from models.model import User
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
db.init_app(app)


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[
                      validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[
                         validators.required(), validators.Length(min=3, max=35)])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():

    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        if form.validate():
            username = request.form['name']
            password = request.form['password']
            email = request.form['email']

            print(username, email, password)
            u = User(email=email, username=username, password=password)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('foo'))

        else:
            flash('All the form fields are required.', category='error')

    return render_template('signup.html', form=form)


if __name__ == '__main__':
    db.create_all(app=app)
    app.run(host='localhost', port=3000, debug=True)
