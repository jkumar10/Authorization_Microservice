from main import db

class UserModel(db.Model):
    __tablename__ = 'usertable'

    id = db.Column(db.Integer, primary_key = True)
    email=db.Column(db.String(120), unique = True, nullable = False)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)

    def save_info(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def search_username(cls, username):
        return cls.query.filter_by(username = username).first()

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)
