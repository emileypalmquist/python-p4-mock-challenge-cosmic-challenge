from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import ipdb

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    missions = db.relationship('Mission', back_populates='planet')
    scientists = association_proxy('missions', 'scientist')

    serialize_rules = ('-missions.planet',)

    def __repr__(self):
        return f'<Planet id={self.id} name={self.name} >'


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    field_of_study = db.Column(db.String, nullable=False)

    missions = db.relationship('Mission', back_populates="scientist")
    planets = association_proxy('missions', 'planet')

    @validates('name')
    def validates_name(self, key, new_name):
        if not new_name:
            raise ValueError('Name must be provided.')
        return new_name

    @validates('field_of_study')
    def validates_field_of_study(self, key, new_field_of_study):
        if not new_field_of_study:
            raise ValueError('Field of Study must be provided.')
        return new_field_of_study

    serialize_rules = ('-missions', )

    def __repr__(self):
        return f'<Scientist id={self.id} name={self.name} >'


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    scientist_id = db.Column(db.Integer, db.ForeignKey(
        'scientists.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey(
        'planets.id'), nullable=False)

    scientist = db.relationship('Scientist', back_populates='missions')
    planet = db.relationship('Planet', back_populates='missions')

    serialize_rules = ('-scientist.missions', '-planet.missions', )

    @validates('name')
    def validates_name(self, key, new_name):
        if not new_name:
            raise ValueError('Name must be provided.')
        return new_name

    @validates('scientist_id')
    def validates_name(self, key, new_scientist_id):
        if not new_scientist_id:
            raise ValueError('Scientist must be provided.')
        return new_scientist_id

    @validates('planet_id')
    def validates_name(self, key, new_planet_id):
        if not new_planet_id:
            raise ValueError('Planet must be provided.')
        return new_planet_id

    def __repr__(self):
        return f'<Mission id={self.id} name={self.name} scientist_id={self.scientist_id} planet_id={self.planet_id}>'
