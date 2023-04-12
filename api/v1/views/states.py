#!/usr/bin/python3
""" all states """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage
from models import base_model


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieve the list of all State """
    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ If the state_id is not linked to any State object,
    raise a 404 error """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ Delete a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ create a state """
    inf = request.get_json()
    if inf is None:
        abort(400, 'Not a JSON')
    if inf.get('name') is None:
        abort(400, 'Missing name')

    state = State(**inf)
    storage.new(state)
    storage.save()
    return jsonify({}), 201