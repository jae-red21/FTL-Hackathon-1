from flask import Flask, render_template

app = Flask(__name__)

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
