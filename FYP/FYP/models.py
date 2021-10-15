from flask_login import LoginManager, login_manager, UserMixin, login_user, current_user
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import getpass
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, column_property
from FYP import db, login_manager, app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    title = db.Column(db.String(10))
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    password = db.Column(db.String(60))
    organization = db.Column(db.String(60))
    patientRecord = db.relationship('Patient', backref='user', lazy='select')
    videoRecord = db.relationship('VideoFiles', backref='user', lazy='select')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps ({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.email}', '{self.title}', '{self.firstname}', '{self.lastname}', '{self.organization}')"

class Patient(db.Model):
    __tablename__="patient"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    gender = db.Column(db.String(6))
    country = db.Column(db.String(60))
    age = db.Column(db.Integer)
    
    therapyid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patientvideos = db.relationship('VideoFiles', backref='patient', lazy='select')

    guardiantitle = db.Column(db.String(5))
    guardianfirstname = db.Column(db.String(120))
    guardianlastname = db.Column(db.String(120))
    relationship = db.Column(db.String(20))
    email = db.Column(db.String(120))

    def __repr__(self):
        return f"Patient('{self.id}')"

class VideoFiles(db.Model):
    __tablename__="VideoFiles"
    videoID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    videoName = db.Column(db.String(300), nullable = False)
    videoData = db.Column(db.LargeBinary, nullable = False)
    uploaderid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patientid = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    videoEmotion = db.Column(db.PickleType, nullable = True)
    videoDate = db.Column(db.String(100), nullable = True)

    def __repr__(self):
        return f"VideoFiles('{self.videoName}')"

class Variables:
    username = getpass.getuser()
    date = datetime.now()

