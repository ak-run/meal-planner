class DbConnectionError(Exception):
    pass


class RecipeDatabase:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_recipe(self, search_param, search_by):
        """
        Retrieve recipe details by a search parameter from the database.
        Args: search param (int for id, string for ingredient), search by (id or ingredient)
        Returns: dict: A dictionary containing recipe details.
        Raises: DbConnectionError: If there is an issue with the database connection.
        """
        conn = self.db_connection.get_connection_to_db()
        try:
            recipe_data = self._fetch_recipe_data(conn, search_param, search_by)
            return self.map_values_for_recipe(recipe_data)
        except Exception as e:
            raise DbConnectionError("Failed to read data during the search recipe function")
        finally:
            conn.close()

    def upload_item_to_db(self, item_to_upload, tuple_with_data):
        conn = self.db_connection.get_connection_to_db()
        try:
            cur = conn.cursor()
            if item_to_upload == "recipe":
                # query = "CALL AddRecipe (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur.callproc('AddRecipe', tuple_with_data)
                conn.commit()  # Don't forget to commit the changes
                result = cur.fetchall()
                cur.close()
                return result
            elif item_to_upload == "menu":
                pass
            else:
                return "wrong query"
        except Exception as e:
            raise DbConnectionError(f"Failed to connect to database. Error: {e}")
        finally:
            conn.close()

    def _fetch_recipe_data(self, conn, search_param, search_by):
        """
        Fetch recipe data from the database for a given recipe ID.
        Args:
            conn: The database connection.
            search_param (int): The unique identifier of the recipe to retrieve.
        Returns: list: A list of database query results.
        Note: This function is meant to be used internally by the `get_recipe_by_id` method.
        """
        try:
            cur = conn.cursor()
            if search_by == "id":
                query = f"SELECT * FROM vw_recipes_with_list_of_ingredients WHERE recipe_id = {search_param}"
            elif search_by == "ingredient":
                query = f"SELECT * FROM vw_recipes_with_list_of_ingredients WHERE ingredients LIKE '%{search_param}%'"
            else:
                return "wrong query"
            cur.execute(query)
            result = cur.fetchall()
            cur.close()
            return result
        except Exception:
            raise DbConnectionError("Failed to connect to database")

    def map_values_for_recipe(self, result):
        """Putting earch_recipe_by_recipe_id result into a dict with corresponding keys"""
        mapped = []
        for item in result:
            mapped.append({
                'Recipe ID': item[0],
                'Recipe Title': item[1],
                'Description': item[2],
                'Instructions': item[3],
                'Prep Time': item[4],
                'Cook Time': float(item[5]),
                'Servings': item[6],
                'Cuisine': item[7],
                'Difficulty': item[8],
                'Image URL': item[9],
                'Ingredients': item[10]
            })
        return mapped