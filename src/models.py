from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favoriteCharacters = db.relationship('FavoriteCharacter', backref=db.backref('user', lazy=True))

    favoritePlanets = db.relationship('FavoritePlanet', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.Integer())
    hair_color = db.Column(db.String(50))
    skin_color = db.Column(db.String(50)) 
    eye_color = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    birth_year = db.Column(db.String(50))

    favoriteCharacters = db.relationship('FavoriteCharacter', backref=db.backref('character', lazy=True))


    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "name": self.name,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "birth_year": self.birth_year    
        }  

class Planet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer())
    climate = db.Column(db.String(50))
    diameter = db.Column(db.Integer()) 
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.Integer())

    favoritePlanets = db.relationship('FavoritePlanet', backref=db.backref('planet', lazy=True))


    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "diameter": self.diameter,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }               

class FavoriteCharacter(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')) # ondelete: permite eliminar datos de las tablas secundarias automáticamente cuando elimina los datos de la tabla principal
    character_id = db.Column(db.Integer(), db.ForeignKey('character.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class FavoritePlanet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')) # ondelete: permite eliminar datos de las tablas secundarias automáticamente cuando elimina los datos de la tabla principal
    planet_id = db.Column(db.Integer(), db.ForeignKey('planet.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }
