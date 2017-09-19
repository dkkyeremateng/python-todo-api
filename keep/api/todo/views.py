from flask import Blueprint

from keep.api.todo.api import TodoAPI

todo = Blueprint('todo', __name__, url_prefix='/api')

todo_view = TodoAPI.as_view('todo_api')

todo.add_url_rule('/todos/', defaults={'todo_id': None},
                  view_func=todo_view, methods=['GET', ])

todo.add_url_rule('/todos/',
                  view_func=todo_view, methods=['POST', ])

todo.add_url_rule('/todos/<todo_id>',
                  view_func=todo_view, methods=['GET', 'PUT', 'DELETE'])
