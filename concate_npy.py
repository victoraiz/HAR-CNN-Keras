# inputs output
import numpy as np
import os, sys

results = []
for f in sys.argv[1:-1]:
    print(f)
    a = np.load(f)
    results.append(a)

result = np.concatenate(results, axis=0)

np.save(sys.argv[-1], result)
