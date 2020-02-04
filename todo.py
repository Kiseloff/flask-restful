from flask import Flask, request
from flask_restful import Api, Resource
import logging, time

app = Flask(__name__)
api = Api(app)

todos = {}


class HelloWorld(Resource):
    def get(self):
        return {
            'hello': 'world'
        }


class TodoSimple(Resource):
    # def get(self, todo_id):
    #     logging.info(f' -- {todos}')
    #     return {
    #         'todo' + todo_id: todos[todo_id]
    #     } if todo_id in todos.keys() else 'There is no such a task!'

    def get(self, todo_id):
        time.sleep(5)
        return '', 201

    def post(self, todo_id):
        todos[todo_id] = request.json['task']
        logging.info(f' -- {todos}')
        return {
            f'todo{todo_id}': todos[todo_id]
        }


# api.add_resource(HelloWorld, '/', '/hello')
api.add_resource(TodoSimple, '/todo<string:todo_id>')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # TODO: don't forget to drop DEBUG flag
    app.run(port=5001, debug=True)
