import os

from flask import Flask

FILE_NAME = "output.pdf"

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))

    from views import views
    app.register_blueprint(views, url_prefix="/")

    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    create_app()