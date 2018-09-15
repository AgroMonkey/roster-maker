from rostermaker import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    shifts = db.relationship('Shift', backref='shift_user', lazy=True)

    def __init__(self, username, email, password, real_name, role):
        self.username = username
        self.email = email
        self.password = password
        self.real_name = real_name
        self.role = role

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.real_name}')"


class Shift(db.Model):
    shift_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable = False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sbreak = db.Column(db.String(5), default=None)

    def __init__(self, date, start_time, end_time, location, user_id, sbreak=None):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.sbreak = sbreak
        self.location = location
        self.user_id = user_id

    def __repr__(self):
        return f"Shift('{self.shift_id}', '{self.date}', '{self.location}')"

