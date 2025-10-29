from flask import Flask, render_template
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)
name = 'Grey Li'
users = ['Tom', 'Bob', 'Grey Li']
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

@app.route('/')
def index():
    return render_template('index.html', name=name,movies=movies)


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
class Movie(db.Model):
    __tablename__ = 'movie'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(60))
    year: Mapped[str] = mapped_column(String(10))
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year
        }
@app.route('/create_tables/<table_name>', methods=['GET', 'POST'])
def create_tables(table_name):
    table_name = f'{table_name}'
    if table_name == 'user':
        User.__table__.create(db.engine)
    elif table_name == 'movie':
        Movie.__table__.create(db.engine)
    elif table_name == 'all':
        User.__table__.create(db.engine)
        Movie.__table__.create(db.engine)
        table_name = 'user,movie'
    else:
        return jsonify({'message': 'Table create false!!!'})
    return jsonify({'message': f'Table {table_name} create successfully!'})
@app.route('/drop_tables/<table_name>', methods=['POST'])
def drop_tables(table_name):
    if table_name == 'user':
        User.__table__.drop(db.engine)
    elif table_name == 'movie':
        Movie.__table__.drop(db.engine)
    elif table_name == 'all':
        User.__table__.drop(db.engine)
        Movie.__table__.drop(db.engine)
    return jsonify({'message': f'Table {table_name} drop successfully!'})
@app.route('/add_users', methods=['POST'])
def add_user():
    # data = request.get_json()
    # user = User(name=data['name'])
    for user in users:
        print(f'user: {user}')
        user_name = User(name=user)
        db.session.add(user_name)
        db.session.commit()
    return jsonify({'message': 'User created successfully!'})
@app.route('/add_movies', methods=['POST'])
def add_movie():
    for movie in movies:
        movie = Movie(title=movie['title'],year=movie['year'])
        db.session.add(movie)
        db.session.commit()
        print(f'add {movie} successfully!')
    return jsonify({'message': 'Movie added successfully!'})
# 查询用户数据
# win: curl -X POST http://127.0.0.1:5001/get_users

@app.route('/get_users', methods=['GET','POST'])
def get_users():
    user_list = User.query.all()

    user_result = [u.to_dict() for u in user_list]
    print(f'user: {user_result}')
    movie_list = Movie.query.all()
    movie_result = [u.to_dict() for u in movie_list]
    # return jsonify({'users': user_result,'movies': movie_result})
    return render_template('query.html', name=random.choice(user_result)['name'], users=user_result, movies=movie_result)
@app.errorhandler(404)
def page_not_found(error):
    user = db.session.execute(select(User)).scalar()
    return render_template('404.html', user=user), 404


if __name__ == '__main__':
    app.run()
