create new plan (wipes old plan)
```shell
sous-chef new plan 
```

plan recipe (adds it to the list)
```shell
sous-chef plan <search term> 
```

show which recipes (titles only) are in the shopping list
```shell
sous-chef view plan
```

show the merged shopping list
```shell
sous-chef view list
```

create new recipe (wizard that guides you through it)
```shell
sous-chef new recipe 
```

view configuration 
```shell
sous-chef config list
```

update configuration 
```shell
sous-chef config set --key value 
```

# TODO: 

```shell
sous-chef new alias "ground cumin" "cumin powder"
```

```shell
sous-chef new category poultry 
sous-chef categorise chicken poultry
```



This is a more natural language style:
- sous-chef 
  - init <setup wizard for recipes folder etc> 
  - new 
    - plan
    - recipe <wizard> 
  - plan <search>
  - view
    - plan
    - list
    - config
  - config <args>

This is a more tree-based approach: 
- sous-chef
  - init <setup wizard for recipes folder etc> 
  - plan
    - new
    - recipe <search> 
    - view
    - list
  - recipe <wizard>
  - config
    - view
    - set

| action                              | natural language | tree-based           | 
|-------------------------------------|------------------|----------------------|
| create new plan (wipe old)          | new plan         | plan new             |
| add recipe to plan                  | plan <search>    | plan recipe <search> |
| view recipes in plan                | view plan        | plan view            |
| view merged shopping list           | view list        | plan list            |
|                                     |                  |                      |
| create new recipe (wizard)          | new recipe       | recipe               |
|                                     |                  |                      |
| update settings (also shows config) | config <args>    | config <args>        |
|                                     |                  |                      |
|                                     |                  |                      |
|                                     |                  |                      |
|                                     |                  |                      |
|                                     |                  |                      |
|                                     |                  |                      |

