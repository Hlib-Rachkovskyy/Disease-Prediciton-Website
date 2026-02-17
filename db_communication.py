import string

from flask_sqlalchemy import SQLAlchemy
import secrets

db = SQLAlchemy()

"""Invites"""


def get_invites(amount):
    invites = InvitesToSystem.query.limit(amount).all()
    if len(invites) == 0:
        return None
    return invites


def create_invites(num):
    invites = [generate_token() for _ in range(num)]
    return invites


def find_invites_in_base(invite):
    invite_record = InvitesToSystem.query.filter_by(Invite=invite).first()
    if invite_record:
        db.session.delete(invite_record)
        db.session.commit()
        return True
    return False


# noinspection PyGlobalUndefined
def generate_token():
    invite_not_in_db = True
    global token
    while invite_not_in_db:
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))

        if InvitesToSystem.query.filter_by(Invite=token).count() == 0:
            db.session.add(InvitesToSystem(Invite=token))
            db.session.commit()
            invite_not_in_db = False

    return token


"""Disease"""


def get_diseases_of_user_not_approved(user):
    diseases = Disease.query.filter_by(User_Id=user.Id).all()
    diseases = [disease for disease in diseases if disease not in user.diseases]
    if not diseases:
        return []
    return diseases


def modify_disease_name(disease_id, name):
    disease = Disease.query.get(disease_id)
    if disease:
        disease.Name = name
        db.session.commit()
        return True
    return False


def delete_disease(disease_id):
    num_of_rows = Disease.query.filter_by(Id=disease_id).delete()
    db.session.commit()
    return num_of_rows


def get_disease_by_id(disease_id):
    return Disease.query.get(disease_id)


def create_disease_in_db(Name, Username, Description):
    new_disease = Disease(Name=Name, Description=Description, User_Id=get_user_from_database(Username).Id)
    db.session.add(new_disease)
    db.session.commit()
    return new_disease.Name


"""User"""


def get_user_from_database(username):
    return User.query.filter_by(Username=username).first()


def get_user_added_diseases(username):
    user = get_user_from_database(username)
    disease_list = Disease.query.filter_by(User_Id=user.Id).all()
    if user:
        return disease_list
    return None


def create_user(name, password, workplace):
    new_user = User(Username=name, Password=password, Workplace=workplace)
    db.session.add(new_user)
    db.session.commit()
    return new_user.Id


"""Approved by"""


def approve_disease_db(disease, user):
    existing_approval = db.session.query(approved_by).filter_by(user_id=user.Id, disease_id=disease.Id).first()
    if existing_approval:
        return False
    original_user = User.query.get(disease.User_Id)
    if user.Id == disease.User_Id or user.Workplace == original_user.Workplace:
        user.diseases.append(disease)
        db.session.commit()
        return True
    return False


"""Migrations"""

approved_by = db.Table('approved_by',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.Id'), primary_key=True),
                       db.Column('disease_id', db.Integer, db.ForeignKey('disease.Id'), primary_key=True),
                       )


class Disease(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(500), nullable=False)
    ListOfSymptoms = db.Column(db.String(377), nullable=True)
    User_Id = db.Column(db.Integer, db.ForeignKey('user.Id'), nullable=False)

    def to_dict(self):
        return {
            'Id': self.Id,
            'Name': self.Name,
            'Description': self.Description,
            'ListOfSymptoms': self.ListOfSymptoms,
            'User_Id': self.User_Id
        }


class User(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String, nullable=False)
    Workplace = db.Column(db.String(200), nullable=False)
    diseases = db.relationship('Disease', secondary=approved_by, lazy='subquery',
                               backref=db.backref('users', lazy=True))


class InvitesToSystem(db.Model):
    Invite = db.Column(db.String(16), primary_key=True)

    def to_str(self):
        return {
            'Invite': self.Invite,
        }


class GuestRequest(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(500), nullable=False)
