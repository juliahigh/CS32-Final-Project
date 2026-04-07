computer_ingredients = open('ingredients.csv')
matching_ingredients = 0
total_ingredients = 0
overlapping_ingredients = 0

print ("Welcome to the CS32 cookbook!\nYou tell us your ingredients, and we will recommend a recipe.")
input("Press enter to begin.")

user_ingredients = []
user_input = input("Please list up to 10 ingredients you have in your kitchen, separated by commas.")

for ingredient in user_input.split(","):
    user_ingredients.append(ingredient.strip().lower())

with open('txts/ingredients.csv') as computer_ingredients:
    recipe_ingredients = []
    for ingredient in computer_ingredients:
        recipe_ingredients.append(ingredient.strip().lower())

total_ingredients = len(recipe_ingredients)

for ingredient in recipe_ingredients:
    if ingredient in user_ingredients:
        matching_ingredients += 1

overlapping_ingredients = ((matching_ingredients/total_ingredients) * 100)
print ("You have" + str(overlapping_ingredients) + "% of the ingredients required to make this dish.")
