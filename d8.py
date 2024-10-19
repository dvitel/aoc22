lines = open("d8.txt").read().splitlines()
grid = [[int(t) for t in l] for l in lines]
gridT = [[r[j] for r in grid] for j in range(len(grid[0]))]

visible = set()

def watch(grid, rev=False):
    for i, r in enumerate(grid):
        visible.update((j, i, t) if rev else (i,j,t) for j, t in enumerate(r) if all(t0 < t for t0 in r[0:j]))

    #right
    for i, r in enumerate(grid):
        visible.update((j, i, t) if rev else (i,j,t) for j, t in enumerate(r) if all(t0 < t for t0 in r[j+1:]))    

watch(grid)
watch(gridT, rev=True)

#part1
len(visible)

def watch_from_tree(i, j, t, grid, left=True):
    for t0 in reversed(grid[i][:j]) if left else grid[i][j+1:]:
        if t0 <= t:
            yield t0 
        if t0 >= t:
            break
    
def f(*args):
    return len(list(watch_from_tree(*args)))

#part2
sorted([f(i, j, t, grid) * 
    f(i, j, t, grid, False) *
    f(j, i, t, gridT) *
    f(j, i, t, gridT, False) for i, j, t in sorted(visible, key=lambda x:-x[2])], key = lambda x:-x)[0]
