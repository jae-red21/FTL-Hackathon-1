from flask import request, jsonify
from flask_restful import Resource
from models.user_model import User, db
import joblib
import numpy as np

# Load the trained AI model
model = joblib.load("model/electricity_price_predictor.pkl")

class UserResource(Resource):
    def get(self):
        """Fetch all users"""
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    def post(self):
        """Register a new user and predict electricity cost"""
        data = request.get_json()

        username = data.get("username")
        daily_kwh = data.get("daily_consumption_kwh")
        monthly_kwh = data.get("monthly_consumption_kwh")

        if not username or not daily_kwh or not monthly_kwh:
            return {"message": "Missing data"}, 400

        # Prepare input for the AI model
        input_data = np.array([[daily_kwh, monthly_kwh]])  # Adjust based on your model
        predicted_cost = model.predict(input_data)[0]

        # Save to database
        new_user = User(username=username, daily_consumption_kwh=daily_kwh, 
                        monthly_consumption_kwh=monthly_kwh, predicted_cost=predicted_cost)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User added", "predicted_cost": predicted_cost}, 201
