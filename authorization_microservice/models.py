from run import db
from passlib.hash import pbkdf2_sha256 as sha256


# This class will create the database table and specify the attributed of the table.
class UserModel(db.Model):
    __tablename__ = 'usertable'

    id = db.Column(db.Integer, primary_key = True)
    email= db.Column(db.String(120), unique = True, nullable = False)
    name = db.Column(db.String(120), nullable = False)
    password = db.Column(db.String(120), nullable = False)

    # This will save the information to the database.
    def save_info(self):
        db.session.add(self)
        db.session.commit()

    # This method will search the user by email and will return the email if found.
    @classmethod
    def search_email(cls,email):
        return cls.query.filter_by(email = email).first()

    # This method will genetate the hash code for the correspoding password.
    @staticmethod
    def encrypt_password(password):
        return sha256.hash(password)

    # This method checks if the given password and hashcode matches.
    @staticmethod
    def check_password(password, hash):
        return sha256.verify(password, hash)


    # based on the reference flask architecture given on https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
