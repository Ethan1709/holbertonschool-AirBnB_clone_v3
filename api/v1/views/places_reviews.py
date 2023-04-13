#!/usr/bin/python3
""" all cities """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import base_model
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Retrieve the list of all Places of a City """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = []
    for i in place.places_reviews:
        reviews_list.append(i.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ If the review_id is not linked to any Review object,
    raise a 404 error """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ Delete a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ create a review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    inf = request.get_json()
    if inf is None:
        abort(400, 'Not a JSON')
    if inf.get('user_id') is None:
        abort(400, 'Missing user_id')
    user_id = inf['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if inf.get('text') is None:
        abort(400, 'Missing text')
    inf['place_id'] = place_id
    review = Review(**inf)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ update a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    inf = request.get_json()
    if inf is None:
        abort(400, 'Not a JSON')
    for key, value in inf.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
