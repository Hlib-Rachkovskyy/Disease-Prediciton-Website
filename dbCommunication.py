from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt

db = SQLAlchemy()


def get_from_db_data_to_train():
    pass


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  #idk


def aprove_diseas_db(disease_id, user_id):
    disease_user_id = Disease.query.filter_by(diseas_id=disease_id).first().User_Id
    if user_id == disease_user_id:
        new_aproved_by = ApprovedBy(User_Id=user_id, Disease_Id=disease_id)
        db.session.add(new_aproved_by)
        db.session.commit()
        return True
    return False


def get_user_from_database(username):
    return User.query.filter_by(Username=username).first()


def create_user(name, password):
    new_user = User(username=name, password=hash_password(password))
    db.session.add(new_user)
    db.session.commit()
    return new_user.Id


def find_invites_in_base(invite):
    invite_record = InvitesToSystem.query.filter_by(Invite=invite).first()
    if invite_record:
        db.session.delete(invite_record)
        db.session.commit()
        return True
    return False


def get_disease_by_id(id):
    disease = Disease.query.filter_by(Id=id).first()
    if disease:
        return DiseaseDTO(disease.Id, disease.Description, disease.ListOfDisease)
    return None


class DiseaseDTO:
    def __init__(self, id, description, list_of_disease):
        self.id = id
        self.description = description
        self.list_of_disease = list_of_disease


class Disease(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String, nullable=False)
    ListOfDisease = db.Column(db.String, nullable=False)
    User_Id = db.Column(db.Integer, db.ForeignKey('User.Id'), nullable=False)


class User(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)


class ApprovedBy(db.Model):
    User_Id = db.Column(db.Integer, db.ForeignKey('User.Id'), primary_key=True, nullable=False)
    Disease_Id = db.Column(db.Integer, db.ForeignKey('Disease.Id'), primary_key=True, nullable=False)


class InvitesToSystem(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Invite = db.Column(db.String, nullable=False)
