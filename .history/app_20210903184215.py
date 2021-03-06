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
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.route('/')
def hello():
    user  = User.query.first()
    movies = Movie.query.all()

    return render_template('index.html',user = user ,movies = movies)


# if __name__ == '__main__':
#     app.run()
@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html',user=user),404
@app.context_processor
def inject_user():
    user =  User.query.first()
    return 