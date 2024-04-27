## 0.9.1 (2024-04-27)

### Fix

- included pyyaml in requirements

## 0.9.0 (2024-04-27)

### Feat

- **pipx**: added project.scripts entry so that users can install via pipx

## 0.8.2 (2024-04-27)

### Fix

- recipe wizard now strips trailing whitespace from input

## 0.8.1 (2024-04-03)

### Fix

- settings bug in export command

## 0.8.0 (2024-04-03)

### BREAKING CHANGE

- changes the values that can be set with `chef config`
- changed the default recipe library location

### Feat

- **cli**: added decorator to check recipe library is initialised.
- **settings**: renamed Settings.from_file() -> Settings.load()
- **settings**: split settings into system-wide and project-specific settings
- **settings**: added support for user settings

### Fix

- fixed settings bug when loading all recipes
- fixed a bug where an empty plan would not display properly
- **plan**: Plan.current was broken if no plans existed.
- **config**: config command now correctly handles passed values
- broken Plan.current
- settings loading doesn't break if the file doesn't exist

## 0.7.0 (2024-03-09)

### Feat

- shopping lists now convert units where possible
- added plural handling for units
- added support for normalising and converting units

### Fix

- added support for tsp / tbsp

## 0.6.1 (2024-03-03)

### Fix

- **readme-generation**: we now display author name in the recipe index

## 0.6.0 (2024-03-03)

### Feat

- added --version argument.

### Fix

- export now writes which version of yes-chef was used

## 0.5.0 (2024-03-03)

### Feat

- `chef export` now auto-generates an index of recipes in README.md

### Fix

- recipe list single spacing

## 0.4.1 (2024-03-03)

### Fix

- auto-capitalise items in markdown exports

## 0.4.0 (2024-03-02)

### Feat

- recipe wizard: interactive wizard that guides the user through creating a new recipe

## 0.3.0 (2024-02-26)

### Feat

- dummy change

## 0.2.0 (2024-02-26)

### Feat

- added CI workflows for main branch
