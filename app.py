from app import create_app, db
from app.models import User

# Create an app instance
app = create_app()

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
