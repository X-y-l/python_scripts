import pygame as pg
import matplotlib.cm as cm
import random
import math

def rotateZ(coord, origin, radians):        
    delx = coord[0] - origin[0]
    dely = coord[1] - origin[1]
    d = math.hypot(dely, delx)
    theta = math.atan2(dely, delx) + radians
    newx = origin[0] + d * math.cos(theta)
    newy = origin[1] + d * math.sin(theta)
    return [newx, newy, coord[2]]


def rotateX(coord, origin, radians):
    delz = coord[2] - origin[2]
    dely = coord[1] - origin[1]
    d = math.hypot(dely, delz)
    theta = math.atan2(dely, delz) + radians
    newz = origin[2] + d * math.cos(theta)
    newy = origin[1] + d * math.sin(theta)
    return [coord[0], newy, newz]


pg.init()
width, height = 1500, 900
size = [width, height]
screen = pg.display.set_mode(size)
pg.display.set_caption("Attractor")

done = False
clock = pg.time.Clock()
old_time = 0

points = []
points_transformed = []
trails = []
trails_transformed = []

#Halvorsen var
a = 1.89

#Sprott
b = 2.07
c = 1.79

#Rossler
d=0.2
e=0.2
f=5.7

COR = [0,0,0]

translate = [0,0]
zoom = 30
z_angle = 0
x_angle = 0

num_points = 10
trail_length = 1000
spread = 0.1
colours = [[255 * x for x in cm.bone(i/trail_length)[:3]] for i in range(trail_length)]

for i in range(num_points):
    points.append([random.random()*spread-spread/2,random.random()*spread-spread/2,random.random()*spread-spread/2])
    trails.append([])

while not done:
    clock.tick(60)

    if pg.key.get_pressed()[pg.K_UP] == True:
        x_angle += 0.01
    if pg.key.get_pressed()[pg.K_DOWN] == True:
        x_angle -= 0.01

    if pg.key.get_pressed()[pg.K_RIGHT] == True:
        z_angle += 0.01
    if pg.key.get_pressed()[pg.K_LEFT] == True:
        z_angle -= 0.01

    if pg.key.get_pressed()[pg.K_EQUALS] == True:
        zoom *= 1.01
    if pg.key.get_pressed()[pg.K_MINUS] == True:
        zoom /= 1.01
    
    if pg.mouse.get_pressed()[0]:
        move = pg.mouse.get_rel()
        translate[0] += move[0]
        translate[1] += move[1]
    else:
        pg.mouse.get_rel()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    new_time = pg.time.get_ticks() 
    dt = (new_time - old_time) / 2000
    old_time = new_time
    
    # Halvorsen
    """for i, point in enumerate(points):
        dx = dt*(-a*point[0] - 4*point[1] - 4*point[2] - point[1]**2)
        dy = dt*(-a*point[1] - 4*point[0] - 4*point[2] - point[2]**2)
        dz = dt*(-a*point[2] - 4*point[0] - 4*point[1] - point[0]**2)
        
        point[0] += dx
        point[1] += dy
        point[2] += dz

        trails[i].append([point[0], point[1], point[2]])"""
    
    # Sprott
    for i, point in enumerate(points):
        dx = dt*(point[1] + b*point[0]*point[1] + point[0]*point[2])
        dy = dt*(1 - c*point[0]**2 + point[1]*point[2])
        dz = dt*(point[0] - point[0]**2 - point[1]**2)
        
        point[0] += dx
        point[1] += dy
        point[2] += dz

        trails[i].append([point[0], point[1], point[2]])

    # Rossler
    """for i, point in enumerate(points):
        dx = dt*(-point[1] - point[2])
        dy = dt*(point[0] + d*point[1])
        dz = dt*(e + point[2]*(point[0] - f))
        
        point[0] += dx
        point[1] += dy
        point[2] += dz

        trails[i].append([point[0], point[1], point[2]])"""

    points_transformed = []
    trails_transformed = []

    for point in points:
        points_transformed.append(rotateX(rotateZ(point, COR, z_angle), COR, x_angle))

    screen.fill((0,0,0))

    for i, trail in enumerate(trails):
        if len(trail) > trail_length:
            del(trail[0])

        trails_transformed.append([])
        for coord in trail:
            trails_transformed[i].append(rotateX(rotateZ(coord, COR, z_angle), COR, x_angle)[:2])


    for trail in trails_transformed:
        for i in range(len(trail)-1):
            colour = colours[i]
            pg.draw.line(screen, colour, [trail[i][0]*zoom + width/2 + translate[0], trail[i][1]*zoom + height/2 + translate[1]], [trail[i+1][0]*zoom + width/2 + translate[0], trail[i+1][1]*zoom + height/2 + translate[1]])


    for point in points_transformed:
        pg.draw.circle(screen, (255,255,255), [point[0]*zoom + width/2 + translate[0], point[1]*zoom + height/2 + translate[1]],2)

    pg.display.flip()

pg.quit()
