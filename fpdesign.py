ingredients = open('txts/ingredients.csv')
matching_ingredients = 0
total_ingredients = 0
print ("Welcome to the CS32 cookbook!\nYou tell us your ingredients, and we will recommend a recipe.\nPress Enter to begin.")
#require an enter to begin
user_ingredients = input("Please list 10 ingredients you have in your kitchen, separated by commas.")
#Otherwise prompt an error message, "please enter your ingredients separated by commas"
ingredients.split(",")

#put the ingredients into a list. update the list for each element of the split
#for each line in ingredients
#if user input matches ingredients
#update some variable
#percentage of ingredients matched = some variable / total ingredients in recipe
#print percentage of ingredients matched

while True:
    ingredients_line = ingredients.readline()
    for ingredient in ingredients:
        if user_ingredients == ingredient:
            matching_ingredients += 1
        else:
            break

#print matching ingredients / total ingredients
