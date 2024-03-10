# plan recipe 

```shell
chef plan <QUERY>
```

`yes-chef` searches your recipe library for recipes matching the query. If it finds multiple matches, it will prompt you to choose one:  

```shell
$ chef plan madras
[?] Which recipe did you mean?: 
 > Chicken madras
   lamb pork or beef madras
   chicken madras curryhouse style

Added Chicken madras by Neelam Bajwa to plan. Plan is now: 
Plan (created at 2024-03-10 14:08:41.158247)
```

If it finds only one match, it skips the prompt: 

```shell
$ chef plan porridge
Added porridge by me to plan. Plan is now: 
Plan (created at 2024-03-10 14:08:41.158247)
```

If it finds no matches, it exits with an error: 


```shell
$ chef plan foobar
Couldn't find any recipes for foobar
```