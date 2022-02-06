from app.models import db

class WordModel(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), unique=True, nullable=False)
    translation = db.Column(db.String(120), nullable=True)
    assoc = db.Column(db.String(120), nullable=True)
    connection = db.Column(db.String(120), nullable=True)
    examples = db.Column(db.String(200), nullable=True)
    link = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
