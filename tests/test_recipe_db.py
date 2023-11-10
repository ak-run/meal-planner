import unittest
import json
from classes.db_conn import DatabaseConnection
from classes.recipe_db import RecipeDatabase, DbConnectionError

with open('test_config.json') as config_file:
    test_config = json.load(config_file)

test_conn = DatabaseConnection(test_config)
test_conn.get_connection_to_db()


# Tests without Mock
class TestRecipeDatabaseNoMock(unittest.TestCase):

    def setUp(self):
        # Create a database connection
        self.db_connection = test_conn
        self.recipe_db = RecipeDatabase(self.db_connection)

    def tearDown(self):
        # Close the connection after each test
        self.db_connection.conn_close()

    def test_get_recipe_by_id_valid_query(self):
        result = self.recipe_db.get_recipe(1, "id")

        # Check if the result is as expected
        expected_result = [
            {
                'Recipe ID': 1,
                'Recipe Title': 'Spaghetti Carbonara',
                'Description': 'Classic Italian pasta dish',
                'Instructions': 'Cook pasta, mix with egg and cheese mixture, add crispy bacon',
                'Prep Time': 15,
                'Cook Time': 15.0,
                'Servings': 4,
                'Cuisine': 'Italian',
                'Difficulty': 'Easy',
                'Ingredients': 'Chicken Breast,Broccoli,Parmesan Cheese,Spaghetti,Eggs,Bacon',
                'Image URL': 'spaghetti.png'
            }
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
