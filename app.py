from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from models import db, User 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

    return render_template('signup.html')

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

    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html', name=current_user.first_name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

@app.route('/people')
@login_required
def people():
    users = User.query.all()
    return render_template('people.html', users=users)

if __name__ == "__main__":
    app.run(debug=True)
