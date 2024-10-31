from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models.user import User

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Recipe:
    #_db = "login_reg_db"

    _db = "recipes_db"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        #self.updated_at = data['updated_at']
        self.user_id = data["user_id"]
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(Recipe._db).query_db(query)
        # Create an empty list to append our instances of friends
        friends = []
        # Iterate over the db results and create instances of friends with cls.
        for friend in results:
            friends.append(cls(friend))
        return friends
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO recipes (name, under_30, user_id, description, instructions, created_at, updated_at) 
        VALUES (%(name)s, %(under_30)s,%(user_id)s, %(description)s, %(instructions)s, NOW(), NOW());"""
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(Recipe._db).query_db(query, data)
    
    
    #user_id = %(user_id)s,
    @classmethod
    def update(cls, form_data):
        query = """
        UPDATE recipes 
        SET
        id = %(id)s,
        name = %(name)s,
        under_30 = %(under_30)s,
        
        description = %(description)s,
        instructions = %(instructions)s,
        created_at = NOW()
        WHERE id = %(id)s;
        """
        # data is a dictionary that will be passed into the save method from server.py
        connectToMySQL(Recipe._db).query_db(query, form_data)
        return

    @classmethod
    def get_one(cls, recipe_id):
        query  = "SELECT * FROM recipes WHERE id = %(recipe_id)s;"
        data = {'recipe_id': recipe_id}
        results = connectToMySQL(Recipe._db).query_db(query, data)
        #return cls(results[0])
        recipe = Recipe(results[0])
        return recipe
    
    @classmethod
    def get_all_with_users(cls):
        query = """
        SELECT * FROM recipes
        JOIN users
        ON recipes.user_id = users.id;
        """
        # make sure to call the connectToMySQL function with the schema you are targeting.
        list_of_dicts = connectToMySQL(Recipe._db).query_db(query)
        # Create an empty list to append our instances of friends
        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        for each_dict in list_of_dicts:
            recipe = Recipe(each_dict)
            user_data = {
                "id": each_dict["users.id"], 
                "first_name": each_dict["first_name"], 
                "last_name": each_dict["last_name"], 
                "email": each_dict["email"], 
                "password": each_dict["password"], 
                "created_at": each_dict["users.created_at"], 
                "updated_at": each_dict["users.updated_at"],                
                
            }
            user = User(user_data)
            recipe.user = user
            recipes.append(recipe)

        return recipes
    
    @classmethod
    def delete_by_id(cls, recipe_id):

        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        data = {"recipe_id": recipe_id}
        connectToMySQL(Recipe._db).query_db(query, data)
        return
    
    @staticmethod
    def create_form_is_valid(form_data):
        """This method validates the registration form"""

        is_valid = True

        if len(form_data['name'].strip()) == 0:
            flash("Please enter name.","create")
            is_valid = False
            print("FORM IS NOT VALID -- REDIRECTING - IF")
        elif len(form_data['name'].strip()) < 2:
            flash("Name must be at least 3 characters.","create")
            is_valid = False
            print("FORM IS NOT VALID -- REDIRECTING - ELIF")

        if len(form_data['under_30'].strip()) == 0:
            flash("Please enter under 30.","create")
            is_valid = False
            print("FORM IS NOT VALID -- REDIRECTING - IF")
        elif len(form_data['under_30'].strip()) < 3:
            flash("Under 30 must be at least 3 characters.","create")
            is_valid = False
            print("FORM IS NOT VALID -- REDIRECTING - ELIF")            
        
        if len(form_data['description'].strip()) == 0:
            flash("Please enter description.","create")
            is_valid = False
            print("FORM IS NOT VALID -- REDIRECTING - IF")
        elif not EMAIL_REGEX.match(form_data['description']):
            flash("Description is invalid","create")
            is_valid = False
            print("FORM IS NOT VALID -- REDIRECTING - ELIF")

        if len(form_data['instructions'].strip()) == 0:
            flash("Please enter instructions.","create")
            is_valid = False
            print("FORM IS NOT VALID -- REDIRECTING - IF")
        elif not EMAIL_REGEX.match(form_data['instructions']):
            flash("Instructions is invalid","create")
            is_valid = False
            print("FORM IS NOT VALID -- REDIRECTING - ELIF")

        return is_valid

        