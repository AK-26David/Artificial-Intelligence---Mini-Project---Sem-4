import random

def _gen():
    base = 3
    side = base*base

    def pattern(r, c):
        return (base*(r % base)+r//base+c) % side
    def shuffle(s):
        return random.sample(s, len(s))

    rBase = range(base)
    rows = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base*base+1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    return board
