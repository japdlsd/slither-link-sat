# ~~version 0~~ 
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
~~This should suffice~~ It's wrong. We should add time in this "DFS".

# version 1
## Number of walls
`exactly zero`, `exactly one`, `exactly two`, `exactly three`, `exactly four`

```
exactly zero:
~a & ~b & ~c & ~d
```

```
at least one:
(a || b || c || d)
```

```
at most one:
( a -> ~b & ~c & ~d ) & (b -> ~a & ~c & ~d) & ...
(~a || ~b & ~c & ~d) & (~b || ~a & ~c & ~d) & ...
(~a || ~b) & (~a || ~c) & (~a || ~d) & ...  
```

```
at least two:
at least one && (a -> (b || c || d)) && (b -> (a || c || d)) && (c -> (a || b || d)) && (d -> (a || b || c))
```

```
at most two:
(a & b -> ~c & ~d) & (a & c -> ~b & ~d) & ...
(~a || ~b) || (~c & ~d) = (~a || ~b || ~c) & (~a || ~b || ~d)
```

```
at most three:
(~a || ~b || ~c || ~d)
```

```
exactly four
a & b & c & d
```
## Connectivity
> Each end of each wall is coincident with one other wall.

## One loop
> There must be only one loop, so all wall must be connected.

`reachable(wall, time)` (`time` from `0` to `R*C =: final_time`)

choose starting walls (one of four, call them `west_wall`, `south_wall`, etc.):
```
starting_west <-> west_wall
starting_south <-> ~west_wall & south_wall
starting_east <-> ~west_wall & ~south_wall & east_wall
starting_north <-> ~west_wall & ~south_wall & ~east_wall & north_wall 

reachable(west_wall, 0) <-> starting_west
...
reachable(north_wall, 0) <-> starting_north

// remaining walls
for each wall not in (possible_starts):
  ~reachable(wall, 0)
  reachable(wall, final) <-> exists(wall)

for each wall:
  for each time:
    reachable(wall, time) <->  exists(wall) & 
          ( OR{ reachable(x, time-1) | x in susedia(wall)} || reachable(wall, time-1) )
```

## CNF form of logic expressions used in solution
```
a & b
// CNF form
a
b
```

```
a -> b
// CNF form
~a || b
```

```
a <-> b
// CNF form
~a || b
~b || a
```

```
a -> (b1 || b2 || b3 || ...)
// CNF form
~a || b1 || b2 || b3 || ...
```

```
a <- (b1 || b2 || b3 || ...)
~(b1 || ...) || a
(~b1 & ~b2 & ...) || a
(~b1 || a) & (~b2 || a) & ...
// CNF form
~b1 || a
~b2 || a
...
```

```
a -> (b1 & b2 & b3 & ...)
~a || (b1 & b2 & ...)
(~a || b1) & (~a || b2) & ...
// CNF form
(~a || b1)
(~a || b2)
...
```

```
a <- (b1 & b2 & ...)
~(b1 & b2 & ...) || a
(~b1 || ~b2 || ...) || a
// CNF form
a || ~b1 || ~b2 || ...
```
