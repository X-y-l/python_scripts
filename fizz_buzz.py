# Nice tidy way using a sort of binary encoding of the indecies
for i in range(1,101):
    print([i,"Buzz","Fizz","Fizzbuzz"][(i%5==0) + 2*(i%3==0)])

# Gross one line way using generators
[print(str(i)*((i%3)!=0 and (i%5)!=0)+"Fizz"*((i%3)==0)+"Buzz"*((i%5)==0)+", ",end="") for i in range(1,20)]


# Loop over all numbers between 1 and 100
for i in range(0,100):
    # If divisible by 3 and 5
    if i%3 == 0 and i%5 == 0:
            print("FizzBuzz")
    # If divisible by 3
    elif i%3 == 0:
        print("Fizz")
    # If divisible by 5
    elif i%5 == 0:
        print("Buzz")
    # Else print the number
    else:
        print(i)