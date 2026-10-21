# Lattice estimates for Kaiburr

In this folder, we give the code to produce the attack-cost estimates for the LWE problems underlying Kaiburr and, for comparison, FrodoKEM (Tables 3 and 4). Besides the lattice attacks, this also covers Arora–Ge with Gröbner bases and BKW.

This is a fork of the [lattice-estimator](https://github.com/malb/lattice-estimator) at commit `53da598`.

## Running

Requires [SageMath](https://www.sagemath.org). From this directory:

```
sage kaiburr.py    # Kaiburr1792, Kaiburr4608, Kaiburr6144
sage frodo.py      # Frodo640, Frodo976, Frodo1344
```

or, for a single parameter set:

```python
>>> from estimator import *
>>> LWE.estimate(schemes.Kaiburr4608)
```

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

Bold marks the cheapest attack for each set. For Frodo976 and Frodo1344 (Table 4), the cheapest attacks
cost 2^225.2 and 2^281.7.

See the [upstream repository](https://github.com/malb/lattice-estimator) and its
[documentation](https://lattice-estimator.readthedocs.io/en/latest/) for the estimator itself. If you use the estimator,
please cite

> Martin R. Albrecht, Rachel Player and Sam Scott. *On the concrete hardness of Learning with Errors*.
> Journal of Mathematical Cryptology. Volume 9, Issue 3, Pages 169–203, ISSN (Online) 1862-2984,
> ISSN (Print) 1862-2976 DOI: 10.1515/jmc-2015-0016, October 2015
