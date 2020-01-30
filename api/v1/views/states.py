#!/usr/bin/python3
'''
state views
'''
from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.state import State


def all(cls):
    '''
    Return all states
    '''
    states = storage.all(cls)
    return states


def get_state(id):
    '''
    Args:
        id (string):
    Returns:
        state object or None if id not found
    '''
    states = all(State)
    for state in states.values():
        if state.to_dict()['id'] == id:
            return state
    return None


def create(data):
    '''
    create
    Args:
        data (dict):
    Returns:
        dict of object created
    '''
    obj = State(**data)
    obj.save()
    return get_state(obj.id)


def delete(state):
    """
    Delete state.
    Args:
        state (object):
    """
    storage.delete(state)
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
    state = get_state(id)
    if state is None:
        return None
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return state


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


@app_views.route('/states', strict_slashes=False,   methods=('GET', 'POST'))
def states():
    '''
    GET: Return all states
    POST: Create states
    '''
    if request.method == 'GET':
        result = all(State)
        states = [state.to_dict() for state in result.values()]
        return make_response(jsonify(states), 200)
    if request.method == 'POST':

        data = request.get_json()
        if not data:
            return error_handler(400, 'Not a JSON')

        if data.get('name', None) is None:
            return error_handler(400, 'Missing name')
        result = create(data)
        return make_response(jsonify(result), 201)


@app_views.route('/states/<id>', strict_slashes=False,
                 methods=('GET', 'DELETE', 'PUT'))
def states_id(id):
    '''
    GET: return dict state by id
    DELETE: delete state by id
    '''
    if request.method == 'GET':
        state = get_state(id)
        if state is None:
            return error_handler(404, 'Not found')
        state = state.to_dict()
        return make_response(jsonify(state), 200)

    if request.method == 'DELETE':
        state = get_state(id)
        if state is None:
            return error_handler(404, 'Not found')
        delete(state)
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return error_handler(400, 'Not a JSON')
        state_updated = update(id, data)
        state_updated = state_updated.to_dict()
        return make_response(jsonify(state_updated), 200)
