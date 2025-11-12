
# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from datetime import datetime
from extensions import db
from models import Book, User
from forms import LoginForm, BookForm, RegistrationForm
from sqlalchemy import or_
from werkzeug.security import generate_password_hash
import constants as cn
# print(cn.APPLICATION_ROOT, cn.STATIC, cn.SQLALCHEMY_DATABASE_URI, cn.hostname)

def create_app():
    app = Flask(__name__, static_folder=cn.STATIC)
    app.config['SECRET_KEY'] = 'dev'
    app.config['DEBUG'] = True
    # app.config['APPLICATION_ROOT'] = cn.APPLICATION_ROOT
    app.config['SQLALCHEMY_DATABASE_URI'] = cn.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # --- Root URL ---
    @app.route('/')
    def index():
        return redirect(url_for('login'))

    # --- Authentication Routes ---

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            found_user = User.query.filter_by(username=form.username.data).first()
            if found_user and found_user.check_password(form.password.data):
                if found_user.is_active:
                    # login_user(found_user)
                    # ✅ Redirect based on role
                    if found_user.role in ['Viewer', 'Team Member', 'Admin']:
                        return redirect(url_for('inventory'))
                        # flash('User found pls. wait.')
                    else:
                        flash('Unknown user role. Please contact admin.', 'danger')
                        return redirect(url_for('login'))
                else:
                    flash('Your account is not active yet. Please wait for admin approval.', 'warning')
            else:
                flash('Invalid username or password', 'danger')
        return render_template('login.html', form=form)


    # --- Inventory Page ---
    @app.route('/inventory')
    def inventory():
        search = request.args.get('search', '').strip()
        status_filter = request.args.get('status', '').strip()
        sort = request.args.get('sort', 'book_name')
        query = Book.query

        if search:
            query = query.filter(
                db.or_(
                    Book.book_name.ilike(f'%{search}%'),
                    Book.publisher.ilike(f'%{search}%'),
                )
            )

        if status_filter:
            query = query.filter(Book.status == status_filter)

        if sort == 'publisher':
            query = query.order_by(Book.publisher)
        elif sort == 'book_type':
            query = query.order_by(Book.book_type)
        else:
            query = query.order_by(Book.book_name)
        books = query.all()
        print(books)
        return render_template('inventory.html' , books=books, search=search,
                               status_filter=status_filter, sort=sort)

    @app.route('/book/<int:book_id>', methods=['GET', 'POST'])
    def book_detail(book_id):
        book = Book.query.get_or_404(book_id)
        return render_template('book_detail.html',book=book)


    # # --- Add Device ---
    @app.route('/book/add', methods=['GET', 'POST'])
    def add_book():
        form = BookForm()

        if form.validate_on_submit() and form.submit_add.data:
            # Create new Device from form data
            new_book = Book(
                book_name=form.book_name.data,
                book_type=form.book_type.data,
                publisher=form.publisher.data,
                location=form.location.data,
                location_in_library=form.location_in_library.data,
                status=form.status.data,
                date_added=datetime.now()
            )
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('inventory'))

        return render_template('add_book.html', form=form)
    


    # --- Registration Route ---
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                role= 'Admin',
                is_active=True  # True if admin creating
            )
            new_user.password = form.password.data
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(
                url_for('login'))
        return render_template('register.html', form=form)


    return app

app = create_app()

if __name__ == '__main__':
    application = create_app()
    with application.app_context():
        db.create_all()
    application.run(debug=True)
