# YAML recipe format

Recipes are stored as YAML files. YAML is a machine readable data format that is also very human readable, with minimal syntax. This makes it an excellent way to declare non-technical things like recipes, while still allowing them to be machine-readable.

## Recipe syntax 

The only required fields in a recipe are `name` and `ingredients`. This is a minimal example recipe: 

```yaml
name: porridge
ingredients:
  - 50, g, oats
  - water
```

and this is the same recipe, but with all the optional fields populated: 

```yaml
name: porridge
author: me
prep_minutes: 1
cook_minutes: 5
servings: 1
source: www.porridge.com
image: porridge.jpg  # this file must exist in the /images folder
notes: easy peasy
equipment:
  - small saucepan
  - stove
ingredients:
  - 50, g, oats
  - 100, ml, water
  - brown sugar
method:
  - put the oats and water in the pan
  - cook until the desired thickness is reached
  - serve with some brown sugar to taste
```

## Ingredient syntax

`Ingredient` has 4 fields:

- name (required)
- amount (optional)
- unit (optional)
- prep (optional)

To preserve the natural-language feel of the input files, We use a custom syntax to declare ingredients. Commas separate the amount, units, and name of the ingredient.

The following examples are valid:

```yaml
ingredients:
  - apples         # amountless
  - 2, apples      # unitless
  - 2, kg, apples  # with units 
```

and all variants can have the optional prep instructions separated by a semicolon:

```yaml
ingredients:
  - apples; chopped
  - 2, apples; chopped
  - 2, kg, apples; chopped
```

Writing this with correct YAML syntax would produce very verbose input files:

```
ingredients:
  - apples:       # amountless
    amount: None
    units: None    
  - apples:       # unitless
    amount: 2
    units: None
  - apples:       # with units 
    amount: 2
    units: kg
```