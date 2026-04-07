#grab our ingredients csv file
computer_ingredients = open('ingredients.csv')

#operationalize all variables
matching_ingredients = 0
total_ingredients = 0
overlapping_ingredients = 0

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

with open('ingredients.csv') as computer_ingredients:
    #create another empty list, this time for the ingredients in the recipe
    recipe_ingredients = []
    #for each line of our ingredients file
    for ingredient in computer_ingredients:
        #add to the actual recipes ingredients
        recipe_ingredients.append(ingredient.strip().lower())

#the total number of ingredients is the number of ingredients in the recipe
total_ingredients = len(recipe_ingredients)


for ingredient in recipe_ingredients:
    if ingredient in user_ingredients:
        matching_ingredients += 1

overlapping_ingredients = ((matching_ingredients/total_ingredients) * 100)
print ("You have " + str(overlapping_ingredients) + "% of the ingredients required to make this dish.")
