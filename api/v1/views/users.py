#!/usr/bin/python3
""" all users """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage
from models import base_model


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieve the list of all Users """
    users = storage.all(User).values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ If the state_id is not linked to any State object,
    raise a 404 error """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """ Delete a state """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ create a state """
    inf = request.get_json()
    if inf is None:
        abort(400, 'Not a JSON')
    if inf.get('email') is None:
        abort(400, 'Missing email')
    if inf.get('password') is None:
        abort(400, 'Missing password')

    user = User(**inf)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    inf = request.get_json()
    if inf is None:
        abort(400, 'Not a JSON')
    for key, value in inf.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
