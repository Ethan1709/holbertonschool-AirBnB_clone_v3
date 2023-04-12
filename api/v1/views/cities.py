#!/usr/bin/python3
""" all cities """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import City
from models import storage
from models import base_model


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieve the list of all State """
    cities = storage.all(City).values()
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_state(city_id):
    """ If the state_id is not linked to any State object,
    raise a 404 error """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """ Delete a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city():
    """ create a city """
    inf = request.get_json()
    if inf is None:
        abort(400, 'Not a JSON')
    if inf.get('name') is None:
        abort(400, 'Missing name')

    city = City(**inf)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    inf = request.get_json()
    if inf is None:
        abort(400, 'Not a JSON')
    for key, value in inf.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
