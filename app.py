from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp
import secrets


from classes.recipe_db import DbConnectionError
from db_utils import recipe_db

app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = foo

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)


class IngredientForm(FlaskForm):
    name = StringField('Search for recipes by ingredient ', validators=[DataRequired(), Length(1, 40)])
    submit = SubmitField('Submit')


class RecipeIdForm(FlaskForm):
    name = StringField('Search for recipes by ID ', validators=[DataRequired(), Length(1, 40)])
    submit = SubmitField('Submit')


class AddRecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 255)])
    description = StringField('Description', validators=[DataRequired(), Length(1, 1000)])
    instructions = StringField('Instructions', validators=[DataRequired(), Length(1, 1000)])
    prep_time = StringField('Prep Time', validators=[DataRequired()])
    cook_time = StringField('Cook Time', validators=[DataRequired()])
    servings = StringField('Servings', validators=[DataRequired()])
    cuisine = StringField('Cuisine', validators=[DataRequired(), Length(1, 255)])
    difficulty = StringField('Difficulty', validators=[DataRequired(), Length(1, 255)])
    image_url = StringField('Image URL', validators=[DataRequired(), Length(1, 255)])
    submit = SubmitField('Submit')

class AddRecipesToMenuForm(FlaskForm):
    start_date = StringField('Start Date (YYYY-MM-DD)', validators=[DataRequired(), Regexp(r'^\d{4}-\d{2}-\d{2}$', message='Invalid date format. Use YYYY-MM-DD.')])
    end_date = StringField('End Date (YYYY-MM-DD)', validators=[DataRequired(), Regexp(r'^\d{4}-\d{2}-\d{2}$', message='Invalid date format. Use YYYY-MM-DD.')])
    recipe_ids = StringField('Recipe IDs (comma-separated)', validators=[DataRequired(), Length(min=1, message='At least one recipe ID is required.')])
    submit = SubmitField('Add Recipes to Menu')

@app.route('/')
def welcome():
    """Route for welcome message for API"""
    return render_template("index.html")


@app.route('/recipes/id/', methods=['GET', 'POST'])
def get_recipe_by_recipe_id():
    """Route to search by recipe id and return the recipe details"""
    form = RecipeIdForm()
    message = ""
    results = []

    if form.validate_on_submit():
        recipe_id = int(form.name.data)
        try:
            results = recipe_db.get_recipe(recipe_id, search_by="id")
        except DbConnectionError as e:
            # Handle database connection errors
            return str(e), 500
        except Exception as e:
            # Handle other unexpected errors
            return 'An error occurred', 500

    return render_template('id_search.html', form=form, results=results, message=message)


@app.route('/recipes/ingredient/', methods=['GET', 'POST'])
def get_recipe_by_ingredient():
    form = IngredientForm()
    message = ""
    results = []

    if form.validate_on_submit():
        ingredient = form.name.data
        try:
            results = recipe_db.get_recipe(ingredient, search_by="ingredient")
        except DbConnectionError as e:
            # Handle database connection errors
            return str(e), 500
        except Exception as e:
            # Handle other unexpected errors
            return 'An error occurred', 500

    return render_template('ingredient_search.html', form=form, results=results, message=message)


@app.route('/recipes/', methods=['GET', 'POST'])
def add_recipe():
    form = AddRecipeForm()
    message = ""
    results = []

    if form.validate_on_submit():
        data = (
            form.title.data,
            form.description.data,
            form.instructions.data,
            form.prep_time.data,
            form.cook_time.data,
            form.servings.data,
            form.cuisine.data,
            form.difficulty.data,
            form.image_url.data,
        )
        try:
            results = recipe_db.upload_item_to_db(item_to_upload="recipe", tuple_with_data=data)
        except DbConnectionError as e:
            # Handle database connection errors
            return str(e), 500
        except Exception as e:
            # Handle other unexpected errors
            return 'An error occurred', 500

    return render_template('add_recipe.html', add_recipe_form=form, results=results, message=message)


@app.route('/recipes/add_to_menu', methods=['GET', 'POST'])
def add_recipes_to_menu_route():
    form = AddRecipesToMenuForm()

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        recipe_ids = [int(id.strip()) for id in form.recipe_ids.data.split(',')]

        try:
            result = recipe_db.add_recipes_to_menu(start_date, end_date, recipe_ids)
            # Handle the result as needed
        except DbConnectionError as e:
            # Handle database connection errors
            return str(e), 500
        except Exception as e:
            # Handle other unexpected errors
            return 'An error occurred', 500

    return render_template('add_to_menu.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

