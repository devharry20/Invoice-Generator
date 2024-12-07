import os

from flask import Flask
from flask_login.login_manager import LoginManager

from database import db

FILE_NAME = "output.pdf"

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))
    DB_NAME = os.path.join(os.getcwd(), 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SECRET_KEY"] = "abc123"

    db.init_app(app)

    from models import User

    with app.app_context():
        db.create_all()

    from views import views
    app.register_blueprint(views, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "views.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    create_app()