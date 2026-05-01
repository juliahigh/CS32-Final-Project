import csv

print ("Welcome to the CS32 cookbook!\nYou tell us your ingredients, and we will recommend a recipe.")
#enter to begin
input("Press enter to begin.")

#create this empty list of the user's ingredients
#testing 123
user_ingredients = []
#request input
user_input = input("Please list up to 20 ingredients you have in your kitchen, separated by commas: ")
user_cuisine = input("What cuisine would you like to have? The options are:\nItalian\nAsian\nMexican\nAmerican\nFrench\nIndian\nSeafood\nRussian\nGreek\nMiddle Eastern")


#take the user's input and split it along the commas. for each of those ingredients...
for ingredient in user_input.split(","):
    #add to the list user_ingredients. and get rid of commas and lowercase everything so you don't have to deal with
    #confusing between upper and lowercase
    user_ingredients.append(ingredient.strip().lower())

#load ingredient families dictionary
ingredient_families = {}

#open the ingredient families file
with open('ingredientfamilies.csv') as ingredient_family_file:
    #read through each line of the ingredient family file
    reader = csv.DictReader(ingredient_family_file)
    #for each line of our ingredient family file
    for row in reader:
        #add to this ingredient families dictionary by labeling the ingredient
        #that matches up to the .csv file and the family category.
        #lowercase everything to keep everything standard
        ingredient_families[row['ingredient'].lower()] = row['family'].lower()

#find the user's ingredient families
user_families = set()
#for each of the user inputted ingredients
for ingredient in user_ingredients:
    #if that ingredient is in one of our pre-set ingredient families
    #this will be more relevant once we add more detail to the ingredient families
    if ingredient in ingredient_families:
        #add the family to this set of user families
        user_families.add(ingredient_families[ingredient])
    #otherwise, just add the ingredient by itself
    else:
        user_families.add(ingredient)

#load up the recipes
recipes = {}


with open ("allrecipes.csv") as recipe_file:
    reader = csv.DictReader(recipe_file)
    #for each line in the recipe file
    for row in reader:
        #with the recipe id as the key in the dictionary,
        #save the info that we need to know for each recipe
        recipes[row['recipe_id']] = {
            "name": row['name'],
            "cuisine": row['cuisine'],
            "instructions": row['instructions'],
        }

#load the recipe ingredients
recipe_ingredients = {}

with open("allingredients.csv") as ingredient_file:
    reader = csv.DictReader(ingredient_file)

    for row in reader:
        #getting the recipe id which is just the number assigned to it in the file
        recipe_id = row["recipe_id"]
        #if the recipe hasn't been added to the dictionary...
        if row['recipe_id'] not in recipe_ingredients:
            recipe_ingredients[row['recipe_id']] = []

        #add it to the empty list^^
        #then store all of the ingredient info, lowercasing when necessary
        recipe_ingredients[recipe_id].append({
            "ingredient": row['ingredient'].lower(),
            "family": row ['family'].lower(),
            "importance": row['importance'].lower(),
            "quantity": row['quantity'],
            "unit": row['unit'],
        })

#This is our new scoring mechanism.
#we're still trying to figure out the most sensible weights to use
#but this just weights the types of items, core, pantry, and optional
weights = {
    "core": 1.0,
    "optional": 0.5
}

#operationalizing our varibles and lists
best_recipe_id = None
best_score = 0
best_missing = []
best_substitutions = []


#for each recipe id,
for recipe_id in recipe_ingredients:
    total_score = 0
    earned_score = 0
    missing_ingredients = []
    substitutions = []

    #for each item in the recipe, get the info from the dictionary
    for item in recipe_ingredients[recipe_id]:
        ingredient = item['ingredient']
        family = item['family']
        importance = item['importance']

        #find how important this ingredient was
        weight = weights[importance]
        #add the total possible score for the recipe
        total_score += weight

        #if the ingredient is a match, then you add the full points
        if ingredient in user_ingredients:
            earned_score += weight
        #if the ingredient is in the same family, it gets similar points
        elif family in user_families:
            earned_score += weight * 0.6

            for user_ingredient in user_ingredients:
                if user_ingredient in ingredient_families and ingredient_families[user_ingredient] == family:
                    substitutions.append((user_ingredient, ingredient))
                    break

        #otherwise, the ingredient is missing
        else:
            missing_ingredients.append(ingredient)

    #calculate the final match score for the recipe
    recipe_score = earned_score / total_score * 100

    #if the recipe score is higher than the current best one
    if recipe_score > best_score:
        #then set the highest score to that recipe's score
        best_score = recipe_score
        #and the best recipe to that recipe, etc
        best_recipe_id = recipe_id
        best_missing = missing_ingredients
        best_substitutions = substitutions
        
    #this block is keeping track of the new best recipe

#now time to print the recipe
if best_recipe_id:
    #print the title of the recommended recipe, cuisine, and the rounded score
    print("\nRecommended recipe:", recipes[best_recipe_id]['name'])
    print("Cuisine:", recipes[best_recipe_id]['cuisine'])
    print("Match score:", round(best_score, 1), "%")

    #if there are substitutions, suggest them (still working on this)
    if best_substitutions:
        print("\nPossible substitutions:")
        for user_ingredient, recipe_ingredient in best_substitutions:
            print("-", "Use", user_ingredient, "instead of", recipe_ingredient)
       
    #print the missing ingredients
    if best_missing:
        print("\n You are missing:")
        for missing in best_missing:
            print("-", missing)

    #print the final ingredients and quantities
    for item in recipe_ingredients[best_recipe_id]:
        print("-", item["quantity"], item["unit"], item["ingredient"])

    #print the instructions - these will be longer for the final version
    print("\nInstructions:")
    print(recipes[best_recipe_id]["instructions"])

#if there are no recipes at all..
else:
    print("Sorry, none of your ingredients match the recipes in the cookbook. Time to go grocery shopping!")



'''
We've already noticed some things we will have to consider how to handle:
- Quantities of ingredients
- Variations of ingredients (i.e. if someone doesn't have san marzano tomatoes but has heirloom, they can still make the dish)
- Spelling variations (i.e. if they enter red pepper versus red pepper flakes)

Additional significant steps will include:
- Adding more recipes and being able to circulate through all ingredients
- Ranking and suggesting the recipes based on which ones have the highest percentage of matching ingredients
- Adding additional ranking criteria, i.e. cuisine, if they're in the mood for fish, pasta, salad, etc.
- For specialized recipes, asking if the user has specialized cooking equipment (i.e. immersion blender)
- Printing the recipe instructions

'''


#we will want to update sauce, family, etc
#also account for if the user types in spaghetti instead of pasta
