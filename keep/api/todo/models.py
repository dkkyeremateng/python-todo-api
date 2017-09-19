from keep.extensions import db
from bson.objectid import ObjectId


class Todo(db.Document):
    """
    This is the todo model
    """
    external_id = db.StringField()
    text = db.StringField(required=True, min_length=1)
    is_completed = db.BooleanField(default=False)
    completed_at = db.DateTimeField(default=None)
    is_live = db.BooleanField(default=True)
    user_id = db.StringField(required=True)

    @classmethod
    def find_by_status(cls, user_id, status=False):
        return cls.objects.filter(is_completed=status,
                                  is_live=True,
                                  user_id=user_id)

    @classmethod
    def find_todo(cls, todo_id, user_id):
        return cls.objects.filter(external_id=todo_id,
                                  is_live=True,
                                  user_id=user_id).first()
