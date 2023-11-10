import unittest
from unittest.mock import Mock, patch
from classes.recipe_db import RecipeDatabase, DbConnectionError


# Tests using Mock
class TestRecipeDatabase(unittest.TestCase):
    def setUp(self):
        # Create a mock database connection
        self.db_connection = Mock()
        self.recipe_db = RecipeDatabase(self.db_connection)

    def test_get_recipe_by_id_valid_query(self):
        # Create a mock database connection
        mock_connection = self.db_connection.get_connection_to_db.return_value
        # Define the result you expect from the database query
        mock_result = [(1, 'Recipe 1', 'Description 1', 'Instructions 1', '30 mins', 2.5, 4, 'Cuisine 1', 'Easy', 'image.jpg', 'Ingredient 1, Ingredient 2')]

        # Mock the cursor and execute method
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchall.return_value = mock_result

        # Call the get_recipe method
        result = self.recipe_db.get_recipe(1, "id")

        # Check if the result is as expected
        expected_result = [
            {
                'Recipe ID': 1,
                'Recipe Title': 'Recipe 1',
                'Description': 'Description 1',
                'Instructions': 'Instructions 1',
                'Prep Time': '30 mins',
                'Cook Time': 2.5,
                'Servings': 4,
                'Cuisine': 'Cuisine 1',
                'Difficulty': 'Easy',
                'Image URL': 'image.jpg',
                'Ingredients': 'Ingredient 1, Ingredient 2'
            }
        ]
        self.assertEqual(result, expected_result)

    def test_get_recipe_by_ingredient_valid_query(self):
        # Create a mock database connection
        mock_connection = self.db_connection.get_connection_to_db.return_value
        # Define the result you expect from the database query
        mock_result = [(1, 'Recipe 1', 'Description 1', 'Instructions 1', '30 mins', 2.5, 4, 'Cuisine 1', 'Easy', 'image.jpg', 'Ingredient 1, Ingredient 2')]

        # Mock the cursor and execute method
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchall.return_value = mock_result

        # Call the get_recipe method
        result = self.recipe_db.get_recipe("Ingredient 1", "ingredient")

        # Check if the result is as expected
        expected_result = [
            {
                'Recipe ID': 1,
                'Recipe Title': 'Recipe 1',
                'Description': 'Description 1',
                'Instructions': 'Instructions 1',
                'Prep Time': '30 mins',
                'Cook Time': 2.5,
                'Servings': 4,
                'Cuisine': 'Cuisine 1',
                'Difficulty': 'Easy',
                'Image URL': 'image.jpg',
                'Ingredients': 'Ingredient 1, Ingredient 2'
            }
        ]
        self.assertEqual(result, expected_result)

    def test_get_recipe_by_id_valid_id_not_in_db(self):
        # Create a mock database connection
        mock_connection = self.db_connection.get_connection_to_db.return_value
        # Define the result you expect from the database query

        # Mock the cursor and execute method
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchall.return_value = []

        # Call the get_recipe method
        result = self.recipe_db.get_recipe(500, "id")

        # Check if the result is as expected
        expected_result = []
        self.assertEqual(result, expected_result)

    def test_get_recipe_db_connection_error(self):
        # Mock a database connection that raises a DbConnectionError
        self.db_connection.get_connection_to_db.side_effect = DbConnectionError

        with self.assertRaises(DbConnectionError):
            self.recipe_db.get_recipe(1, "id")


if __name__ == '__main__':
        unittest.main()