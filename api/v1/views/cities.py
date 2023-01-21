#!/usr/bin/python3
'''Contains the states view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False)
def get_city_for_state(state_id):
    """Returns JSON cities in a given state"""
    state = storage.get('State', state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return (jsonify(cities), 200)
    raise NotFound()


@app_views.route(
    '/cities/<city_id>',
    methods=['GET'],
    strict_slashes=False)
def get_city(city_id=None):
    '''' Gets the city with the given id or 
    all cities in the state with the given id. '''
    if city_id:
        city = storage.get(City, city_id)
        if city:
            return (jsonify(city.to_dict()), 200)
        raise NotFound()
    raise NotFound()


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_city(city_id):
    '''delete a city with the given id.'''
    city = storage.get(State, city_id)
    if city:
        city.delete()
        storage.save()
        return (jsonify({}), 200)
    raise NotFound()


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False)
def post_city(state_id):
    '''creat a new city in a state.'''
    state = storage.get('State', state_id)
    if not state:
        raise NotFound()
    req = request.get_json()
    if type(req) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in req:
        raise BadRequest(description='Missing name')
    req['state_id'] = state.id
    city = City(**req)
    city.save()
    return (jsonify(city.to_dict()), 201)


@app_views.route(
    '/cities/<city_id>',
    methods=['PUT'],
    strict_slashes=False)
def update_city(city_id=None):
    '''Updates the city with an id.'''
    ignore = ('id', 'state_id', 'created_at', 'updated_at')
    if city_id:
        city = storage.get(City, city_id)
        if city:
            req = request.get_json()
            if type(req) is not dict:
                raise BadRequest(description='Not a JSON')
            for key, value in req.items():
                if key not in ignore:
                    setattr(city, key, value)
            city.save()
            return (jsonify(city.to_dict()), 200)
        raise NotFound()
    raise NotFound()
