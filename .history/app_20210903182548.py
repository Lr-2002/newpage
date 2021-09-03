from flask import Flask ,render_template,url_for

from flask_sqlalchemy import SQLAlchemy

import os

import sys

import click



app = Flask(__name__)




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path,'data.db')   
#   / / / / 是文件的绝对路径

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

db = SQLAlchemy(app)


@app.cli.command()
@click.option('--drop',is_flag=True,help = 'Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialize database.')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))

@app.cli.command()
def forge():
    


@app.route('/')
def hello():
    user  = User.query.first()
    movies = Movie.query.all()

    return render_template('index.html',user = user ,movies = movies)


# if __name__ == '__main__':
#     app.run()
