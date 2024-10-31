from flask_app import app, bcrypt
from flask_app.models.user import User
from flask import flash, redirect, render_template, request, session
from flask_app.models.recipe import Recipe




@app.get("/recipes")
def recipes():
    """This route displays the user dashboard"""
    if "user_id" not in session:
        flash("You must be logged in to view that page","login")
        return redirect("/")
    recipes = Recipe.get_all_with_users()
    print(recipes)
    user_all = User
    user = User.find_by_user_id(session["user_id"])
    return render_template("recipes.html",  user=user, all_recipes = recipes, user_all = user_all)


@app.get("/recipes/new")
def recipes_new():
    

    user = User.find_by_user_id(session["user_id"])
    return render_template("recipes_new.html",  user=user)

@app.route('/create_recipe', methods=["POST"])
def create_recipe():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        #"id": request.form["id"], # might break if uncommented
        "name": request.form["name"],
        "under_30": request.form["under_30"],
        "user_id": session["user_id"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "created_at": request.form["created_at"],
        #"updated_at": request.form["updated_at"],
    }
    
    # We pass the data dictionary into the save method from the Friend class.
    Recipe.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/recipes')

@app.post('/edit_recipe')
def edit_recipe():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    """""
    data = {
        #"id": request.form["id"], # might break if uncommented
        "name": request.form["name"],
        "under_30": request.form["under_30"],
        "user_id": session["user_id"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "created_at": request.form["created_at"],
        #"updated_at": request.form["updated_at"],
    }
    """
    
    # We pass the data dictionary into the save method from the Friend class.
    Recipe.update(request.form)
    # Don't forget to redirect after saving to the database.
    return redirect('/recipes')


@app.get("/recipes/view/<int:recipe_id>") 
def recipes_view(recipe_id):
    recipe = Recipe.get_one(recipe_id)
    print(recipes)

    user = User.find_by_user_id(session["user_id"])
    return render_template("recipes_view.html",  user=user, recipe = recipe)

#######################################################################################   START HERE BRO!!!!!
@app.get("/recipes/edit/<int:recipe_id>")
def recipes_edit(recipe_id):
    recipe = Recipe.get_one(recipe_id)
    print(recipes)

    user = User.find_by_user_id(session["user_id"])
    return render_template("recipes_edit.html",  user=user, recipe = recipe)


@app.post("/recipes/delete/<int:recipe_id>")
def delet_recipe(recipe_id):

    Recipe.delete_by_id(recipe_id)
    return redirect("/recipes")
    

"""
@app.get("/recipes")
def recipes():
    
    return render_template("recipes.html")
"""

"""


@app.post("/users/login")
def login():
    

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
    return redirect("/users/dashboard")

@app.get("/users/logout")
def logout():
    
    session.clear()
    return redirect("/")



@app.get("/users/dashboard")
def dashboard():
    
    if "user_id" not in session:
        flash("You must be logged in to view that page","login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])
    return render_template("dashboard.html",  user=user)

"""