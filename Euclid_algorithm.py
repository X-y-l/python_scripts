import numpy as np
import math
#a,b g=gcd(a,b) => m,n ma + nb = g
remainder = np.inf

a = 258
b = 147
quotients = []
remainders = []

a,b = max(a,b), min(a,b)

while remainder != 0:
    quotient = math.floor(a/b)
    remainder = a%b

    quotients.append(quotient)
    remainders.append(remainder)

    a,b = b,remainder

del(remainders[-1])
g = remainders[-1]
