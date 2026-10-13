import os

from estimator import *

# run the attacks in parallel, one process per attack (LWE.estimate runs 8), capped at the number of cores
JOBS = min(8, os.cpu_count())

for scheme in (schemes.Kaiburr1792, schemes.Kaiburr4608, schemes.Kaiburr6144):
    print(scheme)
    # r = LWE.estimate.rough(scheme)   # core-SVP-style estimate
    r = LWE.estimate(scheme, jobs=JOBS)       # full estimate against all supported attacks
