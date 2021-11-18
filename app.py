from operator import methodcaller
import re
from flask import Flask, render_template, url_for, request, redirect, flash
import flask
from flask.templating import render_template_string

from flask_sqlalchemy import SQLAlchemy

import os

from flask_login import LoginManager, login_required, logout_user, current_user, UserMixin, login_user

import click
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os\
    .path.join(app.root_path, 'data.db')
#   / / / / 是文件的绝对路径

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)
print(dir(db.Model))

@app.cli.command()
@click.option('--drop', is_flag=True, help = 'Create after drop.')
def initdb(drop):
    print('trying to drop the db')
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialize database.')


class User(db.Model, UserMixin):
    """User is a database user"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    name = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password) 

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

@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid data')
            return redirect(url_for('edit', movie_id = movie_id))
        movie.title = title
        movie.year = year
        # db.session.add(movie)
        db.session.commit()
        flash('Item created')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item Deleted')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated():
            flash('You are not authenticated,Please re-login')
            return redirect(url_for('index'))
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid request')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html',user=user),404
@app.context_processor
def inject_user():
    user =  User.query.first()
    return dict(user = user)



@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='the password')
def admin(username, password):
    """ creat user """
    db.create_all()
    
    user = User.query.first()
    
    if user is not None:
        click.echo('Updating user ----')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user ----')
        user = User(username = username, name = 'Admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('Done')

# if __name__ == '__main__':
#     username = '123123'
#     password = '123123'
#     admin(['--username', username, '--password', password])


login_manager = LoginManager(app)
# login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    # print("--------------------------user info ---------------------------------\n",user)
    return user


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid username or password,Please check it out')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            print(user)
            login_user(user)
            flash('Successfully logged in')
            return redirect(url_for('index'))

        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))



@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        
        if not name or len(name)>20:
            flash('Invalid input')
            return redirect(url_for('settings'))

        current_user.name = name

        db.session.commit()
        flash('Name changed successfully')
        return redirect(url_for('index'))
    return render_template('settings.html')
