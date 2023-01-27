import pygame as pg
import matplotlib.cm as cm
import random
import math

width, height = 1500, 900
num_points = 10
time_step_scale = 0.001
trail_length = 500
spread = 10
colours = [[255 * x for x in cm.gnuplot2  (i/trail_length)[:3]] for i in range(trail_length)]

pg.init()
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

COR = [0,0,0]
translate = [11,201]
zoom = 14
z_angle = -0.25
x_angle = -1.78


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


def move_attractor_points(type, points, trails):

    for i, point in enumerate(points):
        x, y, z = point

        if type == "Halvorsen":
            a = 1.89

            dx = dt*(-a*x - 4*y - 4*z - y**2)
            dy = dt*(-a*y - 4*x - 4*z - z**2)
            dz = dt*(-a*z - 4*x - 4*y - x**2)
        
        elif type == "Sprott":
            b = 2.07
            c = 1.79

            dx = dt*(y + b*x*y + x*z)
            dy = dt*(1 - c*x**2 + y*z)
            dz = dt*(x - x**2 - y**2)
        
        elif type == "Rossler":
            d=0.2
            e=0.2
            f=5.7

            dx = dt*(-y - z)
            dy = dt*(x + d*y)
            dz = dt*(e + z*(x - f))

        elif type == "Thomas":
            g = -0.19

            dx = dt*(g*x + math.sin(y))
            dy = dt*(g*y + math.sin(z))
            dz = dt*(g*z + math.sin(x))
        
        x += dx
        y += dy
        z += dz

        points[i] = [x,y,z]
        trails[i].append([x, y, z])

    return points, trails


for i in range(num_points):
    points.append([random.random()*spread-spread/2,random.random()*spread-spread/2,random.random()*spread-spread/2])
    trails.append([])

while not done:
    clock.tick(60)

    if pg.key.get_pressed()[pg.K_p] == True:
        print(x_angle, z_angle, zoom, translate, "\n\n")

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
    dt = (new_time - old_time) * time_step_scale
    old_time = new_time

    points, trails = move_attractor_points("Rossler", points, trails)
    
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
