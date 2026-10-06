import sys

import estimator.lwe_primal as P
import estimator.lwe_dual as D

# 2^2000 classical core-SVP: 0.292 * beta = 2000, so beta ~ 6850 (cf. conf.py: 1754 ~ 2^512)
BETA_CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 6850
P.max_beta_global = BETA_CAP
D.max_beta_global = BETA_CAP
print(f"# max_beta overridden to {BETA_CAP} (default 1754, estimator/conf.py)")

from functools import partial

from estimator import *
from estimator.lwe_parameters import LWEParameters
from estimator.nd import NoiseDistribution, RR, sqrt
from estimator.lwe_primal import primal_usvp, primal_bdd
from estimator.lwe_dual import dual
from estimator.lwe_dual import matzov as dual_hybrid
from estimator.conf import red_cost_model as rcm, red_shape_model as rsm


def f(t):
    stddev = RR(sqrt(0.5 + 2**(3 - t)))
    return NoiseDistribution(mean=0, stddev=stddev, bounds=(-2, 2), is_Gaussian_like=True)


def Kaiburr(k, t, tag):
    return LWEParameters(n=k * 256, q=3329, Xs=f(t), Xe=f(t), m=k * 256, tag=tag)


for k, t in ((7, 4), (18, 6), (24, 8)):
    params = Kaiburr(k, t, f"kaiburr-{k*256}").normalize()
    print(f"\n--- n={params.n}, m={params.m}, Xs.stddev={float(params.Xs.stddev):.4f} ---")
    for name, alg in (
        ("usvp", partial(primal_usvp, red_cost_model=rcm, red_shape_model=rsm)),
        ("bdd", partial(primal_bdd, red_cost_model=rcm, red_shape_model=rsm)),
        ("dual", partial(dual, red_cost_model=rcm)),
        ("dual_hybrid", partial(dual_hybrid, red_cost_model=rcm)),
    ):
        try:
            print(name, ":", alg(params))
        except Exception as e:
            print(name, ": EXCEPTION", e)
