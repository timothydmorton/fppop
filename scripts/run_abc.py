#!/usr/bin/env python

from __future__ import print_function, division
import sys, os

ROOT = '..'

sys.path.append(ROOT)
sys.path.append(os.path.join(ROOT,'..'))


from exosyspop.populations import KeplerPowerLawBinaryPopulation
from exosyspop.survey import DetectionRamp
from exosyspop.abc import ABCModel

from simpleabc.simple_abc import pmc_abc

import numpy as np

import logging
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)


pop = KeplerPowerLawBinaryPopulation.load(os.path.join(ROOT,'plaw_pop'))
pop.set_params(period_min=20, period_max=1200, beta=-0.95, fB=0.14)

eff = DetectionRamp(6,16)

data = pop.observe(new=True, regr_trap=True).observe(eff)

model = ABCModel(pop, eff)

model._distance_norms = np.array([ 1.        ,  4.49241213,  2.60025772,  2.73734061])

pmc_posterior = pmc_abc(model, data, epsilon_0=0.5, min_samples=200, steps=20, verbose=True,
                       parallel=True, n_procs=10)

np.save('pmc_posterior', pmc_posterior)
