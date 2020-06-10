from flask import Blueprint, request, jsonify

from init import db, ma

# Product Type
class ProductType(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)

  def __init__(self, name):
    self.name = name

class ProductTypeSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name')

product_type_schema = ProductTypeSchema()
product_types_schema = ProductTypeSchema(many=True)

# Product
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), unique=True)
  type_id = db.Column(db.Integer)
  image_url = db.Column(db.String(200))
  description = db.Column(db.String(1000))

  def __init__(self, type_id, title, image_url, description):
    self.type_id = type_id
    self.title = title
    self.image_url = image_url
    self.description = description

class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'type_id', 'title', 'image_url', 'description')

class ProductsSchema(ma.Schema):
  class Meta:
    fields = ('id', 'type_id', 'title', 'image_url')

product_schema = ProductSchema()
products_schema = ProductsSchema(many=True)

product_api = Blueprint('product_api', __name__)

@product_api.route("/products", methods=['GET'])
def get_products():
  all_products = Product.query.all()
  return products_schema.jsonify(all_products)

@product_api.route("/products/<type_id>", methods=['GET'])
def get_products_by_type(type_id):
  products = Product.query.filter_by(type_id=type_id).all()
  return products_schema.jsonify(products)

@product_api.route("/product/<id>", methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

@product_api.route("/product/<id>", methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()
  
  return product_schema.jsonify(product)

@product_api.route("/product", methods=['POST'])
def add_product():
  type_id = request.json['type_id']
  title = request.json['title']
  image_url = request.json['image']
  description = request.json['description']

  db_type = ProductType.query.filter_by(id=type_id).first()
  if db_type is None:
    return jsonify({'msg': 'Type is invalid'}), 206

  new_product = Product(type_id, title, image_url, description)

  db.session.add(new_product)
  db.session.commit()
  return product_schema.jsonify(new_product)

@product_api.route("/product_type", methods=['GET'])
def get_types():
  types = ProductType.query.all()
  return product_types_schema.jsonify(types)

@product_api.route("/product_type/<id>", methods=['GET'])
def get_type(id):
  type = ProductType.query.filter_by(id=id).first()
  return product_type_schema.jsonify(type)

@product_api.route("/product_type", methods=['POST'])
def add_type():
  name = request.json['name']

  new_type = ProductType(name)
  db.session.add(new_type)
  db.session.commit()
  return product_type_schema.jsonify(new_type)
