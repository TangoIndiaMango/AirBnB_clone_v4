#!/usr/bin/python3
'''Contains the blueprint for the API.'''
from api.v1.views.index import *
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
'''A blueprint for AirBnB clone API Version'''
