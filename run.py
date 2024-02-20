from app import app, db
from app.models import Auth, user_signin
import MySQLdb


if __name__ == "__main__":
    with app.app_context():
        # Creating table first !!
        db.create_all()
        # Running the flask app
        app.run(debug=True)
