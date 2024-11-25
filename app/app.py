from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.models import db, User
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login' 
login_manager.init_app(app)

# Default route
@app.route('/')
def index():
    # Redirect to login or home based on user authentication status
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

# Home route (protected)
@app.route('/home')
def home():
    return render_template('home.html', name=current_user.first_name)

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        school_name = request.form['school_name']
        profession = request.form['profession']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords don't match!", "danger")
            return redirect(url_for('signup'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for('signup'))

        try:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                school_name=school_name,
                profession=profession,
                phone=phone,
                email=email
            )
            new_user.set_password(password)  # Assuming User model has a set_password method
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful!", "success")
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash("An error occurred during registration. Please try again.", "danger")
            return redirect(url_for('signup'))

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):  # Assuming User model has a check_password method
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('home'))

        flash("Invalid email or password!", "danger")
        return redirect(url_for('login'))

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

# View all users (protected)
@app.route('/people')
@login_required
def people():
    users = User.query.all()
    return render_template('people.html', users=users)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database is created before running
    app.run(debug=True, port=8080)
