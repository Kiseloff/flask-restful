import json
from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'my_store',
        'items': [
            {
                'name': 'item1',
                'price': 16.99
            },
            {
                'name': 'item2',
                'price': 0.99
            },
        ]
    }
]


def pp(_json):
    print(json.dumps(_json, indent=4, sort_keys=True))


@app.route('/')
def home():
    return jsonify(
        hello=1,
        foo=2
    )


# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    pp({'stores': stores})
    return jsonify(new_store)


# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'Error': 'there is not such a store'}), 404


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            store['items'].append(request_data)
            return jsonify(store)
    return jsonify({'Error': 'there is not such a store'}), 404


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'Error': 'there is not such a store'}), 404

if __name__ == '__main__':
    # TODO: turn off DEBUG mode
    app.run(port=5001, debug=True)
