from flask import Flask, render_template, request
import csv

app = Flask(__name__)


#this function takes the user's ingredients and desired cuisine
def find_recipe(user_input, user_cuisine):

    #creates an organized list of ingredients
    user_ingredients = [
        ingredient.strip().lower()
        for ingredient in user_input.split(",")
    ]

    #gets rid of any spaces or uppercase
    user_cuisine = user_cuisine.strip().lower()

    # SECTION1 1: Creates a dictionary with the ingredient families
    # Load ingredient families
    ingredient_families = {}

    with open("ingredientfamilies.csv", newline="") as ingredient_family_file:
        reader = csv.DictReader(ingredient_family_file)
        for row in reader:
            ingredient_families[row["ingredient"].lower()] = row["family"].lower()

    # Creates an empty set for the user's ingredient families
    user_families = set()

    # for each ingredient, this section adds to the list of ingredient families
    for ingredient in user_ingredients:
        if ingredient in ingredient_families:
            user_families.add(ingredient_families[ingredient])
        else:
            user_families.add(ingredient)

    # SECTION 2: Creates a dictionary with all of the recipes
    recipes = {}

    with open("allrecipes.csv", newline="") as recipe_file:
        reader = csv.DictReader(recipe_file)
        for row in reader:
            recipes[row["recipe_id"]] = {
                "name": row["name"],
                "cuisine": row["cuisine"],
                "instructions": row["instructions"],
            }

    # SECTION 3: Creates a dictionary with all of the ingredients
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

    # SECTION 4: Scores and finds the best recipes based on ingredients + user's cuisine preference.
    #we've changed the weights to only consider core and optional ingredients
    weights = {
        "core": 1.0,
        "optional": 0.5
    }

    #initializing our variables and lists
    best_recipe_id = None
    best_score = 0
    best_missing = []
    best_substitutions = []

    #for each of the recipe ids
    for recipe_id in recipe_ingredients:
        #if the user entered a cuisine and if the recipe cuisine is different
        # from the user's choice, continue past that recipe and skip the scoring
        # Skip recipes that do not match user's selected cuisine
        if user_cuisine and recipes[recipe_id]["cuisine"].lower() != user_cuisine:
            continue

        #initializing our scoring variables and ingredients + substitutions lists
        total_score = 0
        earned_score = 0
        missing_ingredients = []
        substitutions = []
        
        #for each ingredient in the recipe, get the info from the dictionary
        for item in recipe_ingredients[recipe_id]:
            ingredient = item["ingredient"]
            family = item["family"]
            importance = item["importance"]

            #find out whether this recipe was core or optional
            #the .get will default to zero if it gets an unexpected value, like before we had pantry
            weight = weights.get(importance, 0)
            #and then add that to know the maximum possible score for the recipe
            total_score += weight

            #if the ingredient is in the user's entries
            if ingredient in user_ingredients:
                #then the recipe gets the full score added
                earned_score += weight

            #if the ingredient family is generally in the same category,
            elif family in user_families:
                #then the recipe gets 0.6
                earned_score += weight * 0.6

                #for each of the user's ingredients
                for user_ingredient in user_ingredients:
                    #if that ingredient is in an ingredient family,
                    # AND if that ingredient is in the same ingredient family,
                    if (
                        user_ingredient in ingredient_families
                        and ingredient_families[user_ingredient] == family
                    ):
                        #then addd that ingredient to the substitutions list and end
                        substitutions.append((user_ingredient, ingredient))
                        break

            else:
                #otherwise, add the ingredient to the missing list
                missing_ingredients.append(ingredient)

        #this is a check for if we were to add more recipes,
        #and for some reason the importance of the ingredients isn't listed,
        #it'll just make it zero instead of crashing at the end when we try to divide
        if total_score == 0:
            continue

        #so the recipe's score is the earned score divided by the total possible score
        #and then you get the percent x100
        recipe_score = earned_score / total_score * 100

        #now, if the recipe has a better score than the previous best,
        # you update it
        if recipe_score > best_score:
            best_score = recipe_score
            best_recipe_id = recipe_id
            best_missing = missing_ingredients
            best_substitutions = substitutions

    # if we're on a valid recipe
    if best_recipe_id:
        #return a dictionary with all this info that will be sent
        # to Flask later for the html site
        return {
            "name": recipes[best_recipe_id]["name"],
            "cuisine": recipes[best_recipe_id]["cuisine"],
            #the rounded score
            "score": round(best_score, 1),
            "missing": best_missing,
            "substitutions": best_substitutions,
            "ingredients": recipe_ingredients[best_recipe_id],
            "instructions": recipes[best_recipe_id]["instructions"],
        }

    #if there were no recipes found, then return none
    return None

# SECTION 5: Connects to the website with Flask
#this connects the website to this program, get and post
#correspond to getting the webpage and submitting the form
@app.route("/", methods=["GET", "POST"])

#this function outlines what happens when you open the site
def home():
    #if you click find recipe, it corresponds to post 
    if request.method == "POST":
        #it then sets ingredients to the input from the html form
        ingredients = request.form["ingredients"]
        #and does the same from cuisine too.
        #this is instead of asking for the user's input in the body of the program
        #like we did for fpdesign.py
        cuisine = request.form["cuisine"]

        #then this sets result to the information that our big
        #find_recipe function above returns at the end
        result = find_recipe(ingredients, cuisine)

        #then this sends our result to our templates file
        return render_template("result.html", result=result)

    #and does the same for our index
    return render_template("index.html")

#this says to run the Flask server when I run this newfileflask.py file
if __name__ == "__main__":
    #this is a trick used to show errors
    app.run(debug=True)