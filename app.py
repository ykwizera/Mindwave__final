from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.models import db, User

app = Flask(__name__)

# Configuration for app
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB and LoginManager
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Route for the home page (protected)
@app.route('/home')
@login_required
def home():
    return render_template('app/home.html', name=current_user.first_name)

# Route for signup page
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

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            school_name=school_name,
            profession=profession,
            phone=phone,
            email=email
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for('login'))

    return render_template('app/signup.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('home'))

        flash("Invalid email or password!", "danger")
        return redirect(url_for('login'))

    return render_template('app/login.html')

# Route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

# Route to display all registered users (people page)
@app.route('/people')
@login_required
def people():
    users = User.query.all()
    return render_template('app/people.html', users=users)

# Load user by ID (used for login management)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)
