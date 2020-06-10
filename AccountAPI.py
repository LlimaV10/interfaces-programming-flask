from flask import Blueprint, request, jsonify
from init import db, ma

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(200))

  def __init__(self, name, password):
    self.name = name
    self.password = password

class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'password')

user_schema = UserSchema()

account_api = Blueprint('account_api', __name__)

# test request
users_schema = UserSchema(many=True)
@account_api.route("/account", methods=['GET'])
def get():
  all_users = User.query.all()
  return users_schema.jsonify(all_users)

@account_api.route("/account", methods=['POST'])
def login():
  name = request.json['name']
  password = request.json['password']

  user = User.query.filter_by(name=name).first()
  if user is None:
    return jsonify({'msg': 'User is not registered'}), 401
  
  if user.password != password:
    return jsonify({'msg': 'Incorrect password'}), 401

  return user_schema.jsonify(user)

@account_api.route("/account", methods=['PUT'])
def register():
  name = request.json['name']
  password = request.json['password']

  if (name == ''):
    return jsonify({'msg': 'Incorrect name'}), 401

  if (password == ''):
    return jsonify({'msg': 'Incorrect password'}), 401

  new_user = User(name, password)

  db.session.add(new_user)
  db.session.commit()

  return user_schema.jsonify(new_user)
