#!/usr/bin/python3
'''
city views
'''
from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views.states import get_state


def all(cls):
    '''
    Return all cities
    '''
    cities = storage.all(cls)
    return cities


def get_cities_by(state_id):
    '''
    Args:
        state_id (string):
    Returns:
        city object or None if id not found
    '''
    cities = all(City)
    list_cities = [city.to_dict() for city in cities.values()
                   if city.state_id == state_id]
    return list_cities


def get_city(city_id):
    '''
    Args:
        id (string):
    Returns:
        city object or None if id not found
    '''
    cities = all(City)
    for city in cities.values():
        if city.id == city_id:
            return city
    return None


def create(data, state_id):
    '''
    create
    Args:
        data (dict):
        state_id (string):
    Returns:
        dict of object created
    '''
    obj = City(**data)
    obj.state_id = state_id
    obj.save()
    return get_city(obj.id)


def delete(city):
    """
    Delete city.
    Args:
        city (object):
    """
    storage.delete(city)
    storage.save()


def update(id, data):
    """
        update.
    Args:
        id (string):
        data (dict)
    Returns:
        object update or None if id not found
    """
    city = get_city(id)
    if city is None:
        return None
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return city


def error_handler(error, message):
    """
    Gives error message when any invalid url are requested.
    Args:
        error (string):
        message (string):
    Returns:
        Error message.
    """

    return make_response(jsonify({'error': message}), error)


@app_views.route('/states/<state_id>/cities/', strict_slashes=False,
                 methods=('GET', 'POST'))
def cities_id_state(state_id):
    '''
    GET: return dict cities by state_id
    POST: create cities
    '''
    if request.method == 'GET':
        if get_state(state_id) is None:
            return error_handler(404, 'Not found')

        list_cities = get_cities_by(state_id)
        if not list_cities:
            return error_handler(404, 'Not found')
        return make_response(jsonify(list_cities), 200)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return error_handler(400, 'Not a JSON')
        if get_state(state_id) is None:
            return error_handler(404, 'Not found')
        if data.get('name', None) is None:
            return error_handler(400, 'Missing name')
        city_created = create(data, state_id)
        city_created = city_created.to_dict()
        return make_response(jsonify(city_created), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=('GET', 'DELETE', 'PUT'))
def cities(city_id):
    '''
    GET: return dict cities by id
    DELETE: delete cities
    PUT: update cities
    '''
    if request.method == 'GET':
        city = get_city(city_id)
        if city is None:
            return error_handler(404, 'Not found')
        city = city.to_dict()
        return make_response(jsonify(city), 200)

    if request.method == 'DELETE':
        city = get_city(city_id)
        if city is None:
            return error_handler(404, 'Not found')
        delete(city)
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return error_handler(400, 'Not a JSON')
        city_updated = update(city_id, data)
        if city_updated is None:
            return error_handler(404, 'Not found')
        city_updated = city_updated.to_dict()
        return make_response(jsonify(city_updated), 200)
