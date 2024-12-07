import os

from flask import Flask

FILE_NAME = "output.pdf"

def create_app():
    app = Flask(__name__, template_folder=os.getcwd() + r"\static\templates")

    from views import views
    app.register_blueprint(views, url_prefix="/")

    app.run(debug=True)

if __name__ == "__main__":
    create_app()