#!/usr/bin/python
#

#   F1     5.20e-9   1.94e-9    1.71e-9   1.67e-9
#   F2     4.70e-9   1.56e-9    3.82e-9   1.34e-9
#   F3     5.60e-9   1.93e-9    3.92e+4   1.78e+4
#   F4     5.02e-9   1.71e-9    4.62e-9   1.53e-9
#   F5     6.58e-9   2.17e-9    1.62e-9   2.02e-9
#   F6     4.87e-9   1.66e-9    2.88e+0   1.80e+0
#   F7     3.31e-9   2.02e-9    1.90e-1   6.67e-2
#   F8     2.00e+1   3.89e-3    2.00e+1   4.48e-2
#   F9     2.39e-1   4.34e-1    2.14e-1   1.02e-1
#   F10    7.96e-2   2.75e-1    1.74e+1   7.41e+0
#   F11    9.34e-1   9.00e-1    6.17e+0   1.26e+0
#   F12    2.93e+1   1.42e+2    1.54e+1   4.82e+0
#   F13    6.96e-1   1.50e-1    6.81e-1   2.29e-1
#   F14    3.01e+0   3.49e-1    2.91e+0   2.05e-1
#   F15    2.28e+2   6.80e+1    8.92e+1   6.81e+0
#   F16    9.13e+1   3.49e+0    1.32e+2   3.49e+1
#   F17    1.23e+2   2.09e+1    1.79e+2   5.04e+1
#   F18    3.32e+2   1.12e+2    4.51e+2   5.22e+1
#   F19    3.26e+2   9.93e+1    4.40e+2   5.83e+1
#   F20    3.00e+2   0.00e+0    4.38e+2   5.97e+1
#   F21    5.00e+2   3.48e-13   4.28e+2   9.80e+1
#   F22    7.29e+2   6.86e+0    4.42e+2   2.45e+2
#   F23    5.59e+2   3.24e-11   7.44e+2   6.70e+1
#   F24    2.00e+2   2.29e-6    2.00e+2   1.14e-7
#   F25    3.74e+2   3.22e+0    3.62e+2   8.59e+0

import sys
import numpy as np
import math

# to jest bardzo ladne:
import qopt
import qopt.benchmarks.CEC2005.cec2005 as cec2005
import qopt.algorithms.iQIEA as iQIEA
import qopt.algorithms.SGA as SGA
import qopt.analysis.plot as plot
import copy

FNUM = int(sys.argv[1])

plot_limits = (
        (10000, -500, 8000),  # f1
        (10000, None, 25000),  # f2
        (10000, None, .2e9),  # f3
        (10000, None, 20000),  # f4
        (10000, None, 15000),  # f5
        (10000, None, .1e9),  # f6
        (10000, None, 2500),  # f7
        (10000, None, None),  # f8
        (10000, None, -200),  # f9
        (10000, None, -200),  # f10
        (10000, None, None),  # f11
        (10000, None, 150000),  # f12
        (10000, -150, -100),  # f13
        (10000, None, None),  # f14
        (10000, None, None),  # f15
        (10000, None, 700),  # f16
        (10000, None, 700),  # f17
        (10000, None, 1300),  # f18
        (10000, None, 1300),  # f19
        (10000, None, 1300),  # f20
        (10000, None, 2000),  # f21
        (10000, None, 1700),  # f22
        (10000, None, 1800),  # f23
        (10000, None, 1700),  # f24
        (10000, None, 2400),  # f25
        )

runs = 5
BFUNC = cec2005.FUNCTIONS['f' + str(FNUM)]

max_evaluation = 10000
dim = 10

iqiea = iQIEA.iQIEA()
iqiea.fitness_function = BFUNC['fun']
iqiea.G = dim
iqiea.bounds = [BFUNC['bounds']] * iqiea.G
iqiea.popsize = 10
iqiea.K = 10
iqiea.kstep = 10
iqiea.XI = .1
iqiea.DELTA = .5
iqiea.tmax = max_evaluation / iqiea.K


algs = []
for run in xrange(runs):
    #qopt.tic()
    iqiea.run()
    algs.append(copy.deepcopy(iqiea))
    #print qopt.toc()
plot1 = plot.Plot(algs)
#plot1.pylab().ylim(ymax = 10000)

sgadata = np.matrix(';'.join(open('/tmp/sga/f%s/avg' % str(FNUM)).readlines()))
plot1.pylab().plot(sgadata[:,0], sgadata[:,1], 'x-', label='SGA')
plot1.pylab().legend()
if plot_limits[FNUM - 1][0]:
    plot1.pylab().xlim(xmax = plot_limits[FNUM - 1][0])
if plot_limits[FNUM - 1][1]:
    plot1.pylab().ylim(ymin = plot_limits[FNUM - 1][1])
if plot_limits[FNUM - 1][2]:
    plot1.pylab().ylim(ymax = plot_limits[FNUM - 1][2])

plot1.save('/tmp/plot-f%d.pdf' % FNUM)

