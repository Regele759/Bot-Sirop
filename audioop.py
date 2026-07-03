# Stub for Python 3.13 compatibility
# discord.py tries to import audioop which was removed from Python 3.13
# This provides a minimal implementation so the import doesn't fail

def add(fragment1, fragment2, width):
    return fragment1 + fragment2

def adpcm2lin(data, state, width):
    return data, state

def lin2adpcm(data, state, width):
    return data, state

def lin2alaw(data, width):
    return data

def lin2ulaw(data, width):
    return data

def alaw2lin(data, width):
    return data

def ulaw2lin(data, width):
    return data

def mul(fragment, width, factor):
    return fragment

def ratecv(data, state, width, sr1, sr2, state_size):
    return data, state

def reverse(fragment, width):
    return fragment

def tomono(data, width, lfac, rfac):
    return data

def tostereo(data, width, lfac, rfac):
    return data

def getsample(data, width, index):
    return 0

def max(data, width):
    return 0

def avgpp(data, width):
    return 0

def maxpp(data, width):
    return 0

def avg(data, width):
    return 0

def rms(data, width):
    return 0

def findfit(data, template):
    return 0, 0

def findmax(data, length):
    return 0

def cross(data1, data2):
    return 0

def minmax(data, width):
    return 0, 0
