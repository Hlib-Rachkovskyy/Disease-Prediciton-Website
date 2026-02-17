from flask import Flask, jsonify, request, make_response, render_template, redirect, url_for, session
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt, check_password_hash

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, \
    get_jwt_identity, unset_jwt_cookies, verify_jwt_in_request

bcrypt = Bcrypt()

from flask_restful import Api, Resource, reqparse

import ai_model
from db_communication import create_user, get_disease_by_id, approve_disease_db, get_user_from_database, \
    db, delete_disease, create_invites, modify_disease_name, find_invites_in_base, \
    create_disease_in_db, get_invites, get_diseases_of_user_not_approved

app = Flask(__name__)
api = Api(app)
app.config.from_object('config.Config')

bcrypt = Bcrypt(app)

jwtManager = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

try:
    ai = ai_model.AI(dataset='Final_Augmented_dataset_Diseases_and_Symptoms.csv')
except:
    print("AI was not initialized")


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


"""Guest"""


class GuestRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Name cannot be blank")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank")
        parser.add_argument('workplace', type=str, required=True, help="Workplace cannot be blank")
        parser.add_argument('invite', type=str, required=True, help="You can't join without invite")

        data = parser.parse_args()

        user = get_user_from_database(username=data['username'])

        if user:
            return make_response(jsonify({'error': 'Name already used'}), 400)
        if find_invites_in_base(data['invite']):
            id_of_created_user = create_user(data['username'], hash_password(data['password']), data['workplace'])
            return make_response(
                jsonify({f"User on id ${id_of_created_user} created successfully": id_of_created_user}), 201)
        else:
            return make_response(jsonify({'Wrong invite data': data['invite']}), 401)


api.add_resource(GuestRegister, '/api/register')


class GuestLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Name cannot be blank")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank")

        data = parser.parse_args()
        user = get_user_from_database(data['username'])
        if user and check_password_hash(user.Password, data['password']):
            access_token = create_access_token(identity=data['username'])
            response = make_response(jsonify({'access_token is saved in cookies:': access_token}), 200)
            response.set_cookie('access_token_cookie', access_token, httponly=True, secure=True)
            return response
        else:
            return make_response(jsonify({'error': f"Invalid username or password {hash_password(data['password'])}"}),
                                 401)


api.add_resource(GuestLogin, '/api/login')


def data_modification(parser):
    parser.add_argument('amount', type=int, required=True, help="amount cannot be blank")
    data = parser.parse_args()

    parser.add_argument('description', type=str, required=False, help="")
    data = parser.parse_args()

    for i in range(data['amount']):
        parser.add_argument(f"{i}", type=str, required=True, help="Symptom cannot be blank")

    data = parser.parse_args()
    data.pop('amount', None)
    data = {v: 1 for k, v in data.items()}
    return data


class DiseasePredict(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        data = ai.model_predict(data_modification(parser))
        return make_response(jsonify({'message': 'Your connection is unlogged', 'data': data}), 200)

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        parser = reqparse.RequestParser()
        data = ai.model_predict(data_modification(parser))

        parser.add_argument('description', type=str, required=False, help="")
        description = parser.parse_args()
        create_disease_in_db(data[0], current_user, description['description'])
        return make_response(jsonify({'message': 'Disease was added to database', 'Current user: ': current_user}), 201)

    @jwt_required()
    def delete(self, disease_id):
        current_user = get_jwt_identity()
        if current_user == 'admin':
            if delete_disease(disease_id) == 1:

                return make_response(jsonify({'Disease on this id was removed': disease_id}), 204)
            else:
                return make_response(jsonify({'Disease on this id wasn\'t found or was deleted already': disease_id}),
                                     404)
        else:
            return make_response(jsonify({'You don\'t have enough right\'s to delete a disease': disease_id}), 403)


api.add_resource(DiseasePredict, '/api/disease/predict', '/api/disease/<int:disease_id>/')


class DiseaseList(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        user = get_user_from_database(user)
        diseases = get_diseases_of_user_not_approved(user)
        if diseases:
            return make_response(jsonify({'List of diseases': [disease.to_dict() for disease in diseases]}), 200)
        else:
            return make_response(jsonify({'user don\'t have any disease added': diseases}), 204)


api.add_resource(DiseaseList, '/api/list')


class Invites(Resource):
    @jwt_required()
    def get(self, amount):
        current_user = get_jwt_identity()
        if current_user == 'admin':
            invites = get_invites(amount)
            if not invites:
                return make_response(jsonify({'error': 'Database don\'t have any invites'}), 404)
            return make_response(jsonify({'Invites': [invite.to_str() for invite in invites]}), 200)
        else:
            return make_response(jsonify({'Not enough right\'s': current_user}), 403)

    @jwt_required()
    def post(self, amount):
        current_user = get_jwt_identity()
        if current_user == 'admin':
            created_invites = create_invites(amount)
            return make_response(jsonify({'Invites: ': created_invites}), 201)
        else:
            return make_response(jsonify({'Not enough right\'s': current_user}), 403)


api.add_resource(Invites, '/api/invites/<int:amount>')


class Specify(Resource):
    @jwt_required()
    def post(self, disease_id, correct_name):

        current_user = get_jwt_identity()

        user = get_user_from_database(current_user)
        disease = get_disease_by_id(disease_id)

        if not disease:
            return make_response(jsonify({'disease wasn\'t found': disease_id}), 404)

        if not approve_disease_db(disease, user):
            return make_response(jsonify({
                'you don\'t have enough rights to approve that disease report or that report was approved by someone else': disease_id}),
                403)

        if correct_name == disease.Name:
            return make_response(jsonify({'disease was approved': disease_id}), 200)

        if modify_disease_name(disease_id, correct_name):
            return make_response(jsonify({'disease name was changed': disease_id}), 200)
        else:
            return make_response(jsonify({'disease wasn\'t deleted': disease_id}), 304)


api.add_resource(Specify, '/api/disease/specify/<int:disease_id>/<string:correct_name>')


#WEB

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_from_database(username)
        print(hash_password(password))
        if user and check_password_hash(user.Password, password):
            access_token = create_access_token(identity=username)
            response = redirect(url_for('home'))
            response.set_cookie('access_token_cookie', access_token, httponly=True, secure=True)
            return response
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    return render_template('login.html')


@app.route('/logout')
@jwt_required()
def logout():
    response = redirect(url_for('home'))
    response.status_code = 204
    unset_jwt_cookies(response)

    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        workplace = request.form['workplace']
        invite = request.form['invite']
        user = get_user_from_database(username)

        if user:
            return make_response(jsonify({'error': 'Name already used'}), 400)
        if find_invites_in_base(invite):
            create_user(username, hash_password(password), workplace)
            return redirect(url_for('login'))
        else:
            return make_response(jsonify({'Wrong invite data': invite}), 401)

    return render_template('register.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    user = None
    try:
        verify_jwt_in_request(optional=True)
        user = get_jwt_identity()
    except NoAuthorizationError:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.json
        result_data = ai.model_predict(data)
        session['result_data'] = result_data
        message = 'Token is valid'
        create_disease_in_db(Name=result_data[0], Username=user, Description=' '.join(result_data))

        return redirect(url_for('predict_result', message=message))

    else:
        if not user:
            return redirect(url_for('login'))
        return render_template('predict.html')


@app.route('/predict_result', methods=['GET'])
def predict_result():
    message = request.args.get('message')
    data = session.get('result_data', {})
    return render_template('predict_result.html', message=message, data=data)


@app.route('/unaproved', methods=['GET'])
@jwt_required()
def list_unapproved():
    current_user = get_jwt_identity()
    user = get_user_from_database(current_user)
    diseases = get_diseases_of_user_not_approved(user)
    return render_template('list_of_unapproved_disease.html', diseases=diseases)


@app.route('/approve/<int:disease_id>', methods=['GET', 'POST'])
@jwt_required()
def approve_disease(disease_id):
    current_user = get_jwt_identity()
    user = get_user_from_database(current_user)
    if not user:
        return redirect(url_for('login'))

    disease = get_disease_by_id(disease_id)
    if not disease:
        return redirect(url_for('list_unapproved'))

    if request.method == 'POST':
        correct_name = request.form['name']
        disease.Name = correct_name
        if approve_disease_db(disease, user):
            return redirect(url_for('list_unapproved'))
        else:
            return "Error approving disease", 405

    return render_template('approve.html', disease=disease)


if __name__ == '__main__':
    app.run(debug=False)
