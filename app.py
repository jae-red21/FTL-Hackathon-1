from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os
from models.user_models import init_db
from extensions import db
from routes.user_routes import UserResource

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "database/electricity.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
#db = SQLAlchemy(app)
api = Api(app)


# Import models and routes
from routes.user_routes import UserResource

# Create database tables
with app.app_context():
    db.create_all()

# Register API endpoints
api.add_resource(UserResource, "/user")


@app.route("/")
def index():
    user = get_logged_in_user()
    return render_template("base.html", user=user)

@app.route("/dashboard")
def dashboard():
    user = get_logged_in_user()
    return render_template("dashboard.html", user=user)


@app.route("/estimate")
def estimate():
    user = get_logged_in_user()
    return render_template("estimate.html", user=user)


@app.route("/add-row", methods=["POST"])
def add_row():
    """HTMX - Add new row dynamically to bill estimation table."""
    return render_template("row.html")

@app.route("/remove-row", methods=["DELETE"])
def remove_row():
    """HTMX - Remove row dynamically."""
    return ""

@app.route("/calculate-bill", methods=["POST"])
def calculate_bill():
    """Calculate estimated electricity bill based on appliance usage."""
    try:
        power_ratings = list(map(float, request.form.getlist("power_rating[]")))
        usage_hours = list(map(float, request.form.getlist("usage_hours[]")))
        quantities = list(map(int, request.form.getlist("quantity[]")))

        total_energy = sum((p * h * q) / 1000 for p, h, q in zip(power_ratings, usage_hours, quantities))
        estimated_cost = calculate_cost(total_energy)

        return f"Estimated Cost: {estimated_cost} ETB"
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/tips")
def tips():
    user = get_logged_in_user()
    return render_template("tips.html", user=user)

@app.route("/pricing")
def pricing():
    user = get_logged_in_user()
    return render_template("pricing.html", user=user)

def calculate_cost(total_energy):
    # Define your cost calculation logic here
    cost_per_kwh = 0.5  # Example cost per kWh
    return total_energy * cost_per_kwh

def get_logged_in_user():
     if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return user
     return None

if __name__ == "__main__":
    app.run(debug=True)
