from estimator import *
from estimator.nd import NoiseDistribution, RR, sqrt

def f(t):
    """kaiburr noise family f(t): Pr[±2]=2^-t, Pr[±1]=1/4, Pr[0]=1/2-2^-(t-1)."""
    stddev = RR(sqrt(0.5 + 2**(3 - t)))
    return NoiseDistribution(
        mean=0,
        stddev=stddev,
        bounds=(-2, 2),
        is_Gaussian_like=True,
    )

def Kaiburr(k, t, tag):
    return LWEParameters(
        n=k * 256,
        q=3329,
        Xs=f(t),
        Xe=f(t),
        m=k * 256,
        tag=tag,
    )
# compression is already removed, so no changes necessary

kaiburr_1792 = Kaiburr(7, 4, "kaiburr-1792")
kaiburr_4608 = Kaiburr(18, 6, "kaiburr-4608")
kaiburr_6144 = Kaiburr(24, 8, "kaiburr-6144")

for scheme in (kaiburr_1792, kaiburr_4608, kaiburr_6144):
    print(scheme)
    r = LWE.estimate.rough(scheme)   # core-SVP-style estimate
    r = LWE.estimate(scheme)       # full estimate against all supported attacks