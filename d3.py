#part1
sum(ord(ch) - ord(orig) + delta
    for l in open("d3.txt").read().splitlines() 
    for ch in set(l[:len(l)//2]) & set(l[len(l)//2:])
    for (orig, delta) in [('a', 1) if ch.islower() else ('A', 27)])

#part2 
sum(ord(ch) - ord(orig) + delta
    for lines in [open("d3.txt").read().splitlines()]
    for group in [lines[3*i:3*i+3] for i in range(len(lines) // 3)]
    for ch in set.intersection(*(set(g) for g in group))
    for (orig, delta) in [('a', 1) if ch.islower() else ('A', 27)])