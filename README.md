# AuReM picker

_**Au**to **Re**gressive **M**odels for seismic phase picking_

**Version:** 0.1.8

**Author:** Matteo Bagagli

**Date:** 06/2020


### Introduction

This simple package provides a variety of **Au**to **Re**gressive **M**odels for picking porpouses.
For the moment this `README` is just a guide for the small functions distributed. The final package will be done and delivered when I'll have time.


### AR models

In this distribution we use the REC and AIC models.
Ideally, the minimum of those model time series represent a _pronounced_ transient arrival in the time-series.

For the AIC models we use two approaches:

- Maeda1985: The classical approach that operates
- Madarshahian2020: a _reciprocal-aic_ picker, similar to the above, but should be slightly more precise

