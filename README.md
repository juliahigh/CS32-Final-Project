# Final Project CS32 Cookbook!

Authors: Julia High and Raul Ontiveros

## Project Overview: 
We have created a recipe recommendation tool that suggests a recipe to a user based on their available ingredients and cuisine preferences. Our program contains a collection of 100 recipes across several different cuisines.

We started the project in fpdesign.py, a file we ran in the Python terminal. After receiving a suggestion from our mentor, we switched our program to run on a local web server using Flask.

Happy cooking!

## How to Run the Program:
1. Run newfileflask.py in the Python terminal
2. Select "Open in Browser" from the popup
3. Type in your ingredients
4. Type in your cuisine
5. Select find recipe
6. Then you should see a recipe with a match score, possible substitutions, and instructions. Bon appetit!

## Key Files:
* newfileflask.py - Runs our program on the local html site.
* allingredients.csv - Contains all ingredients across 100 recipes. 
* allrecipes.csv - Contains all recipes, cuisines, and instructions.
* ingredientfamilies.csv - Contains substitution options for several different ingredients.
* fpdesign.py - Our original program that works in the Python terminal.

## External Contributors:
Since we wanted to have a large collection of recipes, we used ChatGPT to help create the .csv files. We also used it to help us with the Flask formatting and implementation.