#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# @app.route('/restaurants')
# def restaurants():

#     pass

class GetRestaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        restaurants_dict = [restaurant.to_dict(rules=("-restaurant_pizzas",)) for restaurant in restaurants]
        response = make_response(restaurants_dict, 200)
        return response
api.add_resource(GetRestaurants, "/restaurants")


class GetRestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            message = {"error": "Restaurant not found"}
            return make_response(message, 404)
        restaurant_dict = restaurant.to_dict(rules=("-restaurant_pizzas", "pizzas"))
        response = make_response(restaurant_dict, 200)
        return response
    
    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            message = {"error": "Restaurant not found"}
            return make_response(message, 404)
        db.session.delete(restaurant)
        db.session.commit()
        message = {"message": "Restaurant has been deleted successfully"}
        return make_response(message, 200)

api.add_resource(GetRestaurantByID, "/restaurants/<int:id>")


class GetPizzas(Resource):
    def get(self):
        pizzas = Restaurant.query.all()
        pizzas_dict = [pizza.to_dict(rules=("-restaurant_pizzas",)) for pizza in pizzas]
        response = make_response(pizzas_dict, 200)
        return response
api.add_resource(GetPizzas, "/pizzas")


class GetRestaurantPizzas(Resource):
    def get(self):
        r_pizzas = RestaurantPizza.query.all()
        r_pizzas_dict = [r_pizza.to_dict(rules=("-pizza.restaurant_pizzas",)) for r_pizza in r_pizzas]
        response = make_response(r_pizzas_dict, 200)
        return response

    
    def post(self):
        try:
            new_r_p = RestaurantPizza(
                price=request.get_json()["price"],
                pizza_id=request.get_json()["pizza_id"],
                restaurant_id=request.get_json()["restaurant_id"]
            )
            db.session.add(new_r_p)
            db.session.commit()

            pizza = Pizza.query.filter_by(id=new_r_p.pizza_id).first()
            response = make_response(pizza.to_dict(), 201)
        except ValueError:
            message = {"error": "Invalid input"}
            response = make_response(message, 422)
        return response

api.add_resource(GetRestaurantPizzas, "/restaurant_pizzas")




if __name__ == '__main__':
    app.run(port=5555, debug=True)
