import pygame
import random
import sys
import time
# import copy
import os
from pygame.locals import *

print(os.getcwd())

from Ship import Ship
# from Population import Population
from Pop2 import Pop

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Asteroids")
screen = pygame.display.set_mode((700, 600))
scr_w = screen.get_width()
scr_h = screen.get_height()
font = pygame.font.SysFont('lucidaconsole', 60)
font2 = pygame.font.SysFont('lucidaconsole', 20)
mode = 'menu'
last_shot = 0
aster_convert = 1
asteroid_spawn = 0
spawnx = 0
spawny = 0
score = 0
timeout = 0
starttime = time.time()
highscore = 0
lasthighscore = 0
dispinfo = True

drawnum = 25

asteroid1 = pygame.image.load("Images/Asteroid1.png").convert()
asteroid1.set_colorkey((0, 0, 0))
asteroid2 = pygame.image.load("Images/Asteroid2.png").convert()
asteroid2.set_colorkey((0, 0, 0))
asteroid3 = pygame.image.load("Images/Asteroid3.png").convert()
asteroid3.set_colorkey((0, 0, 0))
asteroid4 = pygame.image.load("Images/Asteroid1_m.png").convert()
asteroid4.set_colorkey((0, 0, 0))
asteroid5 = pygame.image.load("Images/Asteroid2_m.png").convert()
asteroid5.set_colorkey((0, 0, 0))
asteroid6 = pygame.image.load("Images/Asteroid3_m.png").convert()
asteroid6.set_colorkey((0, 0, 0))
asteroid7 = pygame.image.load("Images/Asteroid1_s.png").convert()
asteroid7.set_colorkey((0, 0, 0))
asteroid8 = pygame.image.load("Images/Asteroid2_s.png").convert()
asteroid8.set_colorkey((0, 0, 0))
asteroid9 = pygame.image.load("Images/Asteroid3_s.png").convert()
asteroid9.set_colorkey((0, 0, 0))
costumes = [asteroid1, asteroid2, asteroid3, asteroid4, asteroid5, asteroid6, asteroid7, asteroid8, asteroid9]

ship_move = pygame.image.load("Images/ship_fly.png").convert()
ship_move.set_colorkey((0, 0, 0))
ship_still = pygame.image.load("Images/ship_still.png").convert()
ship_still.set_colorkey((0, 0, 0))

popnum = 50  # num of nets & ships

vardict = {
    'screen': screen,
    'aster_convert': aster_convert,
    'scr_w': scr_w,
    'scr_h': scr_h,
    'asteroid_spawn': asteroid_spawn,
    'spawnx': spawnx,
    'spawny': spawny,
    'score': score,
    'costumes': costumes,
    'ship_move': ship_move,
    'ship_still': ship_still
}

population = Pop(popnum, 5, 3)  # TODO: move all net control to Pop2

ships = []
for i in range(popnum):
    colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    ships.append(Ship(vardict, colour, population.nets[i].run_net, population.nets[i].getnet))  # reference function object so it can be called

fitnesslist = []
drawrays = True

# net settings  # TODO: currently obsolete
popsize = 25
newnetrate = 0.1  # fraction of totally random nets
newnetnum = 3  # how many parent nets are generated
gen = 0
stripemptynets = True
topkeepnum = 3  # not included in popnum
# TODO: Also fix agvfps

# for i in pygame.font.get_fonts():
#    print(i)


def reset(load=False):
    global fitnesslist, ships, gen, topkeepnum, popsize, newnetrate, newnetnum, timeout, highscore
    global lasthighscore, starttime
    # print(population.innovlist)
    for i in range(popsize):
        pass
        # print(population.nets[i].innovs)
    sortedfitnesslist = sorted(fitnesslist, key=lambda x: x[1])
    # print(sortedfitnesslist)
    # print(fitnesslist)
    fitnesslist = sortedfitnesslist
    # print(sortedfitnesslist)
    ships = []
    gen += 1
    timeout = 0
    starttime = time.time()
    if load == False:
        for i in range(popnum):
            colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            ships.append(Ship(vardict, colour, population.nets[i].run_net, population.nets[i].getnet))  # remember to put function object as arg
        population.mutate_all(5)
        # nets = copy.deepcopy(population.combfunc(fitnesslist, newnetnum))
        # for i in range(int(popsize * (1 - newnetrate))):
        #     colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        #     ships.append(Ship(vardict, colour, copy.deepcopy(nets[random.randint(0, len(nets) - 1)])))
        #     ships[-1].net.mutate()
        # for i in range(int(popsize * newnetrate)):
        #     colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        #     ships.append(Ship(vardict, colour, None))
        # for i in range(topkeepnum):
        # print(
        #     f'Saved net: {fitnesslist[-(i + 1)][0]},fitnesslist: {fitnesslist[-(i + 1)][1]},score: {fitnesslist[-(i + 1)][0].score}')
        # colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # print(i, -(i + 1), len(fitnesslist))
        # ships.append(Ship(vardict, colour, fitnesslist[-(i + 1)][0].net))
    else:
        loadall()
    if highscore < fitnesslist[-1][1]:
        highscore = fitnesslist[-1][1]
    print(f'High Score: {highscore}')
    lasthighscore = fitnesslist[-1][1]
    fitnesslist = []


