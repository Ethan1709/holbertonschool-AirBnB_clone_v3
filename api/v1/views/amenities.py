#!/usr/bin/python3
""" all amenities """

import sys
from flask import Flask, jsonify, request, make_response
from models import storage
from api.v1.views import app_views
from flask import abort
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
sys.path.append("/home/Ethan1709/holbertonschool-AirBnB_clone_v3")
sys.path.append("/home/Ethan1709/holbertonschool-AirBnB_clone_v3")


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """ Retrieve the list of all Amenities """
    all_amenities = storage.all(Amenity).values()
    amenities = []
    for amenity in all_amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete a amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ create a new amenity object """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    req_data = request.get_json()
    # ** permet de faire passer args
    instance = Amenity(**req_data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Amenity update """
    if not request.get_json():
        abort(400, description="Not a JSON")

    arg_list = ['id', 'created_at', 'updated_at']

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    req_data = request.get_json()
    for key, value in req_data.items():
        if key not in arg_list:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
