from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from blocklist import BLOCKLIST 

# "_" before variable names are private variables that should not be imported anywhere else in Python.
        
_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",
                        type=str,
                        required=True,
                        help="This field cannot be blank"
)
_user_parser.add_argument("password",
                        type=str,
                        required=True,
                        help="This field cannot be blank"
)


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        
        if UserModel.find_by_username(data["username"]):
            return False, 400

        user = UserModel(**data)
        user.save_to_db()

        return True, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return False, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return False, 404
        user.delete_to_db()
        return True, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        """ 
            This authenticates the user manually
            1. Get the data from parser(request body).
            2. Find the user in the database.
            3. Check the password.
            4. Create an access token.
            5. Craete refresh token (will look at this later).
            6. Return the access token
        """

        # Get the data from parser
        data = _user_parser.parse_args()

        # Find the user in the DB
        user = UserModel.find_by_username(data["username"])

        # Check the password if correct
        # This is what the `authenticate()` function used to do.
        if user and safe_str_cmp(user.password, data["password"]):
            # Create access and refresh token 
            # identity= is what the `identity()` function used to do.
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        # If username not found and/or password is wrong.
        return False, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"] # jti is a "JWT ID", a unique identifier for a JWT.
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200



