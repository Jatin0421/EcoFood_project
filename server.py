from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

# Initialize Flask app with current directory for templates and static files
app = Flask(__name__)
app.config["SECRET_KEY"] = "Jardani jovonovich"  # Use a secure key in production
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecofood.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# --------------------------
# USER MODEL (Authentication)
# --------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)  # For Google users, password can be None
    role = db.Column(db.String(20), nullable=False, default="User")  # e.g., Donor, Recipient, Admin, User
    google_id = db.Column(db.String(200), unique=True, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --------------------------
# DONATION MODEL
# --------------------------
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    expiry_date = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(20), nullable=False)

# --------------------------
# VOLUNTEER MODEL
# --------------------------
class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

# --------------------------
# ROUTES FOR HTML PAGES & FORM SUBMISSIONS
# --------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

# ----- Signup Route -----
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # For form submission, data comes from request.form
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role", "User")

        if User.query.filter_by(email=email).first():
            error = "Email already registered"
            return render_template("signup.html", error=error)
        
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    
    return render_template("signup.html")

# ----- Login Route -----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user and user.password and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        
        error = "Invalid credentials"
        return render_template("login.html", error=error)
    
    return render_template("login.html")

# ----- Google Login Route (JSON Only) -----
@app.route("/google-login", methods=["POST"])
def google_login():
    data = request.json
    token = data.get("token")
    if not token:
        return jsonify({"error": "Missing token"}), 400
    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
        email = idinfo.get("email")
        google_id_val = idinfo.get("sub")
        username = idinfo.get("name")
        
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(username=username, email=email, password=None, role="User", google_id=google_id_val)
            db.session.add(user)
            db.session.commit()
        else:
            if not user.google_id:
                user.google_id = google_id_val
                db.session.commit()
        
        login_user(user)
        return jsonify({"message": "Google login successful!", "email": email, "role": user.role}), 200
    except ValueError as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 400

# ----- Logout Route -----
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ----- Donate Food Route -----
@app.route("/donate", methods=["GET", "POST"])
@login_required
def donate_food():
    if request.method == "POST":
        # Data from form submission
        food_name = request.form.get("foodName")
        quantity = request.form.get("quantity")
        expiry_date = request.form.get("expiryDate")
        location = request.form.get("location")
        contact = request.form.get("contact")

        new_donation = Donation(food_name=food_name, quantity=quantity,
                                expiry_date=expiry_date, location=location, contact=contact)
        db.session.add(new_donation)
        db.session.commit()
        return redirect(url_for("dashboard"))
    
    return render_template("donate.html")

# ----- Food Listing Route -----
@app.route("/food-list")
def get_food_list():
    donations = Donation.query.all()
    # For a simple HTML view, pass donations to template
    return render_template("food-list.html", donations=donations)

# ----- Volunteer Signup Route -----
@app.route("/volunteer", methods=["GET", "POST"])
def volunteer_signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")

        if Volunteer.query.filter_by(email=email).first():
            error = "Volunteer with this email already registered"
            return render_template("volunteer.html", error=error)
        
        new_volunteer = Volunteer(name=name, email=email, phone=phone)
        db.session.add(new_volunteer)
        db.session.commit()
        return redirect(url_for("home"))
    
    return render_template("volunteer.html")

# --------------------------
# RUN THE APP
# --------------------------
# if __name__ == "_main_":
#     with app.app_context():
#        db.create_all()  # Create database tables if they don't exist
#     app.run(debug=True)
    
if __name__ == "__main__":
     with app.app_context():
        db.create_all()  # Create database tables if they don't exis
     app.run(debug=True, host="0.0.0.0", port=5000)
