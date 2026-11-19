import pygame as pg
import numpy as np

pg.init()

TILE = 25
ticks = 60
player_x = 340
player_y = 340
old_player_x = 340
old_player_y = 340
player_r = 10
line_length = 25
sensors_amount = 2
robot_angle = 0
speed = 0.3
gamma = np.pi/3
beta = (np.pi - gamma)/2
sensors_data = [0 for _ in range(sensors_amount)]


maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # 0
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # 1
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # 0
]



screen = pg.display.set_mode((800, 400))
clock = pg.Clock()

def is_wall(cx, cy):
    if(cx < len(maze[0]) and cy < len(maze)):
        return maze[cy][cx]
    return False

def draw_maze():
    background = pg.Surface((len(maze[0])*TILE, len(maze) * TILE)).convert()
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                pg.draw.rect(background, (255, 255, 255), (x*TILE, y*TILE, TILE, TILE))
    return background

def draw_robot(color):
    angle = robot_angle
    pg.draw.line(screen, (0, 255, 0), (player_x, player_y), (player_x+(line_length + 10)*np.cos(angle), player_y-(line_length + 10)*np.sin(angle)))
    angle += beta
    for i in range(sensors_amount):
        pg.draw.line(screen, color, (player_x, player_y), (player_x+line_length*np.cos(angle), player_y-line_length*np.sin(angle)))
        angle += gamma
    return pg.draw.circle(screen, color, (player_x, player_y), player_r)

def read_sensor(angle):
    for length in range(1000):
        if(is_wall(int((player_x+length*np.cos(angle))/TILE), int((player_y-length*np.sin(angle)) / TILE))):
            return length
    return 1000

def read_sensors():
    global sensors_data
    for i in range(sensors_amount):
        sensors_data[i] = (read_sensor(robot_angle+beta+gamma*i))

def find_length():
    l1, l2 = sensors_data
    l3 = round(np.sqrt(l1**2 + l2**2 - 2*l1*l2*np.cos(gamma)))
    S = l1*l2*np.sin(gamma)
    h = S/l3
    return h

def find_angle(h):
    l1,l2 = sensors_data
    gamma1 = np.arccos(h/l1)
    gamma2 = np.arccos(h/l2)
    if gamma < (gamma1 + gamma2 + 0.05) and gamma > (gamma1 + gamma2 - 0.05):
        #gamma = gamma1 + gamma2
        return round(abs(np.pi/2 - gamma1 - beta)*(180/np.pi),4)
    else:
        #gamma = gamma2-gamma1
        return round((gamma - abs(np.pi/2 - gamma1 - beta)) *(180/np.pi), 4)


background = draw_maze()
dragging = False
run = True
while run:
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    robot = draw_robot((255, 0, 0))
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                if robot.collidepoint(e.pos):
                    dragging = True
                    mouse_x, mouse_y = e.pos
                    offset_x = robot.x - mouse_x + player_r
                    offset_y = robot.y - mouse_y + player_r

        elif e.type == pg.MOUSEBUTTONUP:
            dragging = False

        elif e.type == pg.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = e.pos

                player_x = mouse_x + offset_x
                player_y = mouse_y + offset_y 

    key = pg.key.get_pressed()
    if key[pg.K_RIGHT]:
        robot_angle -= 0.01
    elif key[pg.K_LEFT]:
        robot_angle += 0.01
    read_sensors()
    h = find_length()
    alpha = find_angle(h)
    print(h, alpha, robot_angle*(180/np.pi))
    pg.display.update()
    clock.tick(ticks)
pg.quit()