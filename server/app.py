#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = Bakery.query.all()
    bakery_data = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakery_data), 200

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return jsonify({"error": f"Bakery with id {id} not found"}), 404
    bakery_dict = bakery.to_dict()
    bakery_dict['baked_goods'] = [good.to_dict() for good in bakery.baked_goods]
    return jsonify(bakery_dict), 200

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_data = [good.to_dict() for good in baked_goods]
    return jsonify(baked_goods_data), 200

@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not most_expensive:
        return jsonify({"message": "No baked goods available"}), 200
    return jsonify(most_expensive.to_dict()), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
