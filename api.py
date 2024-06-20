from flask import Flask, jsonify, request, session
from flask_bcrypt import bcrypt
from flask_jwt_extended import JWTManager
from ServiceLogic import check_invite
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from dbCommunication import hash_password, create_user, get_disease_by_id, aprove_diseas_db

from dbCommunication import get_user_from_database

# to do: async, database, keys, codes, check tokens, ending with doing endpoints, data thing, gui optionally, make it more workable with data from data sets maybe change database a little bit

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({'error': 'Name and password are required'}), 400

    user = get_user_from_database(username)
    if user:
        return jsonify({'error': 'Name already used'}), 400  #change code

    if check_invite(data['invite']):

        id = create_user(username, password)

        return jsonify({f'User on id ${id} created successfully': id}), 201
    else:
        return jsonify({'Wrong invite data': data['invite']}), 201  #Code change


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = get_user_from_database(username)

    if user and user.password == hash_password(password):
        serializer = Serializer(app.secret_key, expires_in=(3600))  # maybe change it to jwt tokens
        token = serializer.dumps({'user_login_id': user.id}).decode('utf-8')

        return jsonify({'access_token': token}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/approve/disease/<string:token>/<int:id>',
           methods=['POST'])  # make it yes or no by addin other variable in path
def aprove_new_diseas(token, id):
    global user_id
    try:
        serializer = Serializer(app.secret_key)

        data = serializer.loads(token, max_age=3600)  # check if it's working
        user_id = data['user_id']
        print(f"Token is valid for user ID: {user_id}")
    except SignatureExpired:
        print("Token is expired")
    except BadSignature:
        print("Token is invalid")

    diseas = get_disease_by_id(id)
    if diseas:
        if aprove_diseas_db(diseas.id, user_id):
            return jsonify({'disease was aproved': diseas}), 201
        else:
            return jsonify({'you don\'t have enough rights to aprove that disease report'}), 201  #change code
    else:
        return jsonify({'disease wasn\'t found': id}), 200  #change code


@app.route('/disease/predict', methods=['GET'])
def get_diseas():
    data = request.get_json()

    return jsonify({'disease': data['disease']}), 201


@app.route('/disease/<string:token>', methods=['POST'])
def add_new_diseas(token):
    data = request.get_json()
    return jsonify({'disease': data['disease']}), 201


@app.route('/invite/<string:token>/<int:amount>', methods=['POST'])
def add_new_invite(token, amount):
    data = request.get_json()
    return jsonify({'disease': data['disease']}), 201


# On the terminal type: curl http://127.0.0.1:5000/


if __name__ == '__main__':
    app.run(debug=True)
