# yes-chef

A natural language command-line tool for managing recipes and making shopping lists.

## Installation

You can install `yes-chef` by cloning this repo and running the `install.sh` script. This will install the `chef`
command to your `~/.local/bin`. You may need to add this to your PATH variable to be able to run `chef` from anywhere.

## Quick start

In this section we'll walk through the minimum commands required to use `yes-chef`. For more detailed information on the available commands, see [commands](commands.md), or run

```shell
$ chef --help
```

### Creating a new recipe library

`yes-chef` needs a place to store recipe files. You can think of this as a git repository for your recipes. Create a new recipe library in the current directory by running:

```shell
$ chef init .
```

It is recommended to check your recipe folder into a public github repository; this way you can browse and view your recipes on your phone in the kitchen. For example, see [my recipe library](https://github.com/binnev/recipes).

### Adding a new recipe

Recipes are declared as YAML files. YAML is a simple human-readable data format that lends itself well to this task.
The recipe wizard will guide you through creating a yaml recipe.
For example, to create a simple porridge recipe:

```shell
$ chef new recipe
name: porridge
author: me
Ingredients:
format: [amount, [unit,]] name [; prep]
enter an ingredient [leave blank to finish]: 25, g, oats
enter an ingredient [leave blank to finish]: water
enter an ingredient [leave blank to finish]: 
Method:
enter a method step [leave blank to finish]: gently cook the oats. 
enter a method step [leave blank to finish]: 
Equipment:
what equipment do you need? [leave blank to finish]: pan 
what equipment do you need? [leave blank to finish]: 
prep_minutes (int) [0]: 
cook_minutes (int) [0]: 5
servings (int) [0]: 1
source (url or book name): 
image (url or local image): 
notes: 
Created recipe <recipe_library>/yaml/porridge.yaml
```

This will generate the following `porridge.yaml`:

```yaml
author: me
name: porridge
servings: 1
cook_minutes: 5
equipment:
  - pan
ingredients:
  - 25, g, oats
  - water
method:
  - gently cook the oats.
```

Once you understand the fields and syntax expected by the yaml format, you can also create the yaml files directly.
To read more about the ingredient syntax, see [ingredient syntax](ingredient.md)

## Exporting your YAML recipes to Markdown

To export your yaml recipes to a more readable markdown format, run

```shell
$ chef export
```

These markdown files can then be browsed on your phone in the kitchen.

## Planning meals and making a shopping list

One of the main features of `yes-chef` is its ability to create a shopping list for multiple recipes. Let's create a new plan with

```shell
$ chef new plan 
created new plan
```

A plan is just a collection of recipes for which we want to generate a shopping list.
Let's add our porridge recipe:

```shell
$ chef plan porridge
Added porridge by me to plan.
```

`yes-chef` searches your recipe library for "porridge", finds the porridge recipe, and adds it to the plan.
Now let's view the plan:

```shell
$ chef view plan 
Current plan:
    created: 2024-03-03T09:22:55.979689
    recipes:
        porridge by me
```

And we can view the shopping list by running

```shell
$ chef view list
Current shopping list:
oats: 25 g
water: enough for porridge
```

So far, so good. Now let's say we want to plan 2 days worth of porridge -- we can add porridge a second time:

```shell
$ chef plan porridge
Added porridge by me to plan.
```

Now our shopping list looks like this:

```shell
$ chef view list
Current shopping list:
oats: 50 g
water: enough for porridge (x2)
```

The amount of oats has doubled, and the entry for "water" has updated too, even though our porridge recipe doesn't specify an amount for water. 
This is a trivial example, but it really gets useful when we plan several large recipes. `yes-chef` will intelligently merge the ingredients lists.

If several recipes call for "fresh coriander" (no amount specified), this will be displayed like this, so that you know how much "fresh coriander" you need to buy: 

```
fresh coriander:                  
    enough for:
        Neelam Bajwa's chicken madras
        dhaal
```

`yes-chef` will try to sum amounts when it makes sense to do so. (Like in the porridge example above, it knows that `25g + 25g = 50g`). When the units differ, it will display the amounts organised by ingredient, so that you can quickly do the math yourself: 

```
garlic:                           
    3 cloves
    4 tsp
    1.0 bulb
```