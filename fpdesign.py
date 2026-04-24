RAUL IS RIGHT HERE

matching_ingredients = 0

print ("Welcome to the CS32 cookbook!\nYou tell us your ingredients, and we will recommend a recipe.")
#enter to begin
input("Press enter to begin.")

#create this empty list of the user's ingredients
user_ingredients = []
user_input = input("Please list up to 10 ingredients you have in your kitchen, separated by commas: ")

#take the user's input and split it along the commas. for each of those ingredients...
for ingredient in user_input.split(","):
    #add to the list user_ingredients. and get rid of commas and lowercase everything so you don't have to deal with
    #confusing between upper and lowercase
    user_ingredients.append(ingredient.strip().lower())

with open('ingredients.csv') as ingredient_file:
    #create another empty list, this time for the ingredients in the recipe
    recipe_ingredients = []
    #for each line of our ingredients file
    for ingredient in ingredient_file:
        #add to the actual recipes ingredients
        recipe_ingredients.append(ingredient.strip().lower())

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
We've already noticed some things we will have to consider how to handle: RAUL
- Quantities of ingredients
- Variations of ingredients (i.e. if someone doesn't have san marzano tomatoes but has heirloom, they can still make the dish)
- Spelling variations (i.e. if they enter red pepper versus red pepper flakes)

Additional significant steps will include: JULIA
- Adding more recipes and being able to circulate through all ingredients
- Ranking and suggesting the recipes based on which ones have the highest percentage of matching ingredients
- Adding additional ranking criteria, i.e. cuisine, if they're in the mood for fish, pasta, salad, etc.
- For specialized recipes, asking if the user has specialized cooking equipment (i.e. immersion blender)
- Printing the recipe instructions

'''
