class function2(function):
    
L = lambda i, j: (i, j - 1)
R = lambda i, j: (i, j + 1)
U = lambda i, j: (i + 1, j)
D = lambda i, j: (i - 1, j)

lines = open("d9.txt").read().splitlines()
funcs = [(eval(l[0]), int(l[2:])) for l in lines ]
poss = set() 
H = T = (0, 0)
for move, n in funcs: 
    for i in range(n):
        H = move(*H)
        d = [h - t for h, t in zip(H, T)]
        