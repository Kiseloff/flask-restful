from flask import request
from flask_restful import Resource, reqparse


class ItemList(Resource):
    def __init__(self, **kwargs):
        self.items = kwargs['items']

    def get(self):
        return {'items': self.items}
