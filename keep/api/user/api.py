from flask import request, abort, jsonify
from flask.views import MethodView
from jsonschema import Draft4Validator
from jsonschema.exceptions import best_match
import uuid
# from datetime import datetime, timedelta

from keep.api.user.models import User
from keep.api.user.decorators import user_required
from keep.api.user.schema import register_schema, login_schema
from keep.api.user.templates import user_obj, users_obj


class UserAPI(MethodView):

    def __init__(self):
        if (request.method != 'GET' and request.method != 'DELETE') \
                and not request.json:
            abort(400)

    def get(self):
        token = request.headers.get('X-Auth')

        if token is None:
            return jsonify({}), 401

        user = User.find_by_token(token)

        if not user:
            return jsonify({}), 401

        response = {
            'result': 'ok',
            'user': user_obj(user)
        }

        return jsonify(response), 200

    def post(self):

        if request.path == '/api/users/login':
            user_json = request.json

            error = best_match(Draft4Validator(
                login_schema).iter_errors(user_json))

            if error:
                return jsonify({"error": error.message}), 400
            else:
                params = {
                    'email': user_json.get('email'),
                    'password': user_json.get('password')
                }

                u = User.find_by_email(params['email'])

                if u and u.authenticated(password=params['password']):

                    u = u.generate_auth_token()

                    response = {
                        'result': 'ok',
                        'user': user_obj(u)
                    }

                    headers = {'X-Auth': u.tokens.get('token')}

                    return jsonify(response), 200, headers
                else:
                    response = {
                        'error': 'email or password is incorrect'
                    }
                    return jsonify(response), 400

        if request.path == '/api/users/':
            user_json = request.json

            error = best_match(Draft4Validator(
                register_schema).iter_errors(user_json))

            if error:
                return jsonify({"error": error.message}), 400
            else:
                h_password = User.encrypt_password(user_json.get('password'))

                params = {
                    'email': user_json.get('email'),
                    'password': h_password,
                    'external_id': str(uuid.uuid4())
                }

                if User.objects.filter(email=params['email']).first():
                    return jsonify({'error': "Email is already in use"})

                user = User(**params).save()

                user.generate_auth_token()

                response = {
                    'result': 'ok',
                    'user': user_obj(user)
                }

                headers = {'X-Auth': user.tokens.get('token')}

                return jsonify(response), 201, headers

    def delete(self):

        token = request.headers.get('X-Auth')

        if token is None:
            return jsonify({}), 401

        user = User.find_by_token(token)

        if not user:
            return jsonify({}), 401

        u = user.remove_auth_token(token)

        return jsonify({'user': user_obj(u)})
