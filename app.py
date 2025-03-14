from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os
import numpy as np
from models.user_models import User
from models.user_models import init_db
from extensions import db
from routes.user_routes import UserResource
import joblib



app = Flask(__name__)

# Load Machine Learning Model
model = joblib.load("Model/electricity_price_predictor.pkl")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "database/electricity.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
#db = SQLAlchemy(app)
api = Api(app)

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
    usage_data = [
        {'appliance': 'Air Conditioner', 'power_rating': 2000, 'duration': 5, 'total_energy': 10},
        {'appliance': 'Washing Machine', 'power_rating': 500, 'duration': 1, 'total_energy': 0.5},
        {'appliance': 'Refrigerator', 'power_rating': 150, 'duration': 24, 'total_energy': 3.6},
    ]
    return render_template("dashboard.html", user=user, usage_data=usage_data)


@app.route("/estimate")
def estimate():
    user = get_logged_in_user()
    appliances = [
        {'name': '', 'power_rating': 0, 'usage_hours': 0, 'quantity': 1}
    ]
    return render_template("estimate.html", user=user, appliances=appliances)


@app.route("/add-row", methods=["POST"])
def add_row():
    """HTMX - Add new row dynamically to bill estimation table."""
    new_appliance = {'name': '', 'power_rating': 0, 'usage_hours': 0, 'quantity': 1}
    return render_template("row.html", appliance=new_appliance)

@app.route("/remove-row", methods=["DELETE"])
def remove_row():
    """HTMX - Remove row dynamically."""
    return "", 204



@app.route("/calculate-bill", methods=["POST"])
def calculate_bill():
    """Calculate estimated electricity bill based on appliance usage."""
    
    # Get the form data
    try:
        appliances = request.form.getlist('appliance_name[]')
        power_ratings = request.form.getlist('power_rating[]')
        usage_hours = request.form.getlist('usage_hours[]')
        quantities = request.form.getlist('quantity[]')
        
        # Ensure at least one valid row is provided
        if not any(power_ratings) or not any(usage_hours) or not any(quantities):
            return "<p class='text-red-600'>Error: Please enter valid appliance details before estimating.</p>"
        
        
        # Convert inputs to float
        try:
            power_ratings = [float(p) if p.strip() else 0 for p in power_ratings]
            usage_hours = [float(h) if h.strip() else 0 for h in usage_hours]
            quantities = [float(q) if q.strip() else 0 for q in quantities]
        except ValueError:
            return "<p class='text-red-600'>Error: Invalid input. Please enter numeric values.</p>"

        # Ensure at least one appliance has nonzero values
        if sum(power_ratings) == 0 or sum(usage_hours) == 0 or sum(quantities) == 0:
            return "<p class='text-red-600'>Error: Please enter valid appliance details before estimating.</p>"
        
        # Define model input shape (16 features)
        num_appliances = len(power_ratings)
        feature_vector_length = 16
        

        # Initialize a feature matrix filled with zeros
        appliance_data = np.zeros((num_appliances, feature_vector_length))

        for i in range(num_appliances):
            appliance_data[i, 0] = power_ratings[i]  # Power rating (W)
            appliance_data[i, 1] = usage_hours[i]    # Usage hours (hrs)
            appliance_data[i, 2] = quantities[i]     # Quantity


        # Make prediction using the model
        predicted_cost = model.predict(appliance_data)

        # Return the estimated cost
        total_cost = predicted_cost.sum()
        return f"<p class='text-green-600 font-bold'>Estimated Cost: {total_cost:.2f} ETB</p>"


    except Exception as e:
        return f"<p class='text-red-600'>Error: {str(e)}</p>"

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
