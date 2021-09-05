# AuReM picker

_**Au**to **Re**gressive **M**odels for seismic phase picking_

**Version:** 1.0.2

**Author:** Matteo Bagagli

**Date:** 09/2020


### Introduction

This package provides a variety of **Au**to **Re**gressive **M**odels for picking purposes.

If you prefer you can create a python environment with conda or pyenv:

```
$ conda create -n aurem python=3.7
$ conda activate aurem
$ cd where/the/code/is
$ pip install .
# Install pytest and check everything works fine
$ pip install pytest ; pytest
```

Example of usage can be extracted from `./tests/test_aurem.py` for both REC and AIC objects
Library dependencies are stored in `requirements.txt`

From version `1.1.0` the package is hosted to PyPI repository. Therefore, once the environment is created, you would just need to type:

```
$ conda activate aurem
$ pip install aurem
```

and be ready to go ...

### AR models

In this distribution we use the REC and AIC models.
Ideally, the minimum of those model-CFs time series represent a _pronounced_ transient arrival in the time-series.

For the AIC models we use two approaches:

### References

**AIC**
- Maeda 1985: A method for reading and checking phase times in autoprocessing system of seismic wave data

**REC**
- Madarshahian at al. 2020: Bayesian Estimation of Acoustic Emission Arrival Times for Source Localization

_This algorithm acronyms stands for "reciprocal-aic" picker, similar to the above, but should be slightly more precise with micro-earthquakes_




