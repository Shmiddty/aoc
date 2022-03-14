import sys
from enum import aggregate

inp = [line.strip() for line in sys.stdin]
counts = map(aggregate, zip(*inp))

most = map(lambda d: max(d, key=d.get), counts)
print(''.join(most))

least = map(lambda d: min(d, key=d.get), counts)
print(''.join(least))
