from collections import deque
from dataclasses import dataclass
from math import ceil
import math
import random
import re 
lines = open("d19.txt").read().splitlines()
line_re = re.compile(r"^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
# ore, clay, obs, geo = "ore", "clay", "obs", "geo"
# zero = (0, 0, 0, 0) #{ore:0, clay:0, obs:0, geo:0}
bps = {int(m.group(1)): ((0, int(m.group(7)), 0, int(m.group(6))),
                         (0, 0, int(m.group(5)), int(m.group(4))),
                         (0, 0, 0, int(m.group(3))),
                         (0, 0, 0, int(m.group(2)))) for l in lines for m in [line_re.match(l)]}

# def simulate(blueprint, max_t = 24):
#     start_resources = {ore:0, clay:0, obs:0, geo:0}
#     start_robots = {ore:1, clay:0, obs:0, geo:0}
#     start_acts = []
#     q = deque([(0, start_resources, start_robots, start_acts)])
#     best_resources = start_resources
#     best_acts = start_acts
#     def _best(*r):
#         return max([(best_resources, best_acts), *r], key=lambda r: (r[0][geo], r[0][obs], r[0][clay], r[0][ore]))    
#     while len(q) > 0:
#         t, resources, robots, actions = q.popleft()
#         no_act_resources = {r:v + (max_t - t) * robots[r] for r, v in resources.items() }
#         best_resources, best_acts = _best((no_act_resources, actions))
#         for act in [geo, obs, clay, ore]:
#             target_robot_requirements = blueprint[act]
#             if all((target_robot_requirements[r] <= resources[r]) or (robots[r] > 0) for r in target_robot_requirements.keys()):
#                 estimated_time = max([0, *(ceil((target_robot_requirements[r] - resources[r]) / robots[r]) for r in target_robot_requirements.keys() if target_robot_requirements[r] > resources[r])]) + 1
#                 if (t + estimated_time) < max_t:
#                     new_resources = {r:v + estimated_time * robots[r] - target_robot_requirements[r] for r, v in resources.items()}
#                     new_robots = {**robots, act: robots[act] + 1}
#                     q.appendleft((t + estimated_time, new_resources, new_robots, [*actions, act]))
#     return best_resources, best_acts


# simulate(bps[1])

def build_goal(target, blueprint, t, resources, robots):
    requirements = blueprint[target]
    next_target = next((i for i, r in enumerate(requirements) if requirements[r] > resources[r] and robots[r] == 0), None)
    if next_target:
        t, resources, robots = build_goal(next_target, blueprint, t, resources, robots)
        return build_goal(target, blueprint, t, resources, robots)
    # select between noop and building other goal to reach target faster
