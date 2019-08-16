from datetime import datetime
from flask_login import UserMixin
from linkshorten import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    links = db.relationship('Link', backref='author', lazy=True)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1000), nullable=False)  
    isspecial = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return ('{self.id}', '{self.link}','{self.isspecial}', '{self.user_id}')



"""




CREATE TABLE link (id INTEGER PRIMARY KEY NOT NULL,
link VARCHAR(1000) NOT NULL,
isspecial INTEGER NOT NULL, 
sha256 VARCHAR(100) NOT NULL,
user_id INTEGER NOT NULL,
FOREIGN KEY(user_id) REFERENCES user (id));

INSERT OR IGNORE INTO link (id, link, isspecial, sha256, user_id) VALUES (123213, 'asdasdasdasdASD===', 1, 'asdadsdasasddasdasadsdas', 3);


"""