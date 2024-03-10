# new recipe

```shell
chef new recipe
```

The recipe wizard will guide you through creating a YAML recipe.
For example, to create a simple porridge recipe:

```shell
$ chef new recipe 
name: porridge
author: me
Ingredients:
format: [amount, [unit,]] name [; prep]
enter an ingredient [leave blank to finish]: 50, g, oats
enter an ingredient [leave blank to finish]: 100, ml, water
enter an ingredient [leave blank to finish]: brown sugar     
enter an ingredient [leave blank to finish]: 
Method:
enter a method step [leave blank to finish]: put the oats and water in the pan
enter a method step [leave blank to finish]: cook until bla 
enter a method step [leave blank to finish]: serve 
enter a method step [leave blank to finish]: 
Equipment:
what equipment do you need? [leave blank to finish]: small saucepan 
what equipment do you need? [leave blank to finish]: stove
what equipment do you need? [leave blank to finish]: 
prep_minutes (int) [0]: 1
cook_minutes (int) [0]: 5
servings (int) [0]: 1
source (url or book name): www.porridge.com
image (url or local image): porridge.jpg
notes: easy peasy 
Created recipe recipe-library/yaml/porridge.yaml
```

This will generate the following `porridge.yaml`:

```yaml
name: porridge
author: me
prep_minutes: 1
cook_minutes: 5
servings: 1
source: www.porridge.com
image: porridge.jpg
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

Once you understand the fields and syntax expected by the yaml format, you can also create the yaml files directly.

To read more about the YAML format [here](../recipe/yaml.md)