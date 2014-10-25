## human-readable form:

problem instance is number grid RxC, therefore it's dot grid (R+1)x(C+1).

First line of solution contains positive integer N.

Next N lines contain 4 integers Xi, Yi, Xj, Yj (Xi, Xj in [0, R], Yi, Yj in [O,
C]), where ( Xi = Xj & |Yi - Yj| = 1 ) || ( |Xi - Xj| = 1 & Yi = Yj ). Each line 
descrirbes one wall of fence.

All N walls should create a single loop without self-crossings and branches.

## SAT-readable form (bijection between human-readable and Zn)

There are vertical and horisontal walls. Exact amount: (R+1) * (C) + (C+1) * (R) =: K.

