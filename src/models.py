# Define database tables as Python classes

from extensions import db  # import database object
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Device table to store device info
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-generated device ID

    # Required fields
    publisher = db.Column(db.String(200), nullable=False)
    book_name = db.Column(db.String(200), nullable=False)
    book_type = db.Column(db.String(200), nullable=False)
    # Location data
    location = db.Column(db.String(200), nullable=True)
    location_in_library = db.Column(db.String(200), nullable=True)
    # date
    date_added = db.Column(db.Date, default=datetime.utcnow)  # Date device was added
    # Check-in/out tracking
    last_checked_out = db.Column(db.DateTime, nullable=True)
    last_checked_in = db.Column(db.DateTime, nullable=True)
    checked_out_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    checked_out_user = db.relationship('User', backref='checked_out_books', foreign_keys=[checked_out_by])
    status = db.Column(db.String(20), nullable=False, default='Available')  # <-- Add this line

    def __repr__(self):
        return f'<Book {self.book_name} ({self.id})>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique user ID
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)  # first name
    last_name = db.Column(db.String(50), nullable=False)   # last name
    role = db.Column(db.String(20), nullable=False)        # user role (admin, lab manager, viewer)
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=False)          # account activation status

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Properly override Flask-Login's is_active property
    @property
    def is_active(self):
        return self.active

    @is_active.setter
    def is_active(self, value):
        self.active = value

    def __repr__(self):
        return f'<User {self.username} ({self.get_full_name()})>'