def saveall():
    global population, ships, gen
    for i in os.listdir(f'{os.getcwd()}/SavedNets'):
        os.remove(f'{os.getcwd()}/SavedNets/{i}')
    for i in range(len(ships)):
        population.filesave(ships[i].net, ships[i].score, gen, i)


def loadall():
    global population, ships, gen
    ships = []
    files = os.listdir(f'{os.getcwd()}/SavedNets')
    for i in range(popsize):
        colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        ships.append(Ship(vardict, colour, population.fileload(files[i])))


while 1:
    vardict = {
        'screen': screen,
        'aster_convert': aster_convert,
        'scr_w': scr_w,
        'scr_h': scr_h,
        'asteroid_spawn': asteroid_spawn,
        'spawnx': spawnx,
        'spawny': spawny,
        'score': score,
        'costumes': costumes,
        'ship_move': ship_move,
        'ship_still': ship_still
    }
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
    if mode == 'menu':
        screen.fill((0, 0, 0))
        txt = font.render(str('start'), True, (255, 255, 255))
        txtx = scr_w / 2 - txt.get_width() / 2
        txty = scr_h / 3 * 2 - txt.get_height()
        buttonrect = pygame.Rect((txtx, txty), txt.get_size())
        pygame.draw.rect(screen, (255, 255, 255), buttonrect, 1)
        screen.blit(txt, (txtx, txty))
        if pygame.mouse.get_pressed()[0] and buttonrect.collidepoint(pygame.mouse.get_pos()):
            mode = 'game'
    if mode == 'game':
        i = 0
        while 1:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    for i in range(len(ships)):
                        ships[i].shoot()
                if event.type == KEYDOWN and event.key == K_s:
                    timeout = 117200
                if event.type == KEYDOWN and event.key == K_d:
                    drawnum -= 1
                if event.type == KEYDOWN and event.key == K_e:
                    drawnum += 1
                if event.type == KEYDOWN and event.key == K_r:
                    if drawrays == True:
                        drawrays = False
                    else:
                        drawrays = True
                if event.type == KEYDOWN and event.key == K_i:
                    if dispinfo == True:
                        dispinfo = False
                    else:
                        dispinfo = True
                if event.type == KEYDOWN and event.key == K_l:
                    loadall()
                if event.type == KEYDOWN and event.key == K_o:
                    saveall()

            # pressed_keys = pygame.key.get_pressed()
            # if pressed_keys[K_SPACE]:
            #     shots.append(Shot(vardict, ship))
            screen.fill((0, 0, 0))
            i = 0
            while i < len(ships):
                if i < drawnum:
                    ships[i].draw(drawrays)
                    drawbool = True
                else:
                    drawbool = False
                ships[i].gametick(drawbool)  # gametick first to create asteroids before raycast()
                if i == 0:
                    ships[i].move(dispinfo)  # draws the input values of first net
                else:
                    ships[i].move()
                ships[i].off_screen()
                if ships[i].hit() or timeout >= 117200:  # timeout of 2 mins Without time.time() to stop warp
                    fitnesslist.append((ships[i], ships[i].score))
                    del ships[i]
                i += 1
            i = 0
            if len(ships) == 0:
                reset()

            if dispinfo is True:
                txt = font2.render(f'Score: {str(ships[0].score)}', True, (255, 255, 255))
                screen.blit(txt, (0, 0))
                drop = txt.get_height() + 5
                txt = font2.render(f'Gen: {str(gen)}', True, (255, 255, 255))
                screen.blit(txt, (0, drop))
                txt = font2.render(f'ShipNum: {str(len(ships))}', True, (255, 255, 255))
                screen.blit(txt, (0, drop * 2))
                txt = font2.render(f'DrawNum: {str(drawnum)}', True, (255, 255, 255))
                screen.blit(txt, (0, drop * 3))
                txt = font2.render(f'DrawRays: {str(drawrays)}', True, (255, 255, 255))
                screen.blit(txt, (0, drop * 4))
                txt = font2.render(f'HighScore: {str(highscore)}', True, (255, 255, 255))
                screen.blit(txt, (0, drop * 5))
                txt = font2.render(f'LastHighScore: {str(lasthighscore)}', True, (255, 255, 255))
                screen.blit(txt, (0, drop * 6))
                txt = font2.render(f'AvgFPS: {int(timeout / (time.time() - starttime))}', True, (255, 255, 255))
                screen.blit(txt, (0, drop * 7))
                # txt = font2.render(f'LastNetVars: {ships[-1].movements}', True, (255, 255, 255))
                # screen.blit(txt, (0, drop * 8))
                population.draw_net(ships[0].getnet(), screen, scr_w - 20, 20, 20, 30, 7)
            pygame.display.update()
            # if len(asteroids) == 0:
            #     asteroid_spawn = time.time()
            timeout += 1  # for the clock
    pygame.display.update()
