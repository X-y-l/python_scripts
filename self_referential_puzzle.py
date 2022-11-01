# Quick program to find solutions to a puzzle I was working on

import time
solutions = []
for a in range(0,7):
    for b in range(0,7):
        for c in range(0,7):
            print(a,b,c)
            nums = [a,b,c,0,2,2]
            equal_zero = 0
            more_twos = 0
            equal_twos = 0
            less_threes = 0
            for number in nums:
                if number == 0:
                    equal_zero += 1
                if number < 2:
                    more_twos += 1
                if number == 2:
                    equal_twos += 1

            if a == equal_zero and b == more_twos and c == equal_twos:
                solutions.append((a,b,c))

print(solutions)