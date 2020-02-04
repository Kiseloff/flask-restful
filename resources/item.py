import json
from flask import request
from flask_restful import Resource, reqparse


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )

    def __init__(self, **kwargs):
        self.items = kwargs['items']

    # @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        item = next(filter(lambda x: x['name'] == name, self.items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, self.items), None):
            return {'message': f'An item with name <{name}> already exists'}, 400

        data = request.get_json()
        item = {
            'name': name,
            'price': data['price']
        }
        self.items.append(item)

        return item, 201

    def delete(self, name):
        if next(filter(lambda x: x['name'] == name, self.items), None):
            for item in self.items:
                if item['name'] == name:
                    self.items.remove(item)
            return {'message': f' Item with name <{name}> was deleted'}
        else:
            return {'message': f'There is no item with name <{name}>'}, 404

    def put(self, name):
        # Handle request with parser
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, self.items), None)
        if item:
            item.update(data)
        else:
            item = {
                'name': name,
                'price': data['price']
            }
            self.items.append(item)
        return item
