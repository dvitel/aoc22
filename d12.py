from collections import deque

lines = open("d12.txt").read().splitlines()
idx_of = lambda ch: next((i + 1, l.index(ch) + 1) for i, l in enumerate(lines)) #+1 for sentinels
start = idx_of('S')
end = idx_of('E')
m_val = -255
sentinel_line = [m_val for _ in range(len(lines[0]) + 2)]
grid = [sentinel_line, 
        *[[m_val, *[ord('a') if ch == 'S' else (ord('z'), 0) if ch == 'E' else ord(ch) for ch in l], m_val] 
            for l in lines],
        sentinel_line]

q = deque([end])

def try_next(i, j, prev_v, prev_s, q):
    v = grid[i][j]
    if type(v) != tuple and prev_v - v <= 1: 
        grid[i][j] = (v, prev_s + 1)
        q.append((i, j))

while len(q) > 0:
    i, j = q.popleft() 
    prev_v, prev_s = grid[i][j]
    try_next(i - 1, j, prev_v, prev_s, q)
    try_next(i + 1, j, prev_v, prev_s, q)
    try_next(i, j - 1, prev_v, prev_s, q)
    try_next(i, j + 1, prev_v, prev_s, q)    

grid[start[0]][start[1]]
#part 2
min(v[1] for r in grid for v in r if type(v) == tuple and v[0] == ord('a'))
