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
