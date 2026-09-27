import traceback
from functools import partial

from estimator import *
from estimator.lwe_parameters import LWEParameters
from estimator.nd import NoiseDistribution, RR, sqrt
from estimator.lwe_primal import primal_usvp, primal_bdd, primal_hybrid
from estimator.lwe_bkw import coded_bkw
from estimator.lwe_dual import dual
from estimator.lwe_dual import matzov as dual_hybrid
from estimator.gb import arora_gb
from estimator.lwe_guess import guess_composition
from estimator.conf import red_cost_model as red_cost_model_default, red_shape_model as red_shape_model_default


def f(t):
    stddev = RR(sqrt(0.5 + 2**(3 - t)))
    return NoiseDistribution(mean=0, stddev=stddev, bounds=(-2, 2), is_Gaussian_like=True)


def Kaiburr(k, t, tag):
    return LWEParameters(n=k * 256, q=3329, Xs=f(t), Xe=f(t), m=k * 256, tag=tag)


kaiburr_4608 = Kaiburr(18, 6, "kaiburr-4608")
kaiburr_6144 = Kaiburr(24, 8, "kaiburr-6144")

rcm = red_cost_model_default
rsm = red_shape_model_default

algorithms = {
    "arora-gb": guess_composition(arora_gb),
    "bkw": coded_bkw,
    "usvp": partial(primal_usvp, red_cost_model=rcm, red_shape_model=rsm),
    "bdd": partial(primal_bdd, red_cost_model=rcm, red_shape_model=rsm),
    "bdd_hybrid": partial(primal_hybrid, mitm=False, babai=False, red_cost_model=rcm, red_shape_model=rsm),
    "bdd_mitm_hybrid": partial(primal_hybrid, mitm=True, babai=True, red_cost_model=rcm, red_shape_model=rsm),
    "dual": partial(dual, red_cost_model=rcm),
    "dual_hybrid": partial(dual_hybrid, red_cost_model=rcm),
}

for params in (kaiburr_4608, kaiburr_6144):
    print("=" * 80)
    print(params)
    for name, alg in algorithms.items():
        print(f"--- {name} ---")
        try:
            res = alg(params.normalize())
            print(res)
        except Exception as e:
            print(f"EXCEPTION: {type(e).__name__}: {e}")
            traceback.print_exc()
