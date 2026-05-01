from flask import Flask, render_template, request
import csv

app = Flask(__name__)


def find_recipe(user_input, user_cuisine):
    user_ingredients = [
        ingredient.strip().lower()
        for ingredient in user_input.split(",")
    ]

    user_cuisine = user_cuisine.strip().lower()

    # Load ingredient families
    ingredient_families = {}

    with open("ingredientfamilies.csv", newline="") as ingredient_family_file:
        reader = csv.DictReader(ingredient_family_file)
        for row in reader:
            ingredient_families[row["ingredient"].lower()] = row["family"].lower()

    # Find user's ingredient families
    user_families = set()

    for ingredient in user_ingredients:
        if ingredient in ingredient_families:
            user_families.add(ingredient_families[ingredient])
        else:
            user_families.add(ingredient)

    # Load recipes
    recipes = {}

    with open("allrecipes.csv", newline="") as recipe_file:
        reader = csv.DictReader(recipe_file)
        for row in reader:
            recipes[row["recipe_id"]] = {
                "name": row["name"],
                "cuisine": row["cuisine"],
                "instructions": row["instructions"],
            }

    # Load recipe ingredients
    recipe_ingredients = {}

    with open("allingredients.csv", newline="") as ingredient_file:
        reader = csv.DictReader(ingredient_file)

        for row in reader:
            recipe_id = row["recipe_id"]

            if recipe_id not in recipe_ingredients:
                recipe_ingredients[recipe_id] = []

            recipe_ingredients[recipe_id].append({
                "ingredient": row["ingredient"].lower(),
                "family": row["family"].lower(),
                "importance": row["importance"].lower(),
                "quantity": row["quantity"],
                "unit": row["unit"],
            })

    weights = {
        "core": 1.0,
        "optional": 0.5
    }

    best_recipe_id = None
    best_score = 0
    best_missing = []
    best_substitutions = []

    for recipe_id in recipe_ingredients:
        # Skip recipes that do not match selected cuisine
        if user_cuisine and recipes[recipe_id]["cuisine"].lower() != user_cuisine:
            continue

        total_score = 0
        earned_score = 0
        missing_ingredients = []
        substitutions = []

        for item in recipe_ingredients[recipe_id]:
            ingredient = item["ingredient"]
            family = item["family"]
            importance = item["importance"]

            weight = weights.get(importance, 0)
            total_score += weight

            if ingredient in user_ingredients:
                earned_score += weight

            elif family in user_families:
                earned_score += weight * 0.6

                for user_ingredient in user_ingredients:
                    if (
                        user_ingredient in ingredient_families
                        and ingredient_families[user_ingredient] == family
                    ):
                        substitutions.append((user_ingredient, ingredient))
                        break

            else:
                missing_ingredients.append(ingredient)

        if total_score == 0:
            continue

        recipe_score = earned_score / total_score * 100

        if recipe_score > best_score:
            best_score = recipe_score
            best_recipe_id = recipe_id
            best_missing = missing_ingredients
            best_substitutions = substitutions

    if best_recipe_id:
        return {
            "name": recipes[best_recipe_id]["name"],
            "cuisine": recipes[best_recipe_id]["cuisine"],
            "score": round(best_score, 1),
            "missing": best_missing,
            "substitutions": best_substitutions,
            "ingredients": recipe_ingredients[best_recipe_id],
            "instructions": recipes[best_recipe_id]["instructions"],
        }

    return None


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ingredients = request.form["ingredients"]
        cuisine = request.form["cuisine"]

        result = find_recipe(ingredients, cuisine)

        return render_template("result.html", result=result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)