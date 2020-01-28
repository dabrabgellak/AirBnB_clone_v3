#!/usr/bin/python3
'''
index views
'''
from api.v1.views import app_views
from flask import jsonify


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
        "amenities": 47,
        "cities": 36,
        "places": 154,
        "reviews": 718,
        "states": 27,
        "users": 31
    }

    return jsonify(**stats_count)
