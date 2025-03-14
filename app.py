from flask import Flask, render_template, request

app = Flask(__name__)

# Ethiopian Electrical Utility Pricing (ETB per kWh)
EEU_TARIFFS = [
    (50, 0.273), (100, 0.563), (200, 0.858), (500, 1.081), (float("inf"), 1.256)
]

def calculate_cost(energy_kwh):
    """Calculate electricity cost based on EEU tariff system."""
    cost = 0
    remaining_kwh = energy_kwh

    for limit, rate in EEU_TARIFFS:
        if remaining_kwh <= 0:
            break
        used_kwh = min(remaining_kwh, limit)
        cost += used_kwh * rate
        remaining_kwh -= used_kwh

    return round(cost, 2)

# ---------------- ROUTES ----------------

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/estimate")
def estimate():
    return render_template("estimate.html")

@app.route("/add-row", methods=["POST"])
def add_row():
    """HTMX - Add new row dynamically to bill estimation table."""
    return render_template("row.html")

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
    return render_template("tips.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

if __name__ == "__main__":
    app.run(debug=True)
