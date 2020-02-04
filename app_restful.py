from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from app import pp

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )

    # @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f'An item with name {name} already exists'}, 400

        data = request.get_json()
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        if next(filter(lambda x: x['name'] == name, items), None):
            items = list(filter(lambda x: x['name'] != name, items))
            return {'message': f' Item with name {name} deleted'}
        else:
            return {'message': f'There is no item with name {name}'}, 404

    def put(self, name):

        data = Item.parser.parse_args()

        # data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {
                'name': name,
                'price': data['price']
            }
            items.append(item)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


# http://127.0.0.1/item/Fork
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
