#!/usr/bin/python3
""" all states """

from flask import jsonify, abort
from api.v1.views import app_views
from models.state import State
from models import storage
from models import base_model


@app_views('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieve the list of all State """
    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ If the state_id is not linked to any State object, raise a 404 error """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())
