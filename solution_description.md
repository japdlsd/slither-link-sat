# first solution

TODO

### idea: 
How to control connectivity of all walls:
Each wall has a variable `reachable` with following rules:
````
reachable(wall) <- ~exists(wall)
reachable(wall) <- exists(wall), coincident(wall, neighbour), exists(neighbour), reachable(neighbour)
````
and one wall added as starting.
How to choose "first" wall? find first cell with number, and find first
existing wall ("choose north wall, if exists. If doesn't then choose east, If
both don't exist then choose south…").
-- This should suffice -- It's wrong. We should add time in this "DFS".
