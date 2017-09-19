from flask import request, abort, jsonify
from flask.views import MethodView
from jsonschema import Draft4Validator
from jsonschema.exceptions import best_match
import uuid

from keep.api.todo.models import Todo
from keep.api.todo.schema import schema
from keep.api.user.decorators import user_required
from keep.api.todo.templates import todo_obj, todos_obj


class TodoAPI(MethodView):

    decorators = [user_required]

    def __init__(self):
        if (request.method != 'GET' and request.method != 'DELETE') \
                and not request.json:
            abort(400)

    def get(self, todo_id, *args, **kwargs):
        user = kwargs['user']

        if todo_id:
            todo = Todo.find_todo(todo_id, user.external_id)

            if not todo:
                return jsonify({}), 404

            response = {
                'result': 'ok',
                'todo': todo_obj(todo)
            }

            return jsonify(response), 200
        else:
            todos = Todo.find_by_status(user.external_id)

            response = {
                'result': 'ok',
                'todos': todos_obj(todos)
            }

            return jsonify(response), 200

    def post(self, *args, **kwargs):
        user = kwargs['user']

        todo_json = request.json
        error = best_match(Draft4Validator(schema).iter_errors(todo_json))

        if error:
            return jsonify({"error": error.message}), 400
        else:
            params = {
                'text': todo_json.get('text'),
                'external_id': str(uuid.uuid4()),
                'user_id': user.external_id
            }

            todo = Todo(**params).save()

            response = {
                'result': 'ok',
                'todo': todo_obj(todo)
            }

            return jsonify(response)

    def put(self, todo_id, *args, **kwargs):
        user = kwargs['user']

        todo_json = request.json
        error = best_match(Draft4Validator(schema).iter_errors(todo_json))

        if error:
            return jsonify({"error": error.message}), 400

        todo = Todo.find_todo(todo_id, user.external_id)

        if not todo:
            return jsonify({}), 404

        params = {
            'text': todo_json.get('text', todo.text),
            'is_completed': todo_json.get('is_completed', todo.is_completed)
        }

        if params['is_completed']:
            from datetime import datetime
            todo.completed_at = datetime.utcnow()
        else:
            todo.completed_at = None

        todo.text = params['text']
        todo.is_completed = params['is_completed']
        todo.save()

        response = {
            'result': 'ok',
            'todo': todo_obj(todo)
        }

        return jsonify(response), 200

    def delete(self, todo_id, *args, **kwargs):
        user = kwargs['user']

        todo = Todo.find_todo(todo_id, user.external_id)

        if not todo:
            return jsonify({}), 404

        todo.is_live = False
        todo.save()

        return jsonify({}), 204
