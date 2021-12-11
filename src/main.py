"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoint para CREAR VARIOS USUARIOS (y no tener que crear uno a uno en el flask admin):
@app.route('/create-users', methods=['GET'])
def list_of_users():

    data = {
        "users": [
            {
                "email": "usuario1@gmail.com",
                "password": "1234",
                "is_active": True            
            },
            {
                "email": "usuario2@gmail.com",
                "password": "1994",
                "is_active": True              
            },
            {
                "email": "usuario3@gmail.com",
                "password": "0000",
                "is_active": True              
            },
            {
                "email": "usuario4@gmail.com",
                "password": "8753",
                "is_active": True              }
        ],
    }

    for user in data['users']:
        new_user = User(email = user['email'], password = user['password'], is_active = user['is_active'])
        db.session.add(new_user)

    db.session.commit()
    
    return jsonify({"msg": "Users loaded"})

# Obtener la lista de todos los usuarios:
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()  # busco en la BBDD todos los usuarios

    users_serialized = list(map(lambda user: user.serialize(), users)) # del array de usuarios (users), consigo cada usuario serializado

    return jsonify(users_serialized), 200 

# Obtener la lista de todos los favoritos de un usuario: AMBAS OPCIONES DEVUELVEN SIEMPRE "[], 200" ???
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    """ user = User.query.get(user_id)

    favs_characters = FavoriteCharacter.query.filter_by(user_id=user_id) # busco en la tabla FavoriteCharacter los personajes favoritos del usuario (mediante el user_id)

    favs_planets = FavoritePlanet.query.filter_by(user_id=user_id)

    favorites = []

    for character in favs_characters:
        favorites.append(character.serialize())  

    for planet in favs_planets:
        favorites.append(planet.serialize())          

    return jsonify(favorites), 200  """

    user = User.query.get(user_id)

    favorites_characters = FavoriteCharacter.query.filter_by(user_id=user_id) 

    favs_characters = list(map(lambda fav_character: Character.query.get(favoriteCharacter.character_id).serialize(), favorites_characters)) # para cada inscripción, busco el id de usuario para de ahí sacar el propio usuario

    return jsonify(favs_characters), 200    

# Añadir un planeta favorito a un usuario: NO FUNCIONa
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    planet = Planet.query.get(planet_id)
    user = User.query.get(1)
    user.favoritePlanets.append(planet_id)
    db.session.commit()
    return jsonify(planet.serialize()), 200


# this only runs if `$ python src/main.py` is executed
# if __name__ == '__main__':
#     PORT = int(os.environ.get('PORT', 3000))
#     app.run(host='0.0.0.0', port=PORT, debug=False)
