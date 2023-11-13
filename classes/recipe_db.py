import datetime

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

    def add_recipes_to_menu(self, start_date:str, end_date:str, recipe_ids_list):
        self.add_weekly_meal_plan(start_date, end_date)
        plan_id = 5
        conn = self.db_connection.get_connection_to_db()
        try:
            cursor = conn.cursor()
            for index, recipe_id in enumerate(recipe_ids_list, start=1):
                sql_query = f"CALL AddMealPlanRecipe({plan_id}, {recipe_id}, 'day_{index}');"
                print(sql_query)
                cursor.execute(sql_query)
                conn.commit()
            return 200

        except Exception as e:
            raise DbConnectionError(f"Failed to connect to database. Error: {e}")

        finally:
            conn.close()

    def add_weekly_meal_plan(self, start_date:str, end_date:str):
        # Convert date strings to datetime objects
        start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        conn = self.db_connection.get_connection_to_db()
        try:
            cursor = conn.cursor()
            # Format the dates in the required format ('YYYY-MM-DD')
            formatted_start_date = start_date_obj.strftime('%Y-%m-%d')
            formatted_end_date = end_date_obj.strftime('%Y-%m-%d')

            # Your SQL query to call the stored procedure
            sql_query = f"CALL AddWeeklyMealPlan('{formatted_start_date}', '{formatted_end_date}')"

            # Execute the query
            cursor.execute(sql_query)
            conn.commit()
            return 200

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