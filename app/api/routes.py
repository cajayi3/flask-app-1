from flask import Blueprint, request, jsonify, render_template
from ..helpers import token_required
from ..models import db, Car, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {''}

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    car = request.json['car']
    name = request.json['name']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    gas = request.json['gas']
    mpg = request.json['mpg']
    engine = request.json['engine']
    user_token = current_user_token.token

    print(f'TEST: {current_user_token.token}')

    car = Car(car, name, model, year, color, gas, mpg, engine, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car.schema.dump(car)
    return jsonify(response)


@api.route('/cars', methods = ['GET']) 
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


@api.route('cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car =  Car.query.get(id)
    car.car = request.jsonn['car']
    car.name = request.json['name']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json['color']
    car.gas = request.json['gas']
    car.mpg = request.json['mpg']
    car.engine = request.json['engine']
    car.user_token = current_user_token.token

    db.session.commit()
    response = cars_schema.dump(car)
    return jsonify(response)


@api.route('cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car =  Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = cars_schema.dump(car)
    return jsonify(response)