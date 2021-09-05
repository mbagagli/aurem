[![DOI](https://zenodo.org/badge/403320617.svg)](https://zenodo.org/badge/latestdoi/403320617)
[![travis-build](https://app.travis-ci.com/mbagagli/aurem.svg?branch=master)](https://app.travis-ci.com/mbagagli/aurem)

# AUREM

**Au**to **Re**gressive **M**odels for seismic phase picking

**Version:** 1.1.0

**Author:** Matteo Bagagli

**Date:** 09/2021


### Introduction

This package provides a variety of **AU**to **RE**gressive **M**odels seismic pickers.
It contains the AIC and REC picking algorithm, and their **CF calculations** are fully **written in C** for faster run times "under the hood".
But, you'll just need to use python ... :)

See references for more details.

### Setup

Currently there are 2 different ways to install the package.

#### Developer
If you prefer you can create a python environment with conda or pyenv, and then clone the project

```
$ conda create -n aurem python=3.7
$ conda activate aurem
$ cd where/the/code/is
$ pip install .
# Install pytest and check everything works fine
$ pip install pytest ; pytest
```

Jupyter notebook example and tutorials can be found in the project's `books` folder.
Library dependencies are stored in `requirements.txt`

Contributors are welcome as well as any suggestion for the project improvement!

#### PyPI
From version `1.1.0` the package is hosted to PyPI repository. Therefore, once the environment is created, you would just need to type:

```
$ conda activate aurem
$ pip install aurem
```
and be ready to go ...

### References

**AIC**
- Maeda 1985: A method for reading and checking phase times in autoprocessing system of seismic wave data

**REC**
- Madarshahian at al. 2020: Bayesian Estimation of Acoustic Emission Arrival Times for Source Localization
