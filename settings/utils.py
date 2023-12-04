def get_serializer(todo):
    try:
        return {
            "id": todo.id,
            "title": todo.title,
            "is_complete": todo.is_complete,
        }
    except AttributeError:
        pass


def get_serializers(todos):
    return [get_serializer(todo) for todo in todos]
