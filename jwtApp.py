# import library
from multiprocessing.dummy import current_process
from flask import Flask, make_response
from flask import jsonify
from flask import request


from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# menuju url static
app = Flask(__name__, static_url_path='/static')

#membuat account
account = {
    "username": "test",
    "password": "test"
}

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "myjwtsecretkey"      # mengatur secret key
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]  #tempat program akan mengakses jwt
jwt = JWTManager(app)


# membuat route menuju login dengan method post
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    # pengecekan password
    if username != account["username"] or password != account["password"]:
        return jsonify({"message": "Bad username or password"}), 401

    # if username and password is right
    access_token = create_access_token(identity=account)         # men generate access token
    response = make_response(jsonify(access_token=access_token), 200)  # membuat response dengan isi token
    response.set_cookie('access_token_cookie', access_token)   # mengirimkan cookie ke client dengan isi token
    return response
    

# JWT Protected route
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/", methods=["GET"])
def mainPage():
    return 200


if __name__ == "__main__":
    app.run(port=5000)