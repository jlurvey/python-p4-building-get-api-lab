#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
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

@app.route('/bakeries')
def bakeries():
    bakeries_list = [bakery.to_dict() for bakery in Bakery.query.all()]
    return jsonify(bakeries_list)


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    
    baked_goods = [goods.to_dict() for goods in bakery.baked_goods]
    
    bakery_data = bakery.to_dict()
    
    bakery_data['baked_goods'] = baked_goods
    
    return jsonify(bakery_data)


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    sorted_baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    sorted_baked_goods_list = [goods.to_dict() for goods in sorted_baked_goods]
    return jsonify(sorted_baked_goods_list)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first().to_dict()
    return jsonify(most_expensive_baked_good)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
