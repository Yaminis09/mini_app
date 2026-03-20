from flask import Flask
from flask_cors import CORS
from db.db import db
from routes.task_routes import task_bp
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(task_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)