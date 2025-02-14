from flask import Flask
from database import db  # Import the database instance
from modules.routes import bp
import dotenv, os
from modules.routes import login_manager
from flask_bootstrap import Bootstrap5

dotenv.load_dotenv() # LOAD ENV VARIABLES
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db.init_app(app)
Bootstrap5(app)

app.register_blueprint(bp)
login_manager.init_app(app)

with app.app_context():
    db.create_all()  # Create tables if they don't exist

if __name__ == '__main__':
    app.config["DEBUG"] = True
    app.run()

