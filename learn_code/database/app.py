import os
import sys
import urllib.parse

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from  config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user' # 定义表名
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Movie(db.Model):
    __tablename__ = 'movie'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60))
    year: Mapped[str] = mapped_column(String(4))
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.title,
            'year': self.year
        }

# 创建表单
@app.route('/create_tables')
def create_tables():
    # db.create_all()
    User.__table__.create(db.engine)
    return jsonify({'message': 'All tables create successfully!'})


# 删除表单
@app.route('/drop_tables')
def drop_tables():
    # db.drop_all()
    User.__table__.drop(db.engine)
    return jsonify({'message': 'All tables drop successfully!'})


# 添加用户数据
# win: curl -X POST http://127.0.0.1:5001/add_users  -H "Content-Type: application/json" -d {\"name\":\"Tom\"}
@app.route('/add_users', methods=['POST'])
def add_user():
    print("原始请求体：", request.data)
    print("请求头：", request.headers)
    data = request.get_json()
    user = User(name=data['name'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'})


# 查询用户数据
# win: curl -X POST http://127.0.0.1:5001/get_users
@app.route('/get_users', methods=['POST'])
def get_users():
    users = User.query.all()
    result = [u.to_dict() for u in users]
    return jsonify(result)


# 更新用户数据
# curl -X PUT http://127.0.0.1:5001/users/1 -H "Content-Type: application/json" -d {\"name\": \"张三丰\"}
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.name = data.get('name',user.name)
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'})


# 删除用户数据
# curl -X DELETE http://127.0.0.1:5001/users/1
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User delete successfully!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
