import pygame as pg
import os, random,math,json
from pprint import pprint
from machine import Machine
from player import Player
from wiring import WiringNet

with open(os.path.join("json","splashes.json"), "r") as f:
    splashes = json.load(f)

version = "0.1_stable"
sprite_size=1
screen_size=(20*(32*sprite_size),20*(32*sprite_size))
display = pg.display.set_mode(screen_size,pg.RESIZABLE, pg.SRCALPHA)
clock = pg.time.Clock()
pg.init()
pg.display.set_caption(f"am_flatworld_{version} - {random.choice(splashes)}")

working = True
world = []
tick = 0
fullscreen = False

for i in range(0,256): 
    for i1 in range(0,256):
        world.append({"block":"stone"})

for i in range(0,random.randint(40,79)):
    pos=[random.randint(0,255),random.randint(0,255)]
    radius = random.randint(1,9)
    for i1 in range(0,radius):
        for i2 in range(0,radius):
            world[(pos[0]+i1 if pos[0]+i1<= 255 else 255)*256+(pos[1]+i2 if pos[1]+i2<= 255 else 255)]={"block":"grass"}

with open(os.path.join("json","buildings.json"), 'r') as f:
    buildings = json.load(f)
io_blocks = []
for i in buildings:
    if buildings[i]["io"]: io_blocks.append(i)

timers = {}

player = Player(display,[256,256],sprite_size,(0,0))
old_k =[]
pg.mouse.set_visible(False)
machinery_list = {}
wire_nets = []
player.inv[1]={"item":"metal_ore","amount":50}
player.inv[2]={"item":"coal_ore","amount":50}
player.inv[0]={"item":"simple_motor_part","amount":1}
player.inv[7]={"item":"castmold_rod","amount":1}
player.inv[6]={"item":"castmold_plate","amount":1}
player.inv[5]={"item":"simple_turbine_part","amount":1}
player.inv[10]={"item":"copper_wire","amount":2}
player.inv[11]={"item":"metal_rod","amount":1}
#world[256*1+4] = {"block":"conveyor_belt","rotation":90}
#world[256*2+3] = {"block":"conveyor_belt","rotation":0}
world[256*5+5] = {"block":"conveyor_belt","rotation":180}
machinery_list["5_5"]=(Machine([5,5],"conveyor_belt",{"in":["","","",""]}))
'''
world[256*2+5] = {"block":"conveyor_belt","rotation":270}
machinery_list.append(Machine([5,2],"conveyor_belt",{"in":["","","",""]}))
world[256+4] = {"block":"conveyor_belt","rotation":180}
machinery_list.append(Machine([4,1],"conveyor_belt",{"in":["","","",""]}))
'''
machinery_list["5_5"].timer[0]=60
machinery_list["5_5"].inv["in"][0]="metal_ore"
#world[256*3+4] = {"block":"conveyor_belt","rotation":270}
#world[256*4+4] = {"block":"conveyor_belt","rotation":90}
#world[261] = {"block":"conveyor_belt","rotation":0}
#world[262] = {"block":"conveyor_belt","rotation":180}

for i in range(0,10):
    wire_nets.append(WiringNet())

if __name__ == "__main__":
    while working:
        changes = ([],[],[],[],[])
        evt_k={}
        m_evt = False
        for evt in pg.event.get():
            if evt.type == pg.QUIT or not working:
                pg.quit()
                working = False  
            elif evt.type == pg.KEYDOWN:
                evt_k = pg.key.get_pressed()
            elif evt.type == pg.MOUSEBUTTONDOWN:
                m_evt = True
        changes = player.gamecycle(working,display, fullscreen,clock,tick,evt_k,machinery_list, world,screen_size,m_evt,wire_nets)
        if changes != None:
            for change in changes[0]:
                world[change[0]] =change[1]
            for change in changes[1]:
                machinery_list[change[0]] =change[1]
            for change in changes[2]:
                machinery_list.pop(change)
            for change in changes[3]:
                machinery_list[change[0]] = change[1]
            wire_nets = changes[4]
        
        for machine in machinery_list:
            machinery_list[machine].update(world,[256,256],machinery_list,60/clock.get_fps() if clock.get_fps() != 0 else 1, io_blocks)
        clock.tick()
        tick += 60/clock.get_fps() if clock.get_fps() != 0 else 1
        for timer in timers:
            if timers[timer] >0: timers[timer]-=(60/clock.get_fps() if clock.get_fps() != 0 else 1)
        if tick >= 60: 
            tick -= 60
            for net in wire_nets:
                machinery_list = net.update(machinery_list)