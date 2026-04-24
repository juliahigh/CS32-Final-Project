import csv

#introduce our recipe + ingredients files

matching_ingredients = 0

print ("Welcome to the CS32 cookbook!\nYou tell us your ingredients, and we will recommend a recipe.")
#enter to begin
input("Press enter to begin.")

#experimentation
#create this empty list of the user's ingredients
user_ingredients = []
user_input = input("Please list up to 10 ingredients you have in your kitchen, separated by commas: ")

#take the user's input and split it along the commas. for each of those ingredients...
for ingredient in user_input.split(","):
    #add to the list user_ingredients. and get rid of commas and lowercase everything so you don't have to deal with
    #confusing between upper and lowercase
    user_ingredients.append(ingredient.strip().lower())

#load ingredient families
ingredient_families = {}

with open('ingredients_families.csv') as family_file:
    #create another empty list, this time for the ingredients in the recipe
    reader = csv.DictReader(family_file)
    #for each line of our ingredients file
    for row in reader:
        ingredient_families[row['ingredient'].lower()] = row['family'].lower()

#find the user's ingredient families
user_families = []

for ingredient in user_ingredients:
    if ingredient in ingredient_families:
        user_families.append(ingredient_families[ingredient])
    else:
        user_families.append(ingredient)

#load up the recipes
recipes = {}

with open ("recipes.csv") as recipe_file:
    reader = csv.DictReader(recipe_file)
    for row in reader:
        recipes[row['recipe_id']] = {
            "name": row['name'],
            "cuisine": row['cuisine'],
            "instructions": row['instructions'],
        }

#load the recipe ingredients
recipe_ingredients = {}

with open("recipe_ingredients.csv") as ingredient_file:
    reader = csv.DictReader(ingredient_file)
    for row in reader:
        if row['recipe_id'] not in recipe_ingredients:
            recipe_ingredients[row['recipe_id']] = []
        recipe_ingredients[recipe_id].append({
            "ingredient": row['ingredient'].lower(),
            "family": row ['family'].lower(),
            "importance": row['importance'].lower(),
            "quantity": row['quantity'],
            "unit": row['unit'],
        })

#new scoring mechanism
weights = {
    "core": 1.0,
    "pantry": 0.5,
    "optional": 0.25
}

best_recipe_id = None
best_score = 0
best_missing = []
best_substitutions = []

for recipe_id in recipe_ingredients:
    total_score = 0
    earned_score = 0
    missing_ingredients = []
    substitutions = []

    for item in recipe_ingredients[recipe_id]:
        ingredient = item['ingredient']
        family = item['family']
        importance = item['importance']
        
        weight = weights[importance]
        total_score += weight

        if ingredient in user_ingredients:
            earned_score += weight
        elif family in user_families:
            earned_score += weight * 0.7
            substitutions.appent(ingredient)

        else:
            missing_ingredients.append(ingredient)
    
recipe_score = earned_score / total_score * 100

if recipe_score > best_score:
    best_score = recipe_score
    best_recipe_id = recipe_id
    best_missing = missing_ingredients
    best_substitutions = substitutions

#now time to print the recipe

if best_recipe_id is not None:
    print("\nRecommended recipe:", recipes[best_recipe_id]['name'])

#the total number of ingredients is the number of ingredients in the recipe
total_ingredients = len(recipe_ingredients)

#create an empty list for any missing ingredients
missing_ingredients = []

for ingredient in recipe_ingredients:
    if ingredient in user_ingredients:
        #if the ingredient from the recipe is in the user's list, add 1 to the matching ingredients number
        matching_ingredients += 1
        #otherwise, add to the missing ingredient's list
    else:
        missing_ingredients.append(ingredient)

#the overlapping ingredients are the percentage
overlapping_ingredients = ((matching_ingredients/total_ingredients) * 100)
#print what % of the ingredients required to make this dish
print ("You have " + str(overlapping_ingredients) + "% of the ingredients required to make this dish.")
#print which ingredients they're missing
print("You are missing:", missing_ingredients)
#if you don't have any of the necessary ingredients...
if total_ingredients == 0:
    print("Recipe has no ingredients listed. Time to go grocery shopping!")

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
