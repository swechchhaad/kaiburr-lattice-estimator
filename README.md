# Lattice estimates for Kaiburr

This artifact accompanies Tables 3 and 4 of the paper "Kaiburr: ML-KEM at (much) higher security."
For each Kaiburr parameter set, it estimates the cost of the known lattice attacks (and Arora–GB and BKW) on the underlying LWE problem, and does the same for FrodoKEM for comparison.

This is a research fork of the well-known [lattice-estimator](https://github.com/malb/lattice-estimator), based on
upstream commit `53da598`.

## Running

Requires [SageMath](https://www.sagemath.org). From the repository root:

```
sage kaiburr.py    # Kaiburr1792, Kaiburr4608, Kaiburr6144
sage frodo.py      # Frodo640, Frodo976, Frodo1344
```

The parameter sets are also available directly:

```python
>>> from estimator import *
>>> LWE.estimate(schemes.Kaiburr4608)
```

## Changes from upstream

Upstream caps the lattice-reduction block size at `max_beta = 1754` (about 2^512 under the ADPS16 core-SVP model). It is too low for the larger Kaiburr sets,
where every lattice attack then returns infinity. We make two changes:

1. [`estimator/conf.py`](estimator/conf.py): `max_beta` is raised to 16384, larger than any lattice dimension that
   arises here, so the cap does not bind.
2. [`estimator/lwe_primal.py`](estimator/lwe_primal.py): the SVP dimension in the BDD attack was separately capped by a
   hard-coded 1754 for lattices of dimension above 4096. It now follows `max_beta`.

For parameter sets where the old cap did not bind, results are unchanged. We checked this for Kaiburr1792 and all three
FrodoKEM sets, which give identical output under both caps.

## Expected results

| Attack          | Frodo640 | Kaiburr1792 | Kaiburr4608 | Kaiburr6144 |
|-----------------|----------|-------------|-------------|-------------|
| arora-gb        | ∞        | ∞           | ∞           | ∞           |
| bkw             | 241.1    | no result   | no result   | no result   |
| usvp            | 166.4    | 494.0       | 1275.5      | 1701.0      |
| bdd             | **162.9**| 488.7       | **1268.9**  | **1694.3**  |
| bdd_hybrid      | 162.9    | 488.7       | 1268.9      | 1694.3      |
| bdd_mitm_hybrid | 349.6    | 883.0       | 2411.1      | 3265.2      |
| dual            | 173.0    | 519.8       | 1400.8      | error       |
| dual_hybrid     | 170.1    | **467.3**   | 1458.3      | 2120.4      |

The cheapest attack for each set is in bold.


See the [upstream repository](https://github.com/malb/lattice-estimator) and its
[documentation](https://lattice-estimator.readthedocs.io/en/latest/) for the estimator itself. If you use the estimator,
please cite

> Martin R. Albrecht, Rachel Player and Sam Scott. *On the concrete hardness of Learning with Errors*.
> Journal of Mathematical Cryptology. Volume 9, Issue 3, Pages 169–203, ISSN (Online) 1862-2984,
> ISSN (Print) 1862-2976 DOI: 10.1515/jmc-2015-0016, October 2015
