from flask import Flask ,render_template,url_for

from flask_sqlalchemy import SQLAlchemy

import os

import sys

import click



app = Flask(__name__)

db = SQLAlchemy(app)


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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie():
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))



# name = 'Grey Li'
# movies = [
#     {'title': 'My Neighbor Totoro', 'year': '1988'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'A Perfect World', 'year': '1993'},
#     {'title': 'Leon', 'year': '1994'},
#     {'title': 'Mahjong', 'year': '1996'},
#     {'title': 'Swallowtail Butterfly', 'year': '1996'},
#     {'title': 'King of Comedy', 'year': '1999'},
#     {'title': 'Devils on the Doorstep', 'year': '1999'},
#     {'title': 'WALL-E', 'year': '2008'},
#     {'title': 'The Pork of Music', 'year': '2012'},
# ]


# @app.route('/static/<name>')
# def static(name):
#     # url_for('static')
#     return name



@app.route('/')
def hello():
    return render_template('index.html',name=name,movies = movies)


# if __name__ == '__main__':
#     app.run()
