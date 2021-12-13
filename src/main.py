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

#### ENDPOINTS PARA CREAR LA BASE DE DATOS AUTOMÁTICAMENTE ####

# CREAR VARIOS USUARIOS: FUNCIONA
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


# CREAR VARIOS PERSONAJES: FUNCIONA
@app.route('/create-characters', methods=['GET'])
def list_of_characters():

    data = {
        "characters": [
            {
                "name": "Darth Vader"        
            },
            {
                "name": "R2-D2"        
            },
            {
                "name": "Luke Skywalker"        
            },
            {
                "name": "Yoda"        
            }
        ],
    }

    for character in data['characters']:
        new_character = Character(name = character['name'])
        db.session.add(new_character)

    db.session.commit()
    
    return jsonify({"msg": "Characters loaded"})


# CREAR VARIOS PLANETAS: FUNCIONA
@app.route('/create-planets', methods=['GET'])
def list_of_planets():

    data = {
        "planets": [
            {
                "name": "ALDERAAN"        
            },
            {
                "name": "ENDOR"        
            },
            {
                "name": "NABOO"        
            },
            {
                "name": "TATOOINE"        
            }
        ],
    }

    for planet in data['planets']:
        new_planet = Planet(name = planet['name'])
        db.session.add(new_planet)

    db.session.commit()
    
    return jsonify({"msg": "Planets loaded"})

#### GET ####

# Obtener la lista de todos los usuarios: FUNCIONA
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()  # busco en la BBDD todos los usuarios
    users_serialized = list(map(lambda user: user.serialize(), users)) # del array de usuarios (users), consigo cada usuario serializado

    return jsonify(users_serialized), 200 

# Obtener la lista de todos los personajes de la BBDD: FUNCIONA
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    characters_serialized = list(map(lambda character: character.serialize(), characters)) # del array de characters, consigo cada character serializado

    return jsonify(characters_serialized)   

# Obtener la información de un personaje: FUNCIONA
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)

    return jsonify(character.serialize())        

# Obtener la lista de todos los planetas de la BBDD: FUNCIONA
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    planets_serialized = list(map(lambda planet: planet.serialize(), planets)) # del array de planetas, consigo cada planeta serializado

    return jsonify(planets_serialized)        

# Obtener la información de un planeta: FUNCIONA
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)

    return jsonify(planet.serialize())

# Obtener la lista de todos los favoritos de un usuario: FUNCIONA
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    #user = User.query.get(user_id) # busco a usuario por id (NO HACE FALTA PORQUE UTILIZO EL USER_ID EN LA TABLA DE RELACIONES -siguiente línea)

    favorites_characters = FavoriteCharacter.query.filter_by(user_id=user_id) # busco en la tabla FavoriteCharacter los personajes favoritos de dicho usuario (aquí sólo obtengo su id)
    #favs_characters = list(map(lambda fav_character: fav_character.serialize(), favorites_characters)) # por cada personaje fav de este usuario, obtengo los datos serializados
    favs_characters = list(map(lambda fav_character: Character.query.get(fav_character.character_id).name, favorites_characters)) # por cada personaje fav de este usuario, obtengo su nombre (a partir de su id)

    favorites_planets = FavoritePlanet.query.filter_by(user_id=user_id)
    favs_planets = list(map(lambda fav_planet: Planet.query.get(fav_planet.planet_id).name, favorites_planets))

    return jsonify(favs_characters, favs_planets), 200    


#### POST ####

# Añadir un planeta favorito a un usuario: FUNCIONA
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    body = request.get_json()

    fav = FavoritePlanet(user_id=body['user_id'], planet_id=planet_id)
   
    db.session.add(fav)
    db.session.commit()

    response_body = {
        "State": "Planeta favorito añadido"
    }    

    return jsonify(response_body), 200

# Añadir un personaje favorito a un usuario: FUNCIONA
@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    body = request.get_json()

    fav = FavoriteCharacter(user_id=body['user_id'], character_id=character_id)
   
    db.session.add(fav)
    db.session.commit()

    response_body = {
        "State": "Personaje favorito añadido"
    }    

    return jsonify(response_body), 200

#### DELETE ####

# Eliminar un planeta favorito de un usuario: FUNCIONA
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    fav_planet = FavoritePlanet.query.get(planet_id)
    user = User.query.get(10)

    if not fav_planet: 
        return jsonify({"fail": "Planeta favorito no encontrado"}), 404

    db.session.delete(fav_planet)
    db.session.commit()

    return jsonify({"success": "Planeta favorito eliminado"}), 200   

# Eliminar un personaje favorito de un usuario: FUNCIONA
@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    fav_character = FavoriteCharacter.query.get(character_id)
    user = User.query.get(10)

    if not fav_character: 
        return jsonify({"fail": "Personaje favorito no encontrado"}), 404

    db.session.delete(fav_character)
    db.session.commit()

    return jsonify({"success": "Personaje favorito eliminado"}), 200   


# this only runs if `$ python src/main.py` is executed
# if __name__ == '__main__':
#     PORT = int(os.environ.get('PORT', 3000))
#     app.run(host='0.0.0.0', port=PORT, debug=False)
