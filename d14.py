from collections import defaultdict
from bisect import insort
import sys

lines = open("d14.txt").read().splitlines()
coords = [[tuple(int(el) for el in pair.split(",")) for pair in line.split(" -> ")] for line in lines]

start_rocks_row_spans_d = defaultdict(list)

# coords.append([(450, 166), (550, 166)])
for l in coords:
    for (c0, r0), (c1, r1) in zip(l, l[1:]):
        # print(f"{(c0, r0)} -> {(c1, r1)}")
        assert c0 == c1 or r0 == r1
        if r0 == r1:
            insort(start_rocks_row_spans_d[r0], (min(c0, c1), max(c0, c1)))
        elif c0 == c1:
            for r in range(min(r0, r1), max(r0, r1) + 1):
                insort(start_rocks_row_spans_d[r], (c0, c0))

rocks_row_spans = sorted(start_rocks_row_spans_d.items(), key=lambda x: x[0])

max_r = max(rid for rid, _ in rocks_row_spans)
min_c = min(spans[0][0] for _, spans in rocks_row_spans)
max_c = max(spans[-1][1] for _, spans in rocks_row_spans)

rocks_row_spans.append((max_r + 2, [(min_c - 400, max_c + 400)]))

max_r += 2 
min_c -= 400
max_c += 400

draw_i = 0
def draw(rocks_row_spans, sand, trace):
    global draw_i
    grid = [['.' for c in range(min_c - 1, max_c + 2)] for r in range(max_r + 1)]

    def set_grid(r, c, v):
        j = c - min_c + 1
        assert grid[r][j] == '.' or grid[r][j] == v, f'Grid is {grid[r][j]} at ({r}, {c}/{j}), setting to {v}'
        grid[r][j] = v

    for r, spans in rocks_row_spans:
        for s, e in spans:
            for c in range(s, e + 1):
                set_grid(r, c, '#')

    for r, c in sand:
        set_grid(r, c, 'o')
    
    for r, c in trace:
        if (r, c) not in sand:
            set_grid(r, c, '~')

    grid_str = "\n".join(["".join(r) for r in grid])
    # with open(f"d14/d{draw_i}.txt", 'w') as f:
    f = sys.stdout
    print(file = f)
    print(file = f)
    print(''.join([' ' if c != 500 else '*' for c in range(min_c - 1, max_c + 2)]), file = f)            
    print(grid_str, file = f)
    draw_i += 1

# draw(rocks_row_spans, {}, {})

def join_intervals(acc, s, e, intervals):
    if len(intervals) == 0: 
        acc.append((s, e))
        return acc 
    else:
        s0, e0 = intervals.pop(0)
        if s <= s0 <= (e + 1):
            s0 = s 
            e0 = max(e, e0)
        else:
            acc.append((s, e))
        return join_intervals(acc, s0, e0, intervals)

rocks_row_spans = [(rid, join_intervals([], spans[0][0], spans[0][1], spans[1:])) for rid, spans in rocks_row_spans]

# grid = [['.' for c in range(min_c - 1, max_c + 2)] for r in range(max_r + 1)]
# def to_j(c):
#     return c - min_c + 1
    
# for r, spans in rocks_row_spans:
#     for s, e in spans:
#         for c in range(s, e + 1):
#             grid[r][to_j(c)] = '#'

# def sand_fall2():
#     i, j = 0, to_j(500)
#     acc = set()
#     grid[i][j] = 'o'
#     # while i + 1 < len(grid): 
#     while True: 
#         poss = [(i + 1, j), (i + 1, j - 1), (i + 1, j + 1)]
#         if (res := next(((i0, j0) for i0, j0 in poss if grid[i0][j0] == '.'), None)) is not None:
#             grid[i][j] = '.'
#             grid[res[0]][res[1]] = 'o'
#             i, j = res
#         else:            
#             acc.add((i, j))
#             if i == 0 and j == 500:
#                 break
#             i, j = 0, to_j(500)
#             grid[i][j] = 'o'    
#     grid[i][j] = '.'
#     draw2()
#     return acc        

# def draw2():
#     # with open(f"d14/d{draw_i}.txt", 'w') as f:
#     f = sys.stdout
#     print(file = f)
#     print(file = f)
#     # print(''.join([' ' if c != 500 else '*' for c in range(min_c - 1, max_c + 2)]), file = f)   
#     grid_str = "\n".join(["".join(r) for r in grid])         
#     print(grid_str, file = f)

# sand = sand_fall2()

def shift_at(row, col, row_spans):      
    def check_candidate(new_row, new_col):
        neg_row_cond = len(row_spans) > 0 \
                        and row_spans[0][0] == new_row \
                        and any(s <= new_col <= e for s, e in row_spans[0][1])
        return None if neg_row_cond else (new_row, new_col)
    return check_candidate(row + 1, col - 1) or check_candidate(row + 1, col + 1)

def sand_fall():
    row, col = 0, 500
    acc = set()
    landing_row = 0
    g_row_spans = list(rocks_row_spans) 
    row_spans = list(g_row_spans)
    trace = set()
    while landing_row is not None: 
        landing_row = None
        while len(row_spans) > 0:
            rid, col_spans = row_spans[0]
            if next(((s, e) for s, e in col_spans if s <= col <= e), None): 
                landing_row = rid
                break 
            else:
                row_spans.pop(0)
        if landing_row is not None:
            new_row = landing_row - 1
            for r in range(row, new_row + 1):
                trace.add((r, col))
            if (res := shift_at(new_row, col, row_spans)) is not None:
                row, col = res 
            else:      
                assert (new_row, col) not in acc
                acc.add((new_row, col))    
                if new_row == 0:
                    break
                if (rid_id := next((i for i, (rid, _) in enumerate(g_row_spans) if rid == new_row), None)) is not None:
                    l = list(g_row_spans[rid_id][1])
                    insort(l, (col, col))                    
                    g_row_spans[rid_id] = (new_row, join_intervals([], l[0][0], l[0][1], l[1:]))
                else:
                    insort(g_row_spans, (new_row, [(col, col)]))               
                row_spans = list(g_row_spans)
                row, col = 0, 500 
                # draw(rocks_row_spans, acc, trace)
                trace = set()
    for r in range(row, max_r + 1):
        trace.add((r, col))    
    # draw(rocks_row_spans, acc, trace)
    return acc

sand = sand_fall()