from werkzeug.security import safe_str_cmp
from user import User

# userid_mapping = {
#     1: {
#         "id": 1,
#         "username": "bob",
#         "password": "1234"
#     }
# }

def authenticate(username, password):
    user = User.find_by_username(username)
    # if user and user.password == password:
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload["identity"]
    return User.find_by_id(user_id)