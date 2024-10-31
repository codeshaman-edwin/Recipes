from flask_app import app, bcrypt
from flask_app.models.user import User
from flask import flash, redirect, render_template, request, session

@app.get("/")
def index():
    """This route desplays the login registration forms."""
    return render_template("index.html")

@app.post("/users/register")
def register():
    """This route processes the register form"""

    if not User.register_form_is_valid(request.form):
        return redirect("/")
    
    potential_user = User.find_by_email(request.form["email"])

    if potential_user != None:
        flash("Email in use. Please log in", "register")
        return redirect("/")

    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    user_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw,
    }
    user_id = User.register(user_data)
    session["user_id"] = user_id
    return redirect("/recipes")


@app.post("/users/login")
def login():
    """This route processes the login form"""

    if not User.login_form_is_valid(request.form):
        return redirect("/")
    
    potential_user = User.find_by_email(request.form["email"])
    if potential_user == None:
        flash("Invalid credentials", "login")
        return redirect("/")
    
    # user exists!
    user = potential_user

    # check the password
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid credentials","login")
        return redirect("/")
    
    session['user_id'] = user.id
    return redirect("/recipes")

@app.get("/users/logout")
def logout():
    """This route clears session"""
    session.clear()
    return redirect("/")



@app.get("/users/dashboard")
def dashboard():
    """This route displays the user dashboard"""
    if "user_id" not in session:
        flash("You must be logged in to view that page","login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])
    return render_template("dashboard.html",  user=user)