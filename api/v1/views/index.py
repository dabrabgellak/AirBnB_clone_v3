#!/usr/bin/python3
'''
index views
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    '''
    Return status code
    '''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    '''
    Return count stats
    '''
    stats_count = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
        }

    return jsonify(**stats_count)
