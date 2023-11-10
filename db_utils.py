import json
from classes.db_conn import DatabaseConnection
from classes.recipe_db import RecipeDatabase, DbConnectionError

with open('config.json') as config_file:
    config = json.load(config_file)

conn = DatabaseConnection(config)
conn.get_connection_to_db()

recipe_db = RecipeDatabase(conn)


try:
    result = recipe_db.upload_item_to_db(item_to_upload="recipe", tuple_with_data=('TESTING', 'Classic Italian pasta dish', 'Cook pasta, mix with egg and cheese mixture, add crispy bacon', 15, 15, 4, 'Italian', 'Easy', 'spaghetti.jpg'))
    print(result)
except DbConnectionError as e:
    print(e)

