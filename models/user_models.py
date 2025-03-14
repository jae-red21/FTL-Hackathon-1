from extensions import db
# from flask_sqlalchemy import SQLAlchemy


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    daily_consumption_kwh = db.Column(db.Float, nullable=False)
    monthly_consumption_kwh = db.Column(db.Float, nullable=False)
    predicted_cost = db.Column(db.Float, nullable=True)

    def __init__(self, username, daily_consumption_kwh, monthly_consumption_kwh, predicted_cost):
        self.username = username
        self.daily_consumption_kwh = daily_consumption_kwh
        self.monthly_consumption_kwh = monthly_consumption_kwh
        self.predicted_cost = predicted_cost

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "daily_consumption_kwh": self.daily_consumption_kwh,
            "monthly_consumption_kwh": self.monthly_consumption_kwh,
            "predicted_cost": self.predicted_cost
        }
# Initialize the database with the Flask app context
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # This creates the tables