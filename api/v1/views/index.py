#!/usr/bin/python3
""" create a file index.py """

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def views_jason():
    return jsonify({'status': 'OK'})