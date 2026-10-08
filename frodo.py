from estimator import *

# FrodoKEM parameter sets, as defined in estimator/schemes.py
for scheme in (schemes.Frodo640, schemes.Frodo976, schemes.Frodo1344):
    print(scheme)
    # r = LWE.estimate.rough(scheme)   # core-SVP-style estimate
    r = LWE.estimate(scheme)       # full estimate against all supported attacks
