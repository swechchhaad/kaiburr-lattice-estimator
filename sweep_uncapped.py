import sys

import estimator.lwe_primal as P
import estimator.lwe_dual as D

BETA_CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 16384
P.max_beta_global = BETA_CAP
D.max_beta_global = BETA_CAP
print(f"# max_beta overridden to {BETA_CAP} (default 1754, estimator/conf.py)")

from functools import partial

from estimator import *
from estimator.lwe_parameters import LWEParameters
from estimator.nd import NoiseDistribution, RR, sqrt
from estimator.lwe_primal import primal_usvp, primal_bdd, primal_hybrid
from estimator.lwe_bkw import coded_bkw
from estimator.lwe_guess import guess_composition
from estimator.gb import arora_gb
from estimator.lwe_dual import dual
from estimator.lwe_dual import matzov as dual_hybrid
from estimator.conf import red_cost_model as rcm, red_shape_model as rsm


def f(t):
    stddev = RR(sqrt(0.5 + 2**(3 - t)))
    return NoiseDistribution(mean=0, stddev=stddev, bounds=(-2, 2), is_Gaussian_like=True)


def Kaiburr(k, t, tag):
    return LWEParameters(n=k * 256, q=3329, Xs=f(t), Xe=f(t), m=k * 256, tag=tag)


# same max_beta for every scheme, so kaiburr and FrodoKEM are estimated under one setting
SCHEMES = [Kaiburr(k, t, f"kaiburr-{k*256}") for k, t in ((7, 4), (18, 6), (24, 8))]
SCHEMES += [schemes.Frodo640, schemes.Frodo976, schemes.Frodo1344]

# same attacks and settings as LWE.estimate (estimator/lwe.py), in the same order
ATTACKS = {
    "arora-gb": guess_composition(arora_gb),
    "bkw": coded_bkw,
    "usvp": partial(primal_usvp, red_cost_model=rcm, red_shape_model=rsm),
    "bdd": partial(primal_bdd, red_cost_model=rcm, red_shape_model=rsm),
    "bdd_hybrid": partial(primal_hybrid, mitm=False, babai=False, red_cost_model=rcm, red_shape_model=rsm),
    "bdd_mitm_hybrid": partial(primal_hybrid, mitm=True, babai=True, red_cost_model=rcm, red_shape_model=rsm),
    "dual": partial(dual, red_cost_model=rcm),
    "dual_hybrid": partial(dual_hybrid, red_cost_model=rcm),
}

# optional second argument filters by tag, e.g. `sage sweep_uncapped.py 16384 frodo`
ONLY = sys.argv[2].lower() if len(sys.argv) > 2 else ""

# optional third argument picks attacks, e.g. `sage sweep_uncapped.py 16384 kaiburr bdd_hybrid,bkw`
if len(sys.argv) > 3:
    ATTACKS = {name: ATTACKS[name] for name in sys.argv[3].split(",")}

for scheme in SCHEMES:
    if ONLY not in scheme.tag.lower():
        continue
    params = scheme.normalize()
    print(f"\n--- {params.tag}: n={params.n}, m={params.m}, q={params.q}, Xs.stddev={float(params.Xs.stddev):.4f} ---")
    for name, alg in ATTACKS.items():
        try:
            print(name, ":", alg(params))
        except Exception as e:
            print(name, ": EXCEPTION", e)
