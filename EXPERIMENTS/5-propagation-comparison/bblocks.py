#!/usr/bin/python
#encoding: utf-8

import pylab
import sys
import numpy as np

import qopt
import qopt.algorithms
import qopt.problems

repeat = 50
popsize = 10

prob = sys.argv[1]
schemanum = int(sys.argv[2])

fname = prob

if prob == 'f1':
    f = qopt.problems.func1d.f1
    schemata = ['01001**********', '01*011*********', '010*11*********']
elif prob == 'f2':
    f = qopt.problems.func1d.f2
    schemata = [ '10100***************', '1*1001**************', '1010****************' ]
elif prob == 'f3':
    f = qopt.problems.func1d.f3
    schemata = ['10001********************', '1000*1*******************', '1000*********************']
elif prob == 'sat15':
    f = qopt.problems.sat15
    schemata = [ '*****11*101****', '******1*1*11***', '******1*1011***' ]
    schemata = '''
        ****011*10*****
        ***00*101******
        ***00*1*1******
        ******1010*1***
        ******101*1****
        **0*0110*******
        *********011*10
        ****0*1*1******
        ******1*1*1****
        **0*0*1********
        ********1011*1*
        ******101*11***
        ****0*101******
        ******1*101****
        ******10101****
        **0*0*10*******
        ****0*1010*****
        ******1*1*11***
        *****11*101****
        ******1*1011***
    '''.split()
elif prob == 'sat20':
    f = qopt.problems.sat20
    schemata = [ '***********1100***** 81.695000', '***********1*00*1*** 81.905998', '***********1100*1*** 82.030998']
    schemata = '''
        *********111*00*****
        ************100*****
        *********1**100*****
        ***********1*000****
        ***********110**1***
        *************0001*1*
        **********11100*****
        *************00*111*
        *************00*1*1*
        *********1*1*00*****
        ************10001***
        ***********11000****
        ***********1*00*****
        ************100*11**
        ************100*1***
        *********1*1100*****
        ***********1100*****
        ***********1*0001***
        ***********1*00*1***
        ***********1100*1***
    '''.split()
elif prob == 'sat25':
    f = qopt.problems.sat25
    schemata = [ '**************01*011*****', '***************1*0110****', '***************1*011*****' ]
    schemata = '''
        **************010*11*****
        **************01***1*****
        ***************1*01******
        1*0*10*******************
        **************0100*1*****
        ***************1*01*0****
        ***************10*110****
        110*10*******************
        ***************1*0*10****
        ***************1***10****
        **************01**11*****
        **************01*0*1*****
        11**10*******************
        ***************1**11*****
        ***************10011*****
        ***************1**110****
        ***************1*0*1*****
        **************01*011*****
        ***************1*0110****
        ***************1*011*****
    '''.split()
elif prob == 'knapsack15':
    f = qopt.problems.knapsack15
    schemata = ['****11111******', '****11*11******', '****11*110*****']
elif prob == 'knapsack20':
    f = qopt.problems.knapsack20
    schemata = [ '************010*10**', '************01011***', '************01*110**' ]
elif prob == 'knapsack25':
    f = qopt.problems.knapsack25
    schemata = ['*******************111*00', '*******************111**0', '******1011***************']

if prob in ('f1', 'sat15', 'knapsack15'):
    chromlen = 15
elif prob in ('f2', 'sat20', 'knapsack20'):
    chromlen = 20
elif prob in ('f3', 'sat25', 'knapsack25'):
    chromlen = 25

schema = schemata[schemanum - 1]

# f1
#schema = '01001**********'
#schema = '01*011*********'
#schema = '010*11*********'

# f2
#schema = '10100***************'
#schema = '1*1001**************'
#schema = '1010****************'

# f3
#schema = '10001********************'
#schema = '1000*1*******************'
#schema = '1000*********************'

# sat 15
#schema = '****001*11*****'
#schema = '**010*10*******'
#schema = '**01001********'

#schema = '***********1100*1***'
#schema = '***********1*00*1***'
#schema = '*********001*00*****'



def count_bblocks(pop):
    res = 0
    for chromo in pop:
        if qopt.matches(chromo, schema):
            res += 1
    return res

def evaluator(chrom):
    s = ''.join([str(g) for g in chrom])
    s = '%s' % s
    #f.repair(s)
    #x = f.getx(s)
    x = s
    return f.evaluate(x)

def step(ga):
    pop = []
    for ind in ga.getPopulation():
        chromo = ''.join([str(g) for g in ind])
        pop.append(chromo)
    bblocks_count.append(count_bblocks(pop))


# QIGA

class QIGA(qopt.algorithms.QIGA):
    def generation(self):
        super(QIGA, self).generation()
        #print self.Q[0]
        #e.append(qopt.E(self.Q, schema))
        #print len(e)
        bblocks_count.append(count_bblocks(self.P))

qiga = QIGA(chromlen = chromlen, popsize = popsize)
qiga.tmax = 160
qiga.problem = f

Y = np.zeros((0,160))
for r in xrange(repeat):
    bblocks_count = []
    #e = []
    qiga.run()
    #print e
    #print bblocks_count
    Y = np.vstack((Y, bblocks_count))

Y = np.average(Y, 0)
print Y

pylab.plot(Y, 'ro-', label='QIGA')

# SGA

Y = np.zeros((0,160))
for r in xrange(repeat):
    bblocks_count = []
    sga = qopt.algorithms.SGA(evaluator, chromlen)
    sga.setElitism(True)
    sga.setGenerations(160)
    sga.setPopulationSize(popsize)
    sga.stepCallback.set(step)
    sga.evolve()
    Y = np.vstack((Y, bblocks_count))

Y = np.average(Y, 0)

pylab.plot(Y, 's-', label='SGA')


pylab.title(u'Porównanie propagacji bloku budującego\nblok: %s, funkcja: %s, $chromlen=%d$' \
        % (schema, fname, chromlen))
pylab.ylabel(u'Średnia liczba bloków budujących')
pylab.xlabel('Numer generacji $t$')
pylab.legend(loc='lower right')
pylab.savefig('/tmp/bb-%s-%d.pdf' % (prob, schemanum), bbox_inches = 'tight')

