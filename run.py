from app import app, db
from app.models import Auth, user_signin
import MySQLdb


if __name__ == "__main__":

    app.run(debug=True)
    db.create_all()
