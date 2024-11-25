from flask import Flask, render_template, request, redirect, url_for
from models import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

@app.route('/register', methods=['GET', 'POST'])
def register():
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
            return "Passwords do not match. Please try again."

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

        return redirect(url_for('people'))

    return render_template('signup.html')

@app.route('/people')
def people():
    users = User.query.all()
    return render_template('people.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
