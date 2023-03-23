from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata = metadata)

# Add models here
class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurant_pizzas = db.relationship("RestaurantPizza", backref="pizza")
    restaurants = association_proxy("restaurant_pizzas", "restaurant")

    serialize_rules = ("-restaurant_pizzas.pizza", "-restaurant_pizzas.restaurant", 
                       "-restaurants.pizzas", "-created_at", "-updated_at")


    def __repr__(self):
        return f"""<Pizza {self.id}; Name: {self.name}; Ingredients: {self.ingredients}.>"""


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = db.relationship("RestaurantPizza", backref="restaurant")
    pizzas = association_proxy("restaurant_pizzas", "pizza")

    serialize_rules = ("-restaurant_pizzas.pizza", "-restaurant_pizzas.restaurant", 
                       "-pizzas.restaurants", "-pizzas.restaurant_pizzas", "-created_at", "-updated_at")

    def __repr__(self):
        return f"""<Restaurant {self.id}; Name: {self.name}; Address: {self.address}.>"""


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))


    serialize_rules = ("-pizza.restaurant_pizzas", "-restaurant.restaurant_pizzas", 
                       "-pizzas.restaurants", "-restaurants.pizzas",
                       "-created_at", "-updated_at")

    @validates("price")
    def validate_price(self, key, price):
        if not price or not 1 <= price <= 30:
        # if price < 1 or  price > 30:
            raise ValueError("must have a price between 1 and 30")
        return price


    def __repr__(self):
        return f"""<RestaurantPizza {self.id}; Price: {self.price}.>"""

    # @validates('price')
    # def validates_strength(self, key, strength):
    #     if not strength == 'Strong' and not strength == 'Weak' and not strength == 'Average':
    #         raise ValueError("Strength must be Strong, Weak, or Average")
    #     return strength