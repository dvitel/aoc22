from bisect import insort
from collections import defaultdict
import re 

line_re = re.compile(r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$")
lines = open("d15.txt").read().splitlines()
pairs = [((int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))) for l in lines if (m := line_re.match(l)) ]

pairs_with_dist = [((s0, e0), (s1, e1), abs(s0 - s1) + abs(e0 - e1)) for (s0, e0), (s1, e1) in pairs]

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

def find_blocked(line_id):
    blocked_spans = sorted((x - (dist - dist0), x + (dist - dist0)) for (x, y), _, dist in pairs_with_dist for dist0 in [abs(y - line_id)] if dist >= dist0)
    blocked = [] if len(blocked_spans) == 0 else join_intervals([], blocked_spans[0][0], blocked_spans[0][1], blocked_spans[1:])
    return sum(e - s + 1 for s, e in blocked) - len({(x, y) for _, (x, y), _ in pairs_with_dist if y == line_id})

#part1 - second term excludes B on same row
# find_blocked(2000000)

max_v = 4000000

def diag_1(x, y):
    return x - y

def diag_2(x, y):
    return x + y - max_v

def to_x(d1, d2):
    return (d1 + d2 + max_v) / 2

def to_y(d1, d2):
    return (d2 - d1 + max_v) / 2

def disjoint_spans(s1, e1, s2, e2):
    if e1 < s2 or e2 < s1: 
        return [(s1, e1)]
    elif s1 < s2 <= e1 <= e2:
        return [(s1, s2 - 1)]
    elif s2 <= s1 <= e1 <= e2:
        return [] 
    elif s2 <= s1 <= e2 < e1:
        return [(e2 + 1, e1)] 
    elif s1 < s2 <= e2 < e1:
        return [(s1, s2 - 1), (e2 + 1, e1)]

def limit_span(s, e, d):
    if d < -max_v or d > max_v:
        return
    lim_v = max_v - abs(d)
    valid_min = -lim_v 
    valid_max = lim_v 
    if e < valid_min or s > valid_max:
        return None 
    elif s < valid_min <= e <= valid_max:
        return (valid_min, e)
    elif s < valid_min <= valid_max < e:
        return (valid_min, valid_max)
    elif valid_min <= s <= valid_max < e: 
        return (s, valid_max)
    elif valid_min <= s <= e <= valid_max:
        return (s, e)

def find_unblocked():
    def build_diag_1(delta):
        all_diag_1 = [((diag_1(x - d, y), diag_1(x, y - d)), (diag_2(x, y - d), diag_2(x + d, y)))
            for (x, y), _, d0 in pairs_with_dist 
            for d in [d0 + delta]]
        return all_diag_1

    acc = set()

    blocked = build_diag_1(0)
    poss = build_diag_1(1)

    dir1_spans = [(d, d2s, d2e) for s1, (d2s, d2e) in poss for d in s1]

    for d1, d2s, d2e in dir1_spans:
        if lim_span := limit_span(d2s, d2e, d1):
            d1_blocks = [(b2s, b2e) for ((b1s, b1e), (b2s, b2e)) in blocked if b1s <= d1 <= b1e]
            d1_spans = [lim_span]
            for bs, be in d1_blocks:
                d1_spans = [ r for d2s, d2e in d1_spans for r in disjoint_spans(d2s, d2e, bs, be)]
                if len(d1_spans) == 0:
                    break
            for d2s, d2e in d1_spans:
                for d2 in range(d2s, d2e + 1):
                    acc.add((to_x(d1, d2), to_y(d1, d2)))

    dir2_spans = [(d, d1s, d1e) for (d1s, d1e), s2 in poss for d in s2]

    for d2, d1s, d1e in dir2_spans:
        if lim_span := limit_span(d1s, d1e, d2):
            d2_blocks = [(b1s, b1e) for ((b1s, b1e), (b2s, b2e)) in blocked if b2s <= d2 <= b2e]
            d2_spans = [lim_span]
            for bs, be in d2_blocks:
                d2_spans = [ r for d1s, d1e in d2_spans for r in disjoint_spans(d1s, d1e, bs, be)]
                if len(d2_spans) == 0:
                    break    
            for d1s, d1e in d2_spans:
                for d1 in range(d1s, d1e + 1):
                    acc.add((to_x(d1, d2), to_y(d1, d2)))

    return acc

acc = find_unblocked()
min(x * 4000000 + y for x, y in acc)
