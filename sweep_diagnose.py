from functools import partial

from estimator import *
from estimator.lwe_parameters import LWEParameters
from estimator.nd import NoiseDistribution, RR, sqrt
from estimator.lwe_primal import primal_usvp, primal_bdd
from estimator.lwe_dual import dual
from estimator.lwe_dual import matzov as dual_hybrid
from estimator.conf import red_cost_model as red_cost_model_default, red_shape_model as red_shape_model_default


def f(t):
    stddev = RR(sqrt(0.5 + 2**(3 - t)))
    return NoiseDistribution(mean=0, stddev=stddev, bounds=(-2, 2), is_Gaussian_like=True)


def Kaiburr(k, t, tag):
    return LWEParameters(n=k * 256, q=3329, Xs=f(t), Xe=f(t), m=k * 256, tag=tag)


rcm = red_cost_model_default
rsm = red_shape_model_default

print("#" * 80)
print("# Sweep 1: fixed noise (t=6, matches kaiburr-4608's sigma), n growing 1792 -> 6144")
print("#" * 80)
for k in (7, 9, 11, 13, 15, 17, 18, 20, 22, 24):
    params = Kaiburr(k, 6, f"sweep-t6-k{k}").normalize()
    print(f"\n--- n={params.n}, m={params.m}, Xs.stddev={float(params.Xs.stddev):.4f} ---")
    try:
        r = primal_usvp(params, red_cost_model=rcm, red_shape_model=rsm)
        print("usvp        :", r)
    except Exception as e:
        print("usvp        : EXCEPTION", e)
    try:
        r = primal_bdd(params, red_cost_model=rcm, red_shape_model=rsm)
        print("bdd         :", r)
    except Exception as e:
        print("bdd         : EXCEPTION", e)
    try:
        r = dual(params, red_cost_model=rcm)
        print("dual        :", r)
    except Exception as e:
        print("dual        : EXCEPTION", e)
    try:
        r = dual_hybrid(params, red_cost_model=rcm)
        print("dual_hybrid :", r)
    except Exception as e:
        print("dual_hybrid : EXCEPTION", e)

print("\n" + "#" * 80)
print("# Sweep 2: the actual kaiburr schemes (n and t both growing, as in kaiburr.py)")
print("#" * 80)
for k, t in ((7, 4), (18, 6), (24, 8)):
    params = Kaiburr(k, t, f"kaiburr-{k*256}").normalize()
    print(f"\n--- n={params.n}, m={params.m}, Xs.stddev={float(params.Xs.stddev):.4f} ---")
    try:
        r = dual_hybrid(params, red_cost_model=rcm)
        print("dual_hybrid :", r)
    except Exception as e:
        print("dual_hybrid : EXCEPTION", e)

print("\n" + "#" * 80)
print("# rough() cross-check (core-SVP style, simpler formulas) for all three kaiburr schemes")
print("#" * 80)
for k, t in ((7, 4), (18, 6), (24, 8)):
    params = Kaiburr(k, t, f"kaiburr-{k*256}")
    print(f"\n{params}")
    r = LWE.estimate.rough(params)
