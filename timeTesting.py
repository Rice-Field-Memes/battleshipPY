from time import time
import cProfile
import random
import numpy.random

def ifelif(x,y,len,rotate):
    if rotate == 2:
        return [(x,a) for a in range(y,y+len)]
    elif rotate == 3:
        return [(a,y) for a in range(x,x+len)]

def ifelse(x,y,len,rotate):
    if rotate == 2:
        return [(x,a) for a in range(y,y+len)]
    else:
        return [(a,y) for a in range(x,x+len)]

def ifTf(x,y,len,rotate):
    if rotate:
        return [(x,a) for a in range(y,y+len)]
    else:
        return [(a,y) for a in range(x,x+len)]

def testNPP(a,b,c,d):
    return ifTf(a,b,c,d)
def testLoop(funct):
    for x in range(1000000):
        (int(10*random.random()),int(10*random.random()),5,int(2*random.random())+2)

def testLoopTF(funct):
    for x in range(1000000):
        (int(10*random.random()),int(10*random.random()),5,random.getrandbits(1))

def testNP(funct):
    t = iter(numpy.random.randint(10,size=2000000))
    for x in range(1000000):
        testNPP(next(t),next(t),5,random.getrandbits(1))

def testNP2(funct):
    t = iter(numpy.random.randint(10,size=3000000))
    for x in range(1000000):
        (next(t),next(t),5,next(t)<5)

def justCoords(funct):
    for x in range(1000000):
        funct(1,1,5,3)

def justCoordsB(funct):
    for x in range(1000000):
        funct(1,1,5,True)


st = time()
testLoop(ifelif)
print("If-elif took {} seconds".format(time()-st))
st = time()

testLoop(ifelse)
print("If-else took {} seconds".format(time()-st))
st = time()

testLoopTF(ifTf)
print("If-TrueFalse took {} seconds".format(time()-st))
st = time()

testNP(ifTf)
print("Numpy iterator took {} seconds".format(time()-st))
st = time()

testNP2(ifTf)
print("Numpy iterator 2 took {} seconds".format(time()-st))
st = time()

print("\n\n")

st = time()
justCoords(ifelif)
print("Just if elif took {} seconds".format(time()-st))

st = time()
justCoords(ifelse)
print("Just if else took {} seconds".format(time()-st))

st = time()
justCoordsB(ifTf)
print("Just true false took {} seconds".format(time()-st))


