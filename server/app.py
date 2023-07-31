#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os
import ipdb

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''


@app.route('/scientists', methods=['GET', 'POST'])
def scientists():
    if request.method == 'GET':
        all_scientists = Scientist.query.all()
        scientist_list = [scientist.to_dict() for scientist in all_scientists]
        response = make_response(scientist_list, 200)
        return response
    elif request.method == 'POST':
        data = request.get_json()
        try:
            scientist = Scientist(
                name=data['name'],
                field_of_study=data['field_of_study']
            )
            db.session.add(scientist)
            db.session.commit()
            response = make_response(scientist.to_dict(), 201)
            return response
        except Exception as e:
            response_dict = {
                "errors": [e.__str__()]
            }
            response = make_response(response_dict, 422)
            return response


@app.route('/scientists/<int:id>')
def scientist_by_id(id):
    scientist = Scientist.query.filter_by(id=id).first()
    if scientist:
        response = make_response(scientist.to_dict(
            rules=('missions', '-missions.scientist', )), 200)
        return response
    else:
        response = make_response({"error": "Scientist not found"}, 404)
        return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
