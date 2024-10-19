from bisect import insort
from collections import deque

lines = open("d18.txt").read().splitlines()
cubes = {tuple(int(x) for x in line.split(',')) for line in lines}

def free_cubes():
    res = {(cube, free_cube) for cube in cubes 
        for dim_id in range(3)
        for free_cube in [tuple(coord - 1 if i == dim_id else coord for i, coord in enumerate(cube)), 
                            tuple(coord + 1 if i == dim_id else coord for i, coord in enumerate(cube))] 
        if free_cube not in cubes}
    return res 

all_free_surfaces = free_cubes()
len(all_free_surfaces)

mins, maxs = tuple(zip(*[(mi, ma) for dim_id in range(3) for mi in [min(cube[dim_id] for cube in cubes) - 1] for ma in [max(cube[dim_id] for cube in cubes) + 1]]))
q = deque([mins]) #water spread, mins not in cubes
water = set([mins])
while len(q) > 0:
    w = q.popleft()
    dirs = [tuple(delta if dim_id0 == dim_id else 0 for dim_id0 in range(3)) for dim_id in range(3) for delta in [-1,1]]
    new_ws = [new_w for d in dirs for new_w in [tuple(a + b for a, b in zip(d, w))] 
                if new_w not in cubes and new_w not in water and all(a <= b <= c for a, b, c in zip(mins, new_w, maxs))]
    water.update(new_ws)
    q.extend(new_ws)

outer_surfaces = [(cube, free_cube) for cube, free_cube in all_free_surfaces if free_cube in water]
len(outer_surfaces)