CREATE DATABASE recipes_db;

USE recipes_db;

CREATE TABLE recipes(
	recipe_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(250) NOT NULL,
    recipe_description VARCHAR(400), 
    instructions VARCHAR(1000), 
    prep_time INT, 
    cook_time INT,
    servings INT,
    cuisine VARCHAR(100),
    difficulty VARCHAR(100),
    image_url VARCHAR(100)
);

CREATE TABLE ingredients_categories(
	category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE ingredients(
	ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
    ingredient_name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    unit VARCHAR(100) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES ingredients_categories(category_id)
);

-- To establish many to many relationshipt between ingredients and recipes tables

CREATE TABLE recipe_ingredients(
    recipe_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);

CREATE TABLE weekly_meal_plan(
	meal_plan_id INT PRIMARY KEY AUTO_INCREMENT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
    -- user id if users are allowed
);


-- to link recipes to meal plans
CREATE TABLE meal_plan_recipes(
	meal_plan_id INT NOT NULL,
    recipe_id INT NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    FOREIGN KEY (meal_plan_id) REFERENCES weekly_meal_plan(meal_plan_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
);

CREATE TABLE shopping_lists(
	shopping_list_id INT PRIMARY KEY AUTO_INCREMENT,
    created_date DATE NOT NULL
    -- user id if users allowed
);

-- to link shopping lists to recipes
CREATE TABLE shopping_list_items(
		shopping_list_id INT NOT NULL,
        ingredient_id INT NOT NULL,
        quantity VARCHAR(100) NOT NULL,
        PRIMARY KEY (shopping_list_id, ingredient_id),
        FOREIGN KEY (ingredient_id) REFERENCES recipe_ingredients(ingredient_id),
        FOREIGN KEY (shopping_list_id) REFERENCES shopping_lists(shopping_list_id)
);

-- STORED PROCEDURES TO ADD ROWS TO TABLE
DELIMITER $$
CREATE PROCEDURE AddRecipe(
    IN p_title VARCHAR(250),
    IN p_recipe_description VARCHAR(400),
    IN p_instructions VARCHAR(1000),
    IN p_prep_time INT,
    IN p_cook_time INT,
    IN p_servings INT,
    IN p_cuisine VARCHAR(100),
    IN p_difficulty VARCHAR(100),
    IN p_image_url VARCHAR(100)
)
BEGIN
    INSERT INTO recipes (title, recipe_description, instructions, prep_time, cook_time, servings, cuisine, difficulty, image_url)
    VALUES (p_title, p_recipe_description, p_instructions, p_prep_time, p_cook_time, p_servings, p_cuisine, p_difficulty, p_image_url);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE AddIngredientCategory(
    IN p_category_name VARCHAR(100)
)
BEGIN
    INSERT INTO ingredients_categories (category_name)
    VALUES (p_category_name);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE AddIngredient(
    IN p_ingredient_name VARCHAR(100),
    IN p_category_id INT,
    IN p_unit VARCHAR(100)
)
BEGIN
    INSERT INTO ingredients (ingredient_name, category_id, unit)
    VALUES (p_ingredient_name, p_category_id, p_unit);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE AddRecipeIngredient(
    IN p_recipe_id INT,
    IN p_ingredient_id INT
)
BEGIN
    INSERT INTO recipe_ingredients (recipe_id, ingredient_id)
    VALUES (p_recipe_id, p_ingredient_id);
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE AddWeeklyMealPlan(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    INSERT INTO weekly_meal_plan (start_date, end_date)
    VALUES (p_start_date, p_end_date);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE AddMealPlanRecipe(
    IN p_meal_plan_id INT,
    IN p_recipe_id INT,
    IN p_day_of_week VARCHAR(20)
)
BEGIN
    INSERT INTO meal_plan_recipes (meal_plan_id, recipe_id, day_of_week)
    VALUES (p_meal_plan_id, p_recipe_id, p_day_of_week);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE AddShoppingList(
    IN p_created_date DATE
)
BEGIN
    INSERT INTO shopping_lists (created_date)
    VALUES (p_created_date);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE AddShoppingListItem(
    IN p_shopping_list_id INT,
    IN p_ingredient_id INT,
    IN p_quantity VARCHAR(100)
)
BEGIN
    INSERT INTO shopping_list_items (shopping_list_id, ingredient_id, quantity)
    VALUES (p_shopping_list_id, p_ingredient_id, p_quantity);
END$$
DELIMITER ;


CREATE VIEW vw_recipe_details AS
SELECT
    r.recipe_id,
    r.title AS recipe_title,
    r.recipe_description,
    r.instructions,
    r.prep_time,
    r.cook_time,
    r.servings,
    r.cuisine,
    r.difficulty,
    r.image_url,
    i.ingredient_name,
    i.unit,
    ic.category_name AS ingredient_category
FROM recipes r
LEFT JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
LEFT JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
LEFT JOIN ingredients_categories ic ON i.category_id = ic.category_id;

CREATE VIEW vw_weekly_menu AS
SELECT
    wp.meal_plan_id,
    wp.start_date,
    wp.end_date,
    mpr.day_of_week,
    r.title AS recipe_name
FROM weekly_meal_plan wp
JOIN meal_plan_recipes mpr ON wp.meal_plan_id = mpr.meal_plan_id
JOIN recipes r ON mpr.recipe_id = r.recipe_id;

CREATE VIEW vw_shopping_list AS
SELECT
    sl.shopping_list_id,
    sli.ingredient_id,
    i.ingredient_name,
    sli.quantity
FROM shopping_lists sl
JOIN shopping_list_items sli ON sl.shopping_list_id = sli.shopping_list_id
JOIN ingredients i ON sli.ingredient_id = i.ingredient_id;

-- Add sample recipes
CALL AddRecipe('Spaghetti Carbonara', 'Classic Italian pasta dish', 'Cook pasta, mix with egg and cheese mixture, add crispy bacon', 15, 15, 4, 'Italian', 'Easy', 'spaghetti.jpg');
CALL AddRecipe('Chicken Stir-Fry', 'Healthy stir-fry with vegetables and chicken', 'Cook chicken and vegetables in a wok with sauce', 20, 15, 4, 'Asian', 'Medium', 'stir-fry.jpg');
CALL AddRecipe('Vegetable Lasagna', 'Vegetarian lasagna with layers of vegetables and cheese', 'Layer pasta, vegetables, and cheese, bake in oven', 30, 45, 6, 'Italian', 'Medium', 'lasagna.jpg');

-- Add sample ingredient categories
CALL AddIngredientCategory('Meat');
CALL AddIngredientCategory('Vegetables');
CALL AddIngredientCategory('Dairy');
CALL AddIngredientCategory('Grains');
CALL AddIngredientCategory('Herbs and Spices');
CALL AddIngredientCategory('Sauces');

-- Add sample ingredients
CALL AddIngredient('Chicken Breast', 1, 'pieces');
CALL AddIngredient('Broccoli', 2, 'grams');
CALL AddIngredient('Parmesan Cheese', 3, 'grams');

CALL AddIngredient('Spaghetti', 4, 'grams');
CALL AddIngredient('Eggs', 3, 'pieces');
CALL AddIngredient('Bacon', 1, 'grams');

CALL AddIngredient('Rice', 4, 'grams');
CALL AddIngredient('Soy Sauce', 6, 'ml');
CALL AddIngredient('Bell Peppers', 2, 'pieces');

CALL AddIngredient('Lasagna Noodles', 4, 'grams');
CALL AddIngredient('Zucchini', 2, 'grams');
CALL AddIngredient('Mozzarella Cheese', 3, 'grams');

-- Add recipe_ingredients to match the additional ingredients
CALL AddRecipeIngredient(1, 1); -- Chicken Breast for Recipe 1
CALL AddRecipeIngredient(1, 2); -- Broccoli for Recipe 1
CALL AddRecipeIngredient(1, 3); -- Parmesan Cheese for Recipe 1

CALL AddRecipeIngredient(1, 4);  -- Spaghetti
CALL AddRecipeIngredient(1, 5);  -- Eggs
CALL AddRecipeIngredient(1, 6);  -- Bacon

CALL AddRecipeIngredient(2, 4);  -- Rice
CALL AddRecipeIngredient(2, 5);  -- Soy Sauce
CALL AddRecipeIngredient(2, 7);  -- Bell Peppers

CALL AddRecipeIngredient(3, 8);  -- Lasagna Noodles
CALL AddRecipeIngredient(3, 9);  -- Zucchini
CALL AddRecipeIngredient(3, 10); -- Mozzarella Cheese


-- Add sample weekly meal plan
CALL AddWeeklyMealPlan('2023-11-01', '2023-11-07');
CALL AddWeeklyMealPlan('2023-11-08', '2023-11-14');
CALL AddWeeklyMealPlan('2023-11-15', '2023-11-21');

-- Add sample meal plan recipes
CALL AddMealPlanRecipe(1, 1, 'Monday');
CALL AddMealPlanRecipe(1, 2, 'Tuesday');
CALL AddMealPlanRecipe(1, 3, 'Wednesday');
CALL AddMealPlanRecipe(2, 2, 'Monday');
CALL AddMealPlanRecipe(2, 1, 'Tuesday');
CALL AddMealPlanRecipe(2, 3, 'Wednesday');
CALL AddMealPlanRecipe(3, 3, 'Monday');
CALL AddMealPlanRecipe(3, 2, 'Tuesday');
CALL AddMealPlanRecipe(3, 1, 'Wednesday');

-- Add sample shopping lists
CALL AddShoppingList('2023-11-01');
CALL AddShoppingList('2023-11-08');
CALL AddShoppingList('2023-11-15');

-- Add sample shopping list items
CALL AddShoppingListItem(1, 4, '250 grams'); -- Spaghetti
CALL AddShoppingListItem(1, 3, '2 pieces');   -- Eggs
CALL AddShoppingListItem(1, 6, '100 grams');  -- Bacon

CALL AddShoppingListItem(2, 4, '300 grams');  -- Rice
CALL AddShoppingListItem(2, 5, '30 ml');      -- Soy Sauce
CALL AddShoppingListItem(2, 7, '2 pieces');    -- Bell Peppers

CALL AddShoppingListItem(3, 8, '400 grams');   -- Lasagna Noodles
CALL AddShoppingListItem(3, 9, '300 grams');   -- Zucchini
CALL AddShoppingListItem(3, 10, '200 grams');  -- Mozzarella Cheese

SELECT *
FROM ingredients;

SELECT *
FROM ingredients_categories;

SELECT *
FROM meal_plan_recipes;

SELECT *
FROM recipe_ingredients;

SELECT *
FROM recipes;

SELECT *
FROM shopping_list_items;

SELECT *
FROM shopping_lists;

SELECT *
FROM weekly_meal_plan;

SELECT *
FROM vw_recipe_details;

SELECT *
FROM vw_shopping_list;

SELECT *
FROM vw_weekly_menu;


SELECT * FROM vw_recipes_with_list_of_ingredients WHERE ingredients LIKE '%chicken%';

UPDATE recipes
SET image_url = "spaghetti.png"
WHERE recipe_id = 1;

