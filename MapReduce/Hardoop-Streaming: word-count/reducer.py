import sys
from itertools import groupby
from operator import itemgetter

data = (line.strip().split("\t") for line in sys.stdin)
for word, group in groupby(sorted(data, key=itemgetter(0)), key=itemgetter(0)):
    total = sum(int(count) for _, count in group)
    print(f"{word}\t{total}")

#  word  count