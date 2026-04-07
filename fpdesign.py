computer_ingredients = open('txts/ingredients.csv')
matching_ingredients = 0
total_ingredients = 0
overlapping_ingredients = 0
print ("Welcome to the CS32 cookbook!\nYou tell us your ingredients, and we will recommend a recipe.\nPress Enter to begin.")
#require an enter to begin
user_ingredients = []
user_input = i input("Please list 10 ingredients you have in your kitchen, separated by commas.")

for ingredient in user_input.split(","):
    user_ingredients.append(ingredient.strip())
total_ingredients = len(computer_ingredients)
#Otherwise prompt an error message, "please enter your ingredients separated by commas"


#put the ingredients into a list. update the list for each element of the split
#for each line in ingredients
#if user input matches ingredients
#update some variable
#percentage of ingredients matched = some variable / total ingredients in recipe
#print percentage of ingredients matched

ingredients_line = computer_ingredients.readline()
for ingredient in computer_ingredients:
    if ingredient in user_ingredients:
        matching_ingredients += 1
    else:
        break
overlapping_ingredients = ((matching_ingredients/total_ingredients) * 100)
print ("You have" + str(overlapping_ingredients) + "% of the ingredients required to make this dish.")

#print matching ingredients / total ingredients
