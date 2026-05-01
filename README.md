# CS32-Final-Project

This is Julia High and Raul Ontiveros' CS32 final project repository.

FP Status Updates:

We've reworked our program so that it includes 10 recipes. We will continue expanding the number of recipes for the final submission.

We've included several new files:
allrecipes.csv - this has the recipe name/id, cuisine, and instructions
allingredients.csv - this has the ingredients and the associated info (i.e. family)
ingredientfamilies.csv - this allows for substitutes, still working on this

Right now, our program still recommends the user a recipe based on the ingredients that they have inputted. Instead of ranking the recipes, we decided to suggest the single best recipe. We may rank them later on.

The best recipe is decided based on several factors. For one, we have added a new file called ingredientfamilies.csv so that the user can account for substitutions. i.e. there are several tomato varieties. This part still needs some work for the final version, of course, because right now ingredients like soy sauce and salsa would be considered the same family.

The ingredients are also ranked based on importance. For example, there are the core ingredients and then there are the pantry ingredients. The pantry ingredients are ones we assume that any home chef has, so they aren't as critical as the fundamental ingredients that someone might have to go to the store for.

Substitute ingredients are given less points, and missing ingredients reduce points.

The program then recommends the highest scoring recipe. We are still rethinking our weights though. While the recipe recommendations are valid given our weights, they aren't the most intuitive.

We used ChatGPT to create the .csv files and to help us format newfileflask.py. We will use more sophisticated recipe instructions for our final submission, but for now we were focused on functionality more than the actual recipes.




---

For our final project, we want to write a cookbook (or accomplish one element of writing a cookbook).

We want to suggest recipes for a user to make based on ingredients that they have. We may have a pre-set list of recipes (fish, salads, pastas, baked goods, etc) that our program will pull from.

There may be the option for the user to input if they have any specialty equipment (i.e. food processor, electric mixer, precision cooker, etc) that would also help narrow down which recipes they should tackle.

Ultimately, the program will match the user with the best recipe based on something like the percentage of ingredients they have to complete it, or something along those lines.
