def user_obj(user):
    user_obj = {
        "id":             user.external_id,
        "email":          user.email
    }
    return user_obj


def users_obj(users):
    users_objs = []
    for user in users:
        users_objs.append(user_obj(user))
    return users_objs
