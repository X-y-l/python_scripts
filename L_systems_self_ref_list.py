# While programming I had a weird bug where my lists had a strange element that looked like [...]. On further inspection,
# I realised that this was a pointer to the list itself, which is very cool and weird. I tried experimenting and found
# you can get things like a list containing 5 of itself, or two lists that just contain each other. I tried thinking of
# ways this could ever be useful and realised they would be a very simple easy way to create L systems - so that's what
# I've done here.

# This is obviously not a very efficient way of doing any of these, but it's interesting, fun, and incredibly simple.

# I'll be using turtle to draw some fractals that use L systems, because it makes it so easy.
# Only downside is it's a little slow, but it's worth it for the sake of simplicity.
import turtle as t

# Hides the turtle, sets the speed to be as fast as possible.
t.ht(); t.speed(0); t.color("lime"); t.bgcolor("black")

# The main interesting function. I tried to make it as versatile as possible so you wouldn't need to change much to adapt it to a different L system.
# To see how its used, look at the later functions.
# The output looks like a list of characters that can be then used as the instructions for a turtle.
def l_system_to_moves(code, depth, a, b, l_sys):
    for item in code:
        # If we havent reached the max depth and the current item is a list, then recursively enter the new list, and increase the depth.
        if type(item) == list and depth > 1:
            l_system_to_moves(item, depth-1, a, b, l_sys)

        # Otherwise, the item is either not a list, or we are at max depth.
        else:
            # if the item is a list, and it is one of the relevent letters, then append the corresponding letter to the output
            if item == a:
                l_sys.append("a")
            elif item == b:
                l_sys.append("b")
            # or if it is just a character that isnt 0
            elif item != "0":
                l_sys.append(item)

    # then return the list so far
    return l_sys
# The 0 is there because it seems when comparing two lists like this makes it sometimes recursively check each element forever,
# unless the two lists are of different lengths, in which case it handles it fine - so I added a dummy character to add to the
# end of either of them if they're the same length.


# This L system draws a cute binary tree, of approximate total height "height", and has recursive depth "depth".
def tree(depth, height):
    # moves the turtle to a nice place
    t.pu(); t.seth(90); t.setpos(0,-100); t.pd()

    # This L system goes:
    # a -> aa
    # b -> a[b]b
    # axiom: b
    # where a means go forwards, b means draw a branch, and the brackets mean rotating 45 degrees left or right, with the open bracket
    # storing the current position in a stack, and the close bracket popping it from the stack and bringing you back there.
    # I just replaced the [ and ] with c and d.

    # defines the variables / constants / rules / axiom
    a, b = [], []
    a[:], b[:] = [a,a], [a,"c",b,"d",b]
    axiom = b

    # the distance has to decrease exponentially as the depth increases to stop it from expanding off to infinity
    # I think the exact ratio is something to do with the hausdorff dimension, but this is good enough
    dist = height / 2**depth
    # generates the list of letters that we can use to draw the tree
    moves = l_system_to_moves(axiom, depth, a, b, [])

    # this list will be used as a stack to store positions, that we can pop from to return to later
    pos_list = []
    for move in moves:
        # if we see a or b, we just move forwards. we could separate these into two cases and then draw a leaf or something on
        # b's, because they only occur at the end of branches.
        if move == "a" or "b":
            t.fd(dist)
        # if we see a c, then add the current position (as a 3-tuple of x,y,angle) to the stack, and then turn left 45 degrees
        if move == "c":
            pos_list.append((t.xcor(),t.ycor(),t.heading())); t.lt(45)
        # if we see a d, pop the last position from the stack and go there, then turn right 45 degrees.
        if move == "d":
            t.pu(); t.goto(pos_list[-1][:2]); t.seth(pos_list[-1][2]); t.pd(); pos_list.pop(); t.rt(45)
    t.done()


# This L system draws successive layers of increasing depth of the cantor set
def cantor(depth, width, height):
    # Ugly turtle starting stuff, draws the first block because depth 0 was being bad (ideally it would return the axiom but it doesn't do that)
    t.width(1); t.pu()
    t.goto(-width/2, -height/2 + height/depth); t.begin_fill(); t.fd(width); t.rt(90); t.fd(height/depth); t.rt(90)
    t.fd(width); t.rt(90); t.fd(height/depth); t.rt(90); t.end_fill(); t.goto(-width/2, -height/2 + 2*height/depth); t.pd()

    # This L system goes:
    # a -> aba
    # b -> bbb
    # axiom: a
    # where a means draw a line, and b means go forwards without drawing a line.

    # defines the variables / constants / rules / axiom
    a,b = [], []
    a[:], b[:] = [a,b,a], [b,b,b,"0"]
    axiom = a

    # generates the rest of the layers
    for y in range(depth-1):
        # the total width needs to be width, and each layer has 3^depth "slices", so the individual width of a slice needs to be this
        dist = width / 3**(y+1)
        # generates the list of moves for the current layer
        moves = l_system_to_moves(axiom, y+1, a, b, [])

        for move in moves:
            # if it's an a, then draw a rectangle of the appropriate width and height
            if move == "a":
                t.begin_fill(); t.fd(dist); t.rt(90); t.fd(height/depth); t.rt(90); t.fd(dist); t.rt(90); t.fd(height/depth); t.rt(90); t.end_fill(); t.fd(dist)
            # if it's a b, then just move to the next section
            elif move == "b":
                t.pu(); t.fd(dist); t.pd()

        # moves to the next layer
        t.pu(); t.goto(-width/2, -height/2 + height * (y+3) / depth); t.pd()

    t.done()
    # theres an annoying bug where the first layer is 1 pixel shorter than the others - why?!

# a couple of other examples to show how easy it is

def arrowhead(depth, size, angle):
    a,b = [], []
    a[:], b[:] = [b,"d",a,"d",b], [a,"c",b,"c",a,"0"]
    axiom = a

    moves = l_system_to_moves(axiom, depth, a, b, [])

    for move in moves:
        if move == "a" or move == "b":
            t.fd(size/2**depth)
        elif move == "c":
            t.rt(angle)
        elif move == "d":
            t.lt(angle)
    t.done()


def dragon(depth, size):
    a,b = [], []
    a[:], b[:] = [a,"c",b], [a,"d",b,"0"]
    axiom = a

    moves = l_system_to_moves(axiom, depth, a, b, [])

    for move in moves:
        if move == "a" or "b":
            t.fd(size/1.5236**depth)
        if move == "c":
            t.rt(90)
        if move == "d":
            t.lt(90)
    t.done()


def plant(depth, size):
    t.pu(); t.goto(0,-size); t.seth(90); t.pd()

    a,b = [], [] # (X → F+[[X]-X]-F[-FX]+X), (F → FF)
    a[:], b[:] = [b,"c","e","e",a,"f","d",a,"f","d",b,"e","d",b,a,"f","c",a], [b,b]
    axiom = a

    moves = l_system_to_moves(axiom, depth, a, b, [])

    pos_list = []
    for move in moves:
        if move == "b":
            t.fd(size/2**depth)
        if move == "c":
            t.rt(25)
        if move == "d":
            t.lt(25)
        if move == "e":
            pos_list.append((t.xcor(),t.ycor(),t.heading()))
        if move == "f":
            t.pu(); t.goto(pos_list[-1][:2]); t.seth(pos_list[-1][2]); t.pd(); pos_list.pop()

    t.done()

#plant(6,300)
#dragon(9,400)
#arrowhead(7, 300, 60)   
#cantor(5, 500, 500)
#tree(6, 400)
