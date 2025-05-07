from itertools import chain, combinations

def powerset(iterable):
    s = list(iterable)
    return [list(item) for item in chain.from_iterable(combinations(s, r) for r in range(len(s)+1))]