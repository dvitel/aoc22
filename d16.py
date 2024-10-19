from collections import deque
import math
import random
import re 
lines = open("d16.txt").read().splitlines()
line_re = re.compile(r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves?\s(.+)$")
caves = {cid: (int(v), [el.strip() for el in next_ids.split(',')], {})  #last one is time necessary to reach corresponding cave
            for l in lines for m in [line_re.match(l)] 
            for (cid, v, next_ids) in [m.groups()]}

def released_preassure(d):
    return sum(caves[cid][0] * (t[1] if type(t) is tuple else t) for cid, t in d.items())

#shortest paths
for cid, (_, next_cids, times) in caves.items():
    times[cid] = 0
    q = deque((cid, next_cid) for next_cid in next_cids)
    while len(q) > 0: 
        cid, next_cid = q.popleft()
        times[next_cid] = times[cid] + 1
        for next_next_cid in caves[next_cid][1]:
            if next_next_cid not in times:
                q.append((next_cid, next_next_cid))

valuable_caves = {cid for cid, (v, _, _) in caves.items() if v > 0}

def walk_caves(acc, valuable_caves, cur_cave_id, t):
    global i
    paths = caves[cur_cave_id][2]
    valuable_caves_here = [(cid, useful_time) for cid in valuable_caves 
                            if cid in paths #and len(set.intersection(paths[cid] - {cid}, valuable_caves)) == 0 
                            for useful_time in [(t - paths[cid]) - 1] if useful_time > 0]
    if len(valuable_caves_here) == 0:
        return acc, released_preassure(acc) 
    res = max((walk_caves({cid: t, **acc}, valuable_caves - {cid}, cid, t) for cid, t in valuable_caves_here), key = lambda x:x[1])
    return res

# walk_caves({}, valuable_caves, 'AA', 30)
# released_preassure(res2)

# def walk_caves2(acc, acc_res, valuable_caves, cur_cave_ids, best_walk_so_far, best_walk_so_far_res):    
#     valuable_caves_here = [(eid, cid, useful_time) for cid in valuable_caves 
#                             for eid, (cur_cave_id, t) in cur_cave_ids.items()
#                             for paths in [caves[cur_cave_id][2]] 
#                             if cid in paths
#                             for useful_time in [(t - paths[cid]) - 1] if useful_time > 0]
#     if len(valuable_caves_here) == 0:
#         return (acc, acc_res) if acc_res >= best_walk_so_far_res else (best_walk_so_far, best_walk_so_far_res)
#     valuable_caves_here_grouped = {}
#     for eid, cid, useful_time in valuable_caves_here:
#         valuable_caves_here_grouped.setdefault(cid, []).append((eid, useful_time))
#     valuable_caves_here_grouped_max = {cid:(mv[0], mv[1], mv[1] * caves[cid][0]) for cid, times in valuable_caves_here_grouped.items() for mv in [max(times, key = lambda x: x[1])]}
#     sorted_valuable_caves_here_grouped_max = sorted(valuable_caves_here_grouped_max.items(), key=lambda x: -x[1][2])
#     for cid, (eid, t, preassure) in sorted_valuable_caves_here_grouped_max:
#         new_acc = {cid: (eid, t), **acc}
#         new_acc_res = acc_res + preassure
#         left_pressure = max(0, best_walk_so_far_res - new_acc_res) #left pressure to overcome best result
#         new_cur_cave_ids = {**cur_cave_ids, eid: (cid, t)}
#         new_valuable_caves = valuable_caves - {cid}
#         if len(new_valuable_caves) > 0:
#             avg_expected_valve = left_pressure / (max(t for (_, t) in new_cur_cave_ids.values()) * len(new_valuable_caves))
#             if all(caves[cid][0] < avg_expected_valve for cid in new_valuable_caves):
#                 # print("Canceling", new_valuable_caves, "avg expected: ", avg_expected_valve, "acc", new_acc)
#                 continue 
#         best_walk_so_far, best_walk_so_far_res = walk_caves2(new_acc, new_acc_res, new_valuable_caves, new_cur_cave_ids, best_walk_so_far, best_walk_so_far_res)
#     return (best_walk_so_far, best_walk_so_far_res)

valuable_caves_list = list(valuable_caves)
valuable_caves_split = [random.randint(0, 1) for _ in valuable_caves_list] #0 - me, 1 - elephant 

def tweak_cave_splits(valuable_caves_split):
    at_pos = random.randrange(0, len(valuable_caves_split))
    res = [1 - f if i == at_pos else f for i, f in enumerate(valuable_caves_split)]
    return res 

def fitness(valuable_caves_split):
    my_caves = {valuable_caves_list[i] for i, f in enumerate(valuable_caves_split) if f == 0}
    elephant_caves = {valuable_caves_list[i] for i, f in enumerate(valuable_caves_split) if f == 1}
    _, my_pressure = walk_caves({}, my_caves, 'AA', 26)
    _, elephant_pressure = walk_caves({}, elephant_caves, 'AA', 26)
    return my_pressure + elephant_pressure

t = 1000 #temperature - we use annealing 
cur_fitness = fitness(valuable_caves_split)
best_split = valuable_caves_split
best_split_fitness = cur_fitness
while t > 0: 
    child_split = tweak_cave_splits(valuable_caves_split)
    child_fitness = fitness(child_split)
    fitness_distance = child_fitness - cur_fitness
    if fitness_distance > 0 or random.random() < math.exp(fitness_distance / t):
        valuable_caves_split = child_split
        cur_fitness = child_fitness
    t -= 1 
    if cur_fitness > best_split_fitness:
        best_split = valuable_caves_split
        best_split_fitness = cur_fitness




# res = walk_caves2({}, 0, valuable_caves, {'Me': ('AA', 26), 'Elephant': ("AA", 26)}, None, 0)
# print(res)