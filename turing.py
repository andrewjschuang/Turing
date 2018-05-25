from flask import Flask, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models.shared import db
import json

app = Flask(__name__)
app.config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    db.create_all()
    app.run(host='localhost', port=3000, debug=True)
