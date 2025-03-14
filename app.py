from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os


app = Flask(__name__)

# Configure SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "database/electricity.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize API and Database
db = SQLAlchemy(app)
api = Api(app)


@app.route("/")
def index():
    return render_template("base.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/estimate")
def estimate():
    return render_template("estimate.html")

@app.route('/tips')
def tips():
    return render_template("tips.html")

@app.route('/pricing')
def pricing():
    return render_template("pricing.html")

if __name__ == "__main__":
    app.run(debug=True)
