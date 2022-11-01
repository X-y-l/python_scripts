# Program to find the greatest common divisor of two numbers using Euclid's Algorithm

# imports libraries
import numpy as np
import math
# a,b g=gcd(a,b) => m,n ma + nb = g

# the numbers you want to find the gcd of
a = 409
b = 818

quotients = []
remainders = []
remainder = np.inf

# reorders a and b
a,b = max(a,b), min(a,b)

# until there's no more remainder
while remainder != 0:
    # find the quotient & remainder when dividing a by b
    quotient = math.floor(a/b)
    remainder = a%b

    # add them to their respective lists
    quotients.append(quotient)
    remainders.append(remainder)

    # rearrange a and b
    a,b = b,remainder

# remove the 0 from the end
del(remainders[-1])
# the last remainder will be the gcd
g = remainders[-1]
print(g)