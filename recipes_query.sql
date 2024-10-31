

SELECT * FROM recipes_db.users; 

SELECT * FROM recipes_db.recipes;

INSERT INTO recipes_db.recipes (name, under_30, user_id, description, instructions, created_at, updated_at) VALUES ("cheezy bread", "yes", 1, "delicious", "cook it then eat it",NOW(), NOW());
INSERT INTO recipes_db.recipes (name, under_30, user_id, description, instructions, created_at, updated_at) VALUES ("cheese sticks", "yes", 1, "delicious", "eat too much",NOW(), NOW());