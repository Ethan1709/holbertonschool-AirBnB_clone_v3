#!/usr/bin/python3
""" all cities """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models import storage
from models import base_model
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieve the list of all Places of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    for i in city.places:
        places_list.append(i.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ If the place_id is not linked to any Place object,
    raise a 404 error """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ Delete a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id, user_id):
    """ create a place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    inf = request.get_json()
    if inf is None:
        abort(400, 'Not a JSON')
    if inf.get('user_id') is None:
        abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if inf.get('name') is None:
        abort(400, 'Missing name')   
    inf['city_id'] = city_id
    place = Place(**inf)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ update a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    inf = request.get_json()
    if inf is None:
        abort(400, 'Not a JSON')
    for key, value in inf.items():
        if key not in ['id', 'user_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
