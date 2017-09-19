def todo_obj(todo):
    todo_obj = {
        "id":             todo.external_id,
        "text":           todo.text,
        "is_completed":   todo.is_completed,
        "completed_at":   todo.completed_at,
        "links": [
            {"rel": "self", "href": "/api/todos/" + todo.external_id}
        ]
    }

    if todo.is_completed:
        todo_obj['completed_at'] = str(
            todo.completed_at.isoformat()[:19]) + "Z"
    else:
        todo_obj.pop('completed_at')
    return todo_obj


def todos_obj(todos):
    todos_objs = []
    for todo in todos:
        todos_objs.append(todo_obj(todo))
    return todos_objs
