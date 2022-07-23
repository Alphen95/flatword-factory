import copy
import pygame as pg
import math, os, json
from machine import Machine
from wiring import WiringNet

class Player():
    def __init__(self,surface,world_dimensions,multiplier,draw_offset):
        self.multiplier = multiplier
        self.world_dimensions = world_dimensions
        self.pos = [0,0]
        self.draw_offset = draw_offset
        self.player_pos = [0,0]
        self.offset = [0,0]
        self.player_offset = [0,0]
        self.sprites = {}
        self.surface = surface
        self.mode = "game"
        self.player_rotation = 0
        self.player_anim_state = 0
        self.cursor_state = "none"
        self.user_clock = pg.time.Clock()
        self.inv = []
        self.tick = 0
        self.build_id = 0
        self.inventory_state = "none"
        self.inventory_tile = "none"
        self.inventory_cell = {}
        self.build_blocks = ["stone","grass"]
        self.openable_machines = ["furnace","storage_box","generator"]
        self.font = pg.font.Font("font.ttf",24)
        self.small_font = pg.font.Font("font.ttf",16)
        self.explosions = []
        block_texture_filenames = os.listdir("res")
        for texture_filename in block_texture_filenames:
            if not(texture_filename in [".DS_Store",".vscode"]):
                self.sprites[texture_filename[:-4]] = pg.image.load(os.path.join("res",texture_filename)).convert()
        self.sprites["grass_base"] = self.sprites["grass"].subsurface(0,0,16,16)
        self.sprites["grass_cut_corner"] = self.sprites["grass"].subsurface(16,0,16,16)
        self.sprites["grass_side"] = self.sprites["grass"].subsurface(32,0,16,16)
        self.sprites["grass_empty_corner"] = self.sprites["grass"].subsurface(48,0,16,16)
        self.sprites["grass_full_corner"] = self.sprites["grass"].subsurface(64,0,16,16)
        self.sprites["grass_overlay"] = self.sprites["grass"].subsurface(80,0,16,16)
        self.sprites["grass_outer_corner"] = self.sprites["grass"].subsurface(96,0,16,16)
        self.sprites["ui_corner"] = self.sprites["ui"].subsurface(0,0,16,16).convert()
        self.sprites["ui_side"] = self.sprites["ui"].subsurface(16,0,16,16).convert()
        self.sprites["ui_center"] = self.sprites["ui"].subsurface(32,0,16,16).convert()
        self.sprites["ui_inv_tile"] = self.sprites["ui"].subsurface(48,0,16,16).convert()
        self.sprites["ui_cursor"] = self.sprites["ui"].subsurface(64,0,16,16).convert()
        self.sprites["ui_cursor_delete"] = self.sprites["ui"].subsurface(80,0,16,16).convert()
        self.sprites["ui_cursor_cable"] = self.sprites["ui"].subsurface(96,0,16,16).convert()
        self.sprites["ui_conv0"] = self.sprites["conveyor_wireframe"].subsurface(0,0,16,16).convert()
        self.sprites["ui_conv90"] = self.sprites["conveyor_wireframe"].subsurface(16,0,16,21).convert()
        self.sprites["ui_conv270"] = self.sprites["conveyor_wireframe"].subsurface(32,0,16,21).convert()
        self.sprites["s_conveyor_belt_0"] = self.sprites["conveyor_belt"].subsurface(0,0,16,16).convert()
        self.sprites["s_conveyor_belt_vert"] = self.sprites["conveyor_belt"].subsurface(16,0,16,21).convert()
        self.sprites["s_conveyor_belt_turn1"] = self.sprites["conveyor_belt"].subsurface(32,0,16,21).convert()
        self.sprites["s_conveyor_belt_turn2"] = self.sprites["conveyor_belt"].subsurface(48,0,16,21).convert()
        self.sprites["s_conveyor_part"] = self.sprites["conveyor_belt"].subsurface(64,0,16,16).convert()
        self.sprites["s_conveyor_belt_side_bottom"] = self.sprites["conveyor_belt"].subsurface(80,0,16,16).convert()
        self.sprites["furnace_part1"] = self.sprites["furnace"].subsurface(0,0,32,32).convert()
        self.sprites["furnace_part3"] = self.sprites["furnace"].subsurface(32,0,32,32).convert()
        self.sprites["furnace_part2"] = self.sprites["furnace"].subsurface(0,32,32,32).convert()
        self.sprites["furnace_part4"] = self.sprites["furnace"].subsurface(32,32,32,32).convert()
        self.sprites["processing_overlay"] = self.sprites["processing"].subsurface(0,0,16,16).convert()
        self.sprites["processing_base"] = self.sprites["processing"].subsurface(16,0,16,16).convert()
        self.sprites["recepie_description_top"] = self.sprites["recepie_description"].subsurface(0,0,64,16).convert()
        self.sprites["recepie_description_middle"] = self.sprites["recepie_description"].subsurface(64,0,64,16).convert()
        self.sprites["boom1"] = self.sprites["exsplosion"].subsurface(0,0,32,32).convert()
        self.sprites["boom2"] = self.sprites["exsplosion"].subsurface(32,0,32,32).convert()
        self.sprites["boom3"] = self.sprites["exsplosion"].subsurface(64,0,32,32).convert()
        self.sprites["boom4"] = self.sprites["exsplosion"].subsurface(96,0,32,32).convert()
        self.sprites["boom5"] = self.sprites["exsplosion"].subsurface(128,0,32,32).convert()
        self.sprites["boom6"] = self.sprites["exsplosion"].subsurface(160,0,32,32).convert()
        self.sprites["power_ui_counter_edge"] = self.sprites["powernet_graphics"].subsurface(0,0,16,16).convert()
        self.sprites["power_ui_counter"] = self.sprites["powernet_graphics"].subsurface(16,0,16,16).convert()
        self.sprites["power_ui_counter_1"] = self.sprites["powernet_graphics"].subsurface(32,0,16,16).convert()
        self.sprites["power_ui_counter_2"] = self.sprites["powernet_graphics"].subsurface(48,0,16,16).convert()
        self.sprites["power_ui_counter_3"] = self.sprites["powernet_graphics"].subsurface(64,0,16,16).convert()
        self.sprites["power_ui_counter_4"] = self.sprites["powernet_graphics"].subsurface(80,0,16,16).convert()
        self.sprites["power_ui_counter_5"] = self.sprites["powernet_graphics"].subsurface(96,0,16,16).convert()
        self.sprites["power_ui_counter_6"] = self.sprites["powernet_graphics"].subsurface(112,0,16,16).convert()
        self.sprites["power_ui_counter_7"] = self.sprites["powernet_graphics"].subsurface(128,0,16,16).convert()
        self.sprites["power_ui_counter_8"] = self.sprites["powernet_graphics"].subsurface(144,0,16,16).convert()
        self.sprites["power_ui_counter_9"] = self.sprites["powernet_graphics"].subsurface(160,0,16,16).convert()
        self.sprites["power_ui_counter_0"] = self.sprites["powernet_graphics"].subsurface(176,0,16,16).convert()
        self.sprites["power_ui_arrow"] = self.sprites["powernet_graphics"].subsurface(192,0,16,16).convert()

        self.sprites["r_conveyor_belt_0"] = self.sprites["conveyor_belt"].subsurface(0,0,16,16).convert()
        self.sprites["r_conveyor_belt_vert"] = self.sprites["conveyor_belt"].subsurface(16,0,16,21).convert()
        self.sprites["r_conveyor_belt_side_bottom"] = self.sprites["conveyor_belt"].subsurface(16,16,16,5).convert()
        self.sprites["r_conveyor_belt_turn1"] = self.sprites["conveyor_belt"].subsurface(32,0,16,21).convert()
        self.sprites["r_conveyor_belt_turn1_part1"] = self.sprites["conveyor_belt"].subsurface(36,0,9,10).convert()
        self.sprites["r_conveyor_belt_turn2"] = self.sprites["conveyor_belt"].subsurface(48,0,16,21).convert()
        self.sprites["r_conveyor_belt_turn2_part1"] = self.sprites["conveyor_belt"].subsurface(51,5,10,11).convert()
        self.sprites["r_conveyor_belt_turn2_part2"] = self.sprites["conveyor_belt"].subsurface(48,15,16,6).convert()
        self.sprites["r_conveyor_part"] = self.sprites["conveyor_belt"].subsurface(64,0,16,16).convert()
        self.sprites["r_conveyor_belt_part_side"] = self.sprites["conveyor_belt"].subsurface(80,0,16,16).convert()
        item_names=["simple_motor_part","simple_turbine_part","copper_wire","water_tank","energy","simple_mechanic_part","simple_assembler","metal_plate","simple_casing","","metal_rod","metal_ore","coal_ore","copper_ore","","copper_rod","conveyor_part","castmold_plate","castmold_rod",""]
        for texture_name in self.sprites:
            self.sprites[texture_name].set_colorkey((0,0,0))
        self.sprites["conveyor_belt_0"] = {}
        self.sprites["conveyor_belt_vert_down"] = {}
        self.sprites["conveyor_belt_vert_up"] = {}
        self.sprites["conveyor_belt_side_vert"] = {}
        self.sprites["conveyor_belt_vert_side"] = {}
        self.sprites["conveyor_belt_side_vert_down"] = {}
        self.sprites["conveyor_belt_vert_down_side"] = {}

        for tick in range(0,60):
            offset = int(32/60*tick/4)
            surface = pg.Surface((32,42))
            surface.set_colorkey((0,0,0))
            block_surface = pg.Surface((32,42))
            block_surface.set_colorkey((0,0,0))
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_belt_0"],(int(32*self.multiplier),int(32*self.multiplier))
                ),(0,10)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_part"],(int(32*self.multiplier),int(32*self.multiplier))
                ),(offset- (0 if offset < 32 else 40)*self.multiplier,10*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_part"],(int(32*self.multiplier),int(32*self.multiplier))
                ),((offset+8- (0 if offset+8 < 32 else 40))*self.multiplier,10*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_part"],(int(32*self.multiplier),int(32*self.multiplier))
                ),((offset+16- (0 if offset+16 < 32 else 40))*self.multiplier,10*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_part"],(int(32*self.multiplier),int(32*self.multiplier))
                ),((offset+24- (0 if offset+24 < 32 else 40))*self.multiplier,10*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_part"],(int(32*self.multiplier),int(32*self.multiplier))
                ),((offset-8- (0 if offset-8 < 32 else 40))*self.multiplier,10*self.multiplier)
            )
            surface.blit(block_surface,(0,0))
            self.sprites["conveyor_belt_0"][offset] = surface
        for tick in range(0,60):
            offset = int(32/60*tick/4)
            surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            surface.set_colorkey((0,0,0))
            block_surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            block_surface.set_colorkey((0,0,0))
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_belt_vert"],(int(32*self.multiplier),int(40*self.multiplier))
                ),(0,0)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(0+offset-(0 if 0+offset < 32 else 40))*self.multiplier)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(8+offset-(0 if 8+offset < 32 else 40))*self.multiplier)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(16+offset-(0 if 16+offset < 32 else 40))*self.multiplier)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(24+offset-(0 if 24+offset < 32 else 40))*self.multiplier)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(-8+offset-(0 if -8+offset < 32 else 40))*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_belt_side_bottom"],(int(32*self.multiplier),int(10*self.multiplier))
                ),(0,32*self.multiplier)
            )
            surface.blit(block_surface,(0,0))
            self.sprites["conveyor_belt_vert_down"][offset] = surface
        for tick in range(0,60):
            offset = int(32/60*tick/4)
            surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            surface.set_colorkey((0,0,0))
            block_surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            block_surface.set_colorkey((0,0,0))
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_belt_vert"],(int(32*self.multiplier),int(40*self.multiplier))
                ),(0,0)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,0-offset+(0 if 0-offset >= -8 else 40)-24)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,8-offset+(0 if 8-offset >= -8 else 40)-24)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,16-offset+(0 if 16-offset >= -8 else 40)-24)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,24-offset+(0 if 24-offset >= -8 else 40)-24)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,32-offset+(0 if 32-offset >= -8 else 40)-24)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_belt_side_bottom"],(int(32*self.multiplier),int(10*self.multiplier))
                ),(0,32)
            )
            surface.blit(block_surface,(0,0))
            self.sprites["conveyor_belt_vert_up"][offset] = surface

        for tick in range(0,60):
            offset = int(32/60*tick/4)
            surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            surface.set_colorkey((0,0,0))
            block_surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            block_surface.set_colorkey((0,0,0))
            block_surface.blit(
                pg.transform.scale(pg.transform.flip(
                    self.sprites["r_conveyor_belt_turn2"],True,False),(int(32*self.multiplier),int(42*self.multiplier))
                ),(0,0)
            )
            block_surface.blit(
                    pg.transform.scale(
                            self.sprites["r_conveyor_belt_part_side"],(int(32*self.multiplier),int(32*self.multiplier))
                    ),(26*self.multiplier,10*self.multiplier)
                )
            block_surface.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((24-offset+(0 if 24-offset > 16 else 40)-32)*self.multiplier,10*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((32-offset+(0 if 32-offset > 16 else 40)-32)*self.multiplier,10*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((40-offset+(0 if 40-offset > 16 else 40)-32)*self.multiplier,10*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((48-offset+(0 if 48-offset > 16 else 40)-32)*self.multiplier,10*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((56-offset+(0 if 56-offset > 16 else 40)-32)*self.multiplier,10*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(pg.transform.flip(
                        self.sprites["r_conveyor_belt_turn2_part1"],True,False),(int(20*self.multiplier),int(22*self.multiplier))
                ),(6,10)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,0-offset+(0 if 0-offset >= -8 else 40)-24)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,8-offset+(0 if 8-offset >= -8 else 40)-24)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,16-offset+(0 if 16-offset >= -8 else 40)-24)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,24-offset+(0 if 24-offset >= -8 else 40)-24)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,32-offset+(0 if 32-offset >= -8 else 40)-24)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_belt_turn2_part2"],(int(32*self.multiplier),int(12*self.multiplier))
                ),(6,30)
            )
            surface.blit(block_surface,(0,0))
            self.sprites["conveyor_belt_side_vert"][offset] = surface

        for tick in range(0,60):
            offset = int(32/60*tick/4)
            surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            surface.set_colorkey((0,0,0))
            block_surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            block_surface2 = pg.Surface((24*self.multiplier,42*self.multiplier))
            block_surface.set_colorkey((0,0,0))
            block_surface2.set_colorkey((0,0,0))
            block_surface.blit(
                pg.transform.scale(
                    self.sprites["r_conveyor_belt_turn2"],(int(32*self.multiplier),int(42*self.multiplier))
                ),(0,0)
            )
            block_surface2.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((32-offset+ (0 if 32-offset > -7 else 40)-24)*self.multiplier,10*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((24-offset+ (0 if 24-offset > -7 else 40)-24)*self.multiplier,10*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((16-offset+ (0 if 16-offset > -7 else 40)-24)*self.multiplier,10*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((8-offset+ (0 if 8-offset > -7 else 40)-24)*self.multiplier,10*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((0-offset+ (0 if 0-offset > -7 else 40)-24)*self.multiplier,10*self.multiplier)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(0+offset-(0 if 0+offset < 32 else 40))*self.multiplier)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(8+offset-(0 if 8+offset < 32 else 40))*self.multiplier)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(16+offset-(0 if 16+offset < 32 else 40))*self.multiplier)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(24+offset-(0 if 24+offset < 32 else 40))*self.multiplier)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(-8+offset-(0 if -8+offset < 32 else 40))*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(pg.transform.flip(
                        self.sprites["r_conveyor_belt_turn2_part1"],False,False),(int(20*self.multiplier),int(22*self.multiplier))
                ),(6,10)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_belt_turn2_part2"],(int(32*self.multiplier),int(12*self.multiplier))
                ),(0,30)
            )
            surface.blit(block_surface,(0,0))
            surface.blit(block_surface2,(0,0))
            self.sprites["conveyor_belt_vert_side"][offset] = surface
        
        for tick in range(0,60):
            offset = int(32/60*tick/4)
            surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            surface.set_colorkey((0,0,0))
            block_surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            block_surface2 = pg.Surface((24*self.multiplier,42*self.multiplier))
            block_surface.set_colorkey((0,0,0))
            block_surface2.set_colorkey((0,0,0))
            block_surface.blit(
                pg.transform.scale(
                    self.sprites["r_conveyor_belt_turn1"],(int(32*self.multiplier),int(42*self.multiplier))
                ),(0,10)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_part"],(int(32*self.multiplier),int(32*self.multiplier))
                ),(0+offset-(0 if 0+offset < 16 else 40),10)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_part"],(int(32*self.multiplier),int(32*self.multiplier))
                ),(-8+offset-(0 if -8+offset < 16 else 40),10)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_part"],(int(32*self.multiplier),int(32*self.multiplier))
                ),(-16+offset-(0 if -16+offset < 16 else 40),10)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_part"],(int(32*self.multiplier),int(32*self.multiplier))
                ),(-24+offset-(0 if -24+offset < 16 else 40),10)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_part"],(int(32*self.multiplier),int(32*self.multiplier))
                ),(-32+offset-(0 if -32+offset < 16 else 40),10)
            )
            block_surface2.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(-3+offset-(0 if -3+offset < 32 else 40))*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(5+offset-(0 if 5+offset < 32 else 40))*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(13+offset-(0 if 13+offset < 32 else 40))*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(21+offset-(0 if 21+offset < 32 else 40))*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),90),(6*self.multiplier,(-11+offset-(0 if -11+offset < 32 else 40))*self.multiplier)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_belt_turn1_part1"],(int(18*self.multiplier),int(22*self.multiplier))
                ),(8,10)
            )

            block_surface2.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_belt_side_bottom"],(int(32*self.multiplier),int(10*self.multiplier))
                ),(0,20)
            )
            surface.blit(block_surface,(0,0))
            surface.blit(block_surface2,(0,12))
            self.sprites["conveyor_belt_side_vert_down"][offset] = surface

        for tick in range(0,60):
            offset = int(32/60*tick/4)
            surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            surface.set_colorkey((0,0,0))
            block_surface = pg.Surface((32*self.multiplier,42*self.multiplier))
            block_surface2 = pg.Surface((24*self.multiplier,42*self.multiplier))
            block_surface.set_colorkey((0,0,0))
            block_surface2.set_colorkey((0,0,0))
            block_surface.blit(
                pg.transform.scale(
                    self.sprites["r_conveyor_belt_turn1"],(int(32*self.multiplier),int(42*self.multiplier))
                ),(0,10)
            )
            block_surface2.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((32-offset+ (0 if 32-offset > -7 else 40)-24)*self.multiplier,10*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((24-offset+ (0 if 24-offset > -7 else 40)-24)*self.multiplier,10*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((16-offset+ (0 if 16-offset > -7 else 40)-24)*self.multiplier,10*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((8-offset+ (0 if 8-offset > -7 else 40)-24)*self.multiplier,10*self.multiplier)
            )
            block_surface2.blit(
                pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                ),((0-offset+ (0 if 0-offset > -7 else 40)-24)*self.multiplier,10*self.multiplier)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,-1-offset+(0 if -1-offset >= -8 else 40)-8)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,7-offset+(0 if 7-offset >= -8 else 40)-8)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,15-offset+(0 if 15-offset >= -8 else 40)-8)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,23-offset+(0 if 23-offset >= -8 else 40)-8)
            )
            block_surface.blit(
                pg.transform.rotate(pg.transform.scale(
                        pg.transform.flip(self.sprites["r_conveyor_part"],True,False),(int(32*self.multiplier),int(28*self.multiplier))
                ),-90),(-2,31-offset+(0 if 31-offset >= -8 else 40)-8)
            )
            block_surface.blit(
                pg.transform.scale(
                        self.sprites["r_conveyor_belt_turn1_part1"],(int(18*self.multiplier),int(20*self.multiplier))
                ),(8,10)
            )
            surface.blit(block_surface,(0,0))
            surface.blit(block_surface2,(0,0))
            self.sprites["conveyor_belt_vert_down_side"][offset] = surface

        dimensions = [5,4]
        for y in range(0,dimensions[1]):
            for x in range(0,dimensions[0]):
                self.sprites["item_{}".format(item_names[x+y*dimensions[0]])] = self.sprites["items"].subsurface(32*x,32*y,32,32)
                self.sprites["item_{}".format(item_names[x+y*dimensions[0]])].convert()
                self.sprites["item_{}".format(item_names[x+y*dimensions[0]])].set_colorkey([0,0,0])
                self.sprites["item_alpha{}".format(item_names[x+y*dimensions[0]])] = self.sprites["items"].subsurface(32*x,32*y,32,32)
                self.sprites["item_alpha{}".format(item_names[x+y*dimensions[0]])].convert()
        with open(os.path.join("json","descriptions.json"), 'r') as f:
            self.descriptions = json.load(f)
        with open(os.path.join("json","recepies.json"), 'r') as f:
            self.recepies = json.load(f)
        with open(os.path.join("json","buildings.json"), 'r') as f:
            self.buildings = json.load(f)
        for i in range(0,24): self.inv.append({})
        self.io_blocks = []
    
    def draw(self,m_pos,tick,machinery_list,world):
        self.surface.fill((160,160,160))
        for sel_y in range(self.pos[1],self.pos[1]+21):
            for sel_x in range(self.pos[0],self.pos[0]+21):
                x = sel_x - self.pos[0]
                y = sel_y - self.pos[1]
                if x >= 0 or x <= 255 or y >= 0 or y <= 255:
                    block = world[sel_x+sel_y*256]
                    sprite = block["block"]
                    if sprite not in ["","stone"]:
                        draw_x = (x*32-self.offset[0])*self.multiplier+self.draw_offset[0]
                        draw_y = (y*32-self.offset[1]-10)*self.multiplier+self.draw_offset[1]
                        if sprite != "grass" and sprite:
                            machine_block = None
                            if str(sel_x)+"_"+str(sel_y) in machinery_list:
                                machine_block = machinery_list[str(sel_x)+"_"+str(sel_y)]
                            if "rotation" in block:
                                rotated = True
                            else: rotated = False
                            if sprite == "furnace":
                                self.surface.blit(
                                    pg.transform.scale(
                                            self.sprites["furnace_part1"],(int(32*self.multiplier),int(32*self.multiplier))
                                    ),(draw_x,draw_y+10)
                                )
                            elif "link_obj" in sprite:
                                self.surface.blit(
                                    pg.transform.scale(
                                            self.sprites[sprite[9:]],(int(32*self.multiplier),int(32*self.multiplier))
                                    ),(draw_x,draw_y+10)
                                )
                            elif sprite == "conveyor_belt":
                                side1 = [True,world[sel_x+(sel_y-1)*256]["rotation"]] if sel_y > 0 and world[sel_x+(sel_y-1)*256]["block"]=="conveyor_belt" else [False,0]
                                side2 = [True,world[(sel_x+1)+sel_y*256]["rotation"]] if sel_x < 255 and world[(sel_x+1)+sel_y*256]["block"]=="conveyor_belt" else [False,0]
                                side3 = [True,world[sel_x+(sel_y+1)*256]["rotation"]] if sel_y < 255 and world[sel_x+(sel_y+1)*256]["block"]=="conveyor_belt" else [False,0]
                                side4 = [True,world[(sel_x-1)+sel_y*256]["rotation"]] if sel_x > 0 and world[(sel_x-1)+sel_y*256]["block"]=="conveyor_belt" else [False,0]
                                #rot0 , слева направо.

                                if block["rotation"] == 0 and (side4==[True,0] and side1==[True,90] or side4==[True,0] and side3==[True,270] or not side1==[True,90] and not side3==[True,270] or side1==[True,90] and side3==[True,270]):
                                    self.surface.blit(
                                        pg.transform.scale(
                                                self.sprites["conveyor_belt_0"][int(32/60*tick/4)],(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[0])*(8/60)*self.multiplier-4,draw_y+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[1])*(8/60)*self.multiplier+4,draw_y+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[2])*(8/60)*self.multiplier+12,draw_y+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[3])*(8/60)*self.multiplier+20,draw_y+8*self.multiplier)
                                        )
                                #rot180 справа налево.

                                elif block["rotation"] == 180 and (side2==[True,180] and side1==[True,90] or side2==[True,180] and side3==[True,270] or not side3==[True,270] and not side1==[True,90] or side3==[True,270] and side1 ==[True,90]):
                                    self.surface.blit(
                                        pg.transform.scale(pg.transform.flip(
                                                self.sprites["conveyor_belt_0"][int(32/60*tick/4)],True,False),(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[0])*(8/60)*self.multiplier-4),draw_y+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[1])*(8/60)*self.multiplier+5),draw_y+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[2])*(8/60)*self.multiplier+14),draw_y+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[3])*(8/60)*self.multiplier+23),draw_y+8*self.multiplier)
                                        )

                                #rot90 сверху вниз
                                elif block["rotation"] == 90 and (side1==[True,90] and side4==[True,0] or side1==[True,90] and side2==[True,180] or not side4==[True,0] and not side2==[True,180]):
                                    self.surface.blit(
                                        pg.transform.scale(
                                                self.sprites["conveyor_belt_vert_down"][int(32/60*tick/4)],(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y+0)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[0])*(8/60)*self.multiplier-4-8)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[1])*(8/60)*self.multiplier+5-8)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[2])*(8/60)*self.multiplier+14-8)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[3])*(8/60)*self.multiplier+23-8)
                                        )

                                #rot270 снизу вверх
                                elif block["rotation"] == 270 and (side3==[True,270] and side4==[True,0] or side3==[True,270] and side2==[True,180] or not side4==[True,0] and not side2==[True,180]):
                                    self.surface.blit(
                                        pg.transform.scale(
                                                self.sprites["conveyor_belt_vert_up"][int(32/60*tick/4)],(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y+0)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[0])*(8/60)*self.multiplier+5+10)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[1])*(8/60)*self.multiplier-4+10)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[2])*(8/60)*self.multiplier-13+10)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[3])*(8/60)*self.multiplier-22+10)
                                        )
                                #rot270 поворот слева вверх
                                elif block["rotation"] == 270 and side2 == [True,180]:
                                    self.surface.blit(
                                        pg.transform.scale(
                                            self.sprites["conveyor_belt_side_vert"][int(32/60*tick/4)],(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y+0)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[0])*(8/60)*self.multiplier-4),draw_y+8*self.multiplier+10)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[1])*(8/60)*self.multiplier+5),draw_y+8*self.multiplier+10)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[2])*(8/60)*self.multiplier-13)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[3])*(8/60)*self.multiplier-22)
                                        )

                                #rot180 сверху налево
                                elif block["rotation"] == 180 and side1 == [True,90]:
                                    self.surface.blit(
                                        pg.transform.scale(pg.transform.flip(
                                            self.sprites["conveyor_belt_vert_side"][int(32/60*tick/4)],False,False),(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y+0)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[0])*(16/60)*self.multiplier-4-8)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[1])*(12/60)*self.multiplier+12-8)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[2])*(8/60)*self.multiplier+14),draw_y+8*self.multiplier+10)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[3])*(8/60)*self.multiplier+23),draw_y+8*self.multiplier+10)
                                        )
                                
                                # сверху направо

                                elif block["rotation"] == 0 and side1 == [True,90]:
                                    self.surface.blit(
                                        pg.transform.scale(pg.transform.flip(
                                            self.sprites["conveyor_belt_vert_side"][int(32/60*tick/4)],True,False),(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y+0)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(12*self.multiplier),int(12*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[0])*(8/60)*self.multiplier-4-8+10)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[1])*(16/60)*self.multiplier+5-8+10)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[2])*(8/60)*self.multiplier+14,draw_y+10+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[3])*(8/60)*self.multiplier+23,draw_y+10+8*self.multiplier)
                                        )
                                
                                #rot270 справа вверх
                                elif block["rotation"] == 270 and side4 == [True,0]:
                                    self.surface.blit(
                                        pg.transform.scale(pg.transform.flip(
                                            self.sprites["conveyor_belt_side_vert"][int(32/60*tick/4)],True,False),(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y+0)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[0])*(8/60)*self.multiplier-4,draw_y+10+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[1])*(8/60)*self.multiplier+5,draw_y+10+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[2])*(16/60)*self.multiplier-5+10)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[3])*(8/60)*self.multiplier-22+10)
                                        )
                                
                                #слева вниз

                                elif block["rotation"] == 90 and side4 == [True,0]:
                                    self.surface.blit(
                                        pg.transform.scale(
                                            self.sprites["conveyor_belt_side_vert_down"][int(32/60*tick/4)],(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[0])*(8/60)*self.multiplier-4,draw_y+10+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[1])*(8/60)*self.multiplier+5,draw_y+10+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[2])*(4/60)*self.multiplier+23-8+10)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[3])*(4/60)*self.multiplier+23-8+4+10)
                                        )
                                #снизу налево

                                elif block["rotation"] == 180 and side3 == [True,270]:
                                    self.surface.blit(
                                        pg.transform.scale(
                                            self.sprites["conveyor_belt_vert_down_side"][int(32/60*tick/4)],(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y+0)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[0])*(8/60)*self.multiplier+5)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[1])*(8/60)*self.multiplier-4)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[2])*(8/60)*self.multiplier+14),draw_y+10+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[3])*(8/60)*self.multiplier+23),draw_y+10+8*self.multiplier)
                                        )
                                    

                                #снизу направо
                                
                                elif block["rotation"] == 0 and side3 == [True,270]:
                                    self.surface.blit(
                                        pg.transform.scale(pg.transform.flip(
                                            self.sprites["conveyor_belt_vert_down_side"][int(32/60*tick/4)],True,False),(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y+0)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[0])*(8/60)*self.multiplier+5+10)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+26-(60-machine_block.timer[1])*(8/60)*self.multiplier-4+10)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[2])*(8/60)*self.multiplier+14,draw_y+10+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+(60-machine_block.timer[3])*(8/60)*self.multiplier+23,draw_y+10+8*self.multiplier)
                                        )

                                #справа вниз

                                elif block["rotation"] == 90 and side2 == [True,180]:
                                    self.surface.blit(
                                        pg.transform.scale(pg.transform.flip(
                                            self.sprites["conveyor_belt_side_vert_down"][int(32/60*tick/4)],True,False),(int(32*self.multiplier),int(42*self.multiplier))
                                        ),(draw_x+0,draw_y)
                                    )
                                    if machine_block.inv["in"][0] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][0]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[0])*(8/60)*self.multiplier-4),draw_y+10+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][1] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][1]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+26-((60-machine_block.timer[1])*(8/60)*self.multiplier+5),draw_y+10+8*self.multiplier)
                                        )
                                    if machine_block.inv["in"][2] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][2]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[2])*(4/60)*self.multiplier+23-8)
                                        )
                                    if machine_block.inv["in"][3] != "":
                                        self.surface.blit(
                                            pg.transform.scale(
                                                    self.sprites[f"item_{machine_block.inv['in'][3]}"],(int(18*self.multiplier),int(18*self.multiplier))
                                            ),(draw_x+10*self.multiplier,draw_y+(60-machine_block.timer[3])*(4/60)*self.multiplier+23-8+4)
                                        )
                            else:
                                self.surface.blit(
                                        pg.transform.scale(
                                                self.sprites[sprite+"_"+str(block["rotation"]) if rotated else sprite],(int(32*self.multiplier),int(32*self.multiplier))
                                        ),((x*32-self.offset[0])*self.multiplier+self.draw_offset[0],(y*32-self.offset[1])*self.multiplier+self.draw_offset[1])
                                    )
                        else:
                            side1 = True if sel_y > 0 and sel_x > 0 and world[(sel_x-1)+(sel_y-1)*256]["block"] == "grass" else False
                            side2 = True if sel_y > 0 and world[sel_x+(sel_y-1)*256]["block"] == "grass" else False
                            side3 = True if sel_y > 0 and sel_x < 255 and world[(sel_x+1)+(sel_y-1)*256]["block"] == "grass" else False
                            side4 = True if sel_x < 255 and world[(sel_x+1)+sel_y*256]["block"] == "grass" else False
                            side5 = True if sel_y < 255 and sel_x < 255 and world[(sel_x+1)+(sel_y+1)*256]["block"] == "grass" else False
                            side6 = True if sel_y < 255 and world[sel_x+(sel_y+1)*256]["block"] == "grass" else False
                            side7 = True if sel_y < 255 and sel_x > 0 and world[(sel_x-1)+(sel_y+1)*256]["block"] == "grass" else False
                            side8 = True if sel_x > 0 and world[(sel_x-1)+sel_y*256]["block"] == "grass" else False
                            self.surface.blit(
                                        pg.transform.scale(
                                                self.sprites["grass_base"],(int(32*self.multiplier),int(32*self.multiplier))
                                        ),(draw_x,draw_y+10)
                                    )
                            if side2:
                                self.surface.blit(
                                        pg.transform.scale(
                                                self.sprites["grass_side"],(int(32*self.multiplier),int(32*self.multiplier))
                                        ),(draw_x,draw_y+10)
                                    )
                            if side4:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_side"],270),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            if side6:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_side"],180),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            if side8:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_side"],90),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            if side2 and side3 and side4:
                                self.surface.blit(
                                        pg.transform.scale(
                                                self.sprites["grass_full_corner"],(int(32*self.multiplier),int(32*self.multiplier))
                                        ),(draw_x,draw_y+10)
                                    )
                            if side4 and side5 and side6:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_full_corner"],270),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            if side6 and side7 and side8:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_full_corner"],180),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            if side8 and side1 and side2:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_full_corner"],90),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            if side2 and not side3 and side4:
                                self.surface.blit(
                                        pg.transform.scale(
                                                self.sprites["grass_empty_corner"],(int(32*self.multiplier),int(32*self.multiplier))
                                        ),(draw_x,draw_y+10)
                                    )
                            if side4 and not side5 and side6:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_empty_corner"],270),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            if side6 and not side7 and side8:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_empty_corner"],180),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            if side8 and not side1 and side2:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_empty_corner"],90),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            if not side2 and not side4:
                                self.surface.blit(
                                        pg.transform.scale(
                                                self.sprites["grass_cut_corner"],(int(32*self.multiplier),int(32*self.multiplier))
                                        ),(draw_x,draw_y+10)
                                    )
                            if not side4 and not side6:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_cut_corner"],270),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            if not side6 and not side8:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_cut_corner"],180),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            if not side8 and not side2:
                                self.surface.blit(
                                        pg.transform.scale(pg.transform.rotate(
                                                self.sprites["grass_cut_corner"],90),(int(32*self.multiplier),int(32*self.multiplier)))
                                        ,(draw_x,draw_y+10)
                                    )
                            self.surface.blit(
                                        pg.transform.scale(
                                                self.sprites["grass_overlay"],(int(32*self.multiplier),int(32*self.multiplier))
                                        ),(draw_x,draw_y+10)
                                    )

            for boom in self.explosions:
                if boom[0] >= self.pos[0] and boom[0] <= self.pos[0]+20 and boom[1] >= self.pos[1] and boom[1] <= self.pos[1]+20:
                    draw_x = (boom[0] - self.pos[0]) * 32
                    draw_y = (boom[1] - self.pos[1]) * 32

                    i = int(boom[2] /20)+1
                    self.surface.blit(
                        pg.transform.scale(
                                self.sprites[f"boom{i}"],(int(32*self.multiplier),int(32*self.multiplier))
                        ),(draw_x,draw_y)
                    )

            x = self.player_pos[0]-self.pos[0]
            y = self.player_pos[1]-self.pos[1]
            self.surface.blit(
                        pg.transform.scale(pg.transform.rotate(
                                self.sprites["player"],self.player_rotation),(int(32*self.multiplier),int(32*self.multiplier))
                        ),((x*32+self.player_offset[0]%32-self.offset[0])*self.multiplier+self.draw_offset[0],(y*32+self.player_offset[1]%32-self.offset[1])*self.multiplier+self.draw_offset[1])
                    )
            pg.draw.rect(self.surface, (50, 50, 50), (0, 0, self.draw_offset[0], 32*20*self.multiplier+self.draw_offset[1]*2))
            pg.draw.rect(self.surface, (50, 50, 50), (self.draw_offset[0]+20*32*self.multiplier, 0, self.draw_offset[0], 32*20*self.multiplier+self.draw_offset[1]*2))
            pg.draw.rect(self.surface, (50, 50, 50), (0, 0, 32*20*self.multiplier+self.draw_offset[0]*2, self.draw_offset[1]))
        pg.draw.rect(self.surface, (50, 50, 50), (0, 32*20*self.multiplier+self.draw_offset[1], 32*20*self.multiplier+self.draw_offset[0]*2, self.draw_offset[1]))
        if self.inventory_state!="none":
            self.surface.blit(
                        pg.transform.scale(
                                self.sprites["inv"],(int(18*32*self.multiplier),int(18*32*self.multiplier))
                        ),((1*32)*self.multiplier+self.draw_offset[0],(1*32)*self.multiplier+self.draw_offset[1])
                    )
            if self.inventory_state=="player":
                for x in range(2,18,2):
                    for y in range(2,8,2):
                        cell = self.inv[int((x/2-1)+(y/2-1)*8)]
                        self.surface.blit(
                                pg.transform.scale(
                                        self.sprites["ui_inv_tile"],(int(32*self.multiplier),int(32*self.multiplier))
                                ),((x*32)*self.multiplier+self.draw_offset[0],(y*32)*self.multiplier+self.draw_offset[1])
                            )
                        self.surface.blit(
                                pg.transform.scale(pg.transform.rotate(
                                        self.sprites["ui_inv_tile"],270),(int(32*self.multiplier),int(32*self.multiplier))
                                ),(((x+1)*32)*self.multiplier+self.draw_offset[0],(y*32)*self.multiplier+self.draw_offset[1])
                            )
                        self.surface.blit(
                                pg.transform.scale(pg.transform.rotate(
                                        self.sprites["ui_inv_tile"],180),(int(32*self.multiplier),int(32*self.multiplier))
                                ),(((x+1)*32)*self.multiplier+self.draw_offset[0],((y+1)*32)*self.multiplier+self.draw_offset[1])
                            )
                        self.surface.blit(
                                pg.transform.scale(pg.transform.rotate(
                                        self.sprites["ui_inv_tile"],90),(int(32*self.multiplier),int(32*self.multiplier))
                                ),((x*32)*self.multiplier+self.draw_offset[0],((y+1)*32)*self.multiplier+self.draw_offset[1])
                            )
                        if cell != {} and cell["item"] != "":
                            self.surface.blit(
                                    pg.transform.scale(
                                            self.sprites[f"item_{cell['item']}"],(int(64*self.multiplier),int(64*self.multiplier))
                                    ),((x*32)*self.multiplier+self.draw_offset[0],(y*32)*self.multiplier+self.draw_offset[1])
                                )
                            if cell['amount'] > 1:
                                item_amonut = self.font.render(str(cell['amount']), False, (255, 255, 255))
                                self.surface.blit(item_amonut, ((x*32)*self.multiplier+self.draw_offset[0]+2,((2+y)*32)*self.multiplier+self.draw_offset[1]-12))
            elif self.inventory_state == "machine":
                text_recepie= self.font.render(self.descriptions["machine_names"][machinery_list[self.inventory_tile].type], False, (0, 0, 0))
                font_width, font_height = self.font.size("0")
                self.surface.blit(text_recepie, (10*32*self.multiplier+self.draw_offset[0]-(font_width*len(self.descriptions["machine_names"][machinery_list[self.inventory_tile].type])/2),1.5*32*self.multiplier+self.draw_offset[1]))
                for x in range(2,18,2):
                    for y in range(10,16,2):
                        cell = self.inv[int((x/2-1)+((y-8)/2-1)*8)]
                        self.surface.blit(
                                pg.transform.scale(
                                        self.sprites["ui_inv_tile"],(int(32*self.multiplier),int(32*self.multiplier))
                                ),((x*32)*self.multiplier+self.draw_offset[0],(y*32)*self.multiplier+self.draw_offset[1])
                            )
                        self.surface.blit(
                                pg.transform.scale(pg.transform.rotate(
                                        self.sprites["ui_inv_tile"],270),(int(32*self.multiplier),int(32*self.multiplier))
                                ),(((x+1)*32)*self.multiplier+self.draw_offset[0],(y*32)*self.multiplier+self.draw_offset[1])
                            )
                        self.surface.blit(
                                pg.transform.scale(pg.transform.rotate(
                                        self.sprites["ui_inv_tile"],180),(int(32*self.multiplier),int(32*self.multiplier))
                                ),(((x+1)*32)*self.multiplier+self.draw_offset[0],((y+1)*32)*self.multiplier+self.draw_offset[1])
                            )
                        self.surface.blit(
                                pg.transform.scale(pg.transform.rotate(
                                        self.sprites["ui_inv_tile"],90),(int(32*self.multiplier),int(32*self.multiplier))
                                ),((x*32)*self.multiplier+self.draw_offset[0],((y+1)*32)*self.multiplier+self.draw_offset[1])
                            )
                        if cell != {} and cell["item"] != "":
                            self.surface.blit(
                                    pg.transform.scale(
                                            self.sprites[f"item_{cell['item']}"],(int(64*self.multiplier),int(64*self.multiplier))
                                    ),((x*32)*self.multiplier+self.draw_offset[0],(y*32)*self.multiplier+self.draw_offset[1])
                                )
                            if cell['amount'] > 1:
                                item_amonut = self.font.render(str(cell['amount']), False, (255, 255, 255))
                                self.surface.blit(item_amonut, ((x*32)*self.multiplier+self.draw_offset[0]+2,((2+y)*32)*self.multiplier+self.draw_offset[1]-12))
                
                for c_id, cell in enumerate(machinery_list[self.inventory_tile].inv["in"]):
                    cell_id = c_id*2
                    self.surface.blit(
                            pg.transform.scale(
                                    self.sprites["ui_inv_tile"],(int(32*self.multiplier),int(32*self.multiplier))
                            ),((((cell_id%16)+2)*32)*self.multiplier+self.draw_offset[0],(int(cell_id/16)+2*32)*self.multiplier+self.draw_offset[1])
                        )
                    self.surface.blit(
                            pg.transform.scale(pg.transform.rotate(
                                    self.sprites["ui_inv_tile"],90),(int(32*self.multiplier),int(32*self.multiplier))
                            ),((((cell_id%16)+2)*32)*self.multiplier+self.draw_offset[0],((int(cell_id/16)+2+1)*32)*self.multiplier+self.draw_offset[1])
                        )
                    self.surface.blit(
                            pg.transform.scale(pg.transform.rotate(
                                    self.sprites["ui_inv_tile"],180),(int(32*self.multiplier),int(32*self.multiplier))
                            ),((((cell_id%16)+2+1)*32)*self.multiplier+self.draw_offset[0],((int(cell_id/16)+2+1)*32)*self.multiplier+self.draw_offset[1])
                        )
                    self.surface.blit(
                                pg.transform.scale(pg.transform.rotate(
                                        self.sprites["ui_inv_tile"],270),(int(32*self.multiplier),int(32*self.multiplier))
                                ),((((cell_id%16)+2+1)*32)*self.multiplier+self.draw_offset[0],((int(cell_id/16)+2)*32)*self.multiplier+self.draw_offset[1])
                            )
                    if cell != {} and cell["item"] != "":
                        self.surface.blit(
                                pg.transform.scale(
                                        self.sprites[f"item_{cell['item']}"],(int(64*self.multiplier),int(64*self.multiplier))
                                ),((((cell_id%16)+2)*32)*self.multiplier+self.draw_offset[0],((int(cell_id/16)+2)*32)*self.multiplier+self.draw_offset[1])
                            )
                        if cell['amount'] > 1:
                            item_amonut = self.font.render(str(cell['amount']), False, (255, 255, 255))
                            self.surface.blit(item_amonut, (((cell_id%16)+2)*32*self.multiplier+self.draw_offset[0]+2,(int(cell_id/16+4)*32)*self.multiplier+self.draw_offset[1]-12))
                                
                if "out" in machinery_list[self.inventory_tile].inv:
                    for c_id, cell in enumerate(machinery_list[self.inventory_tile].inv["out"]):
                        cell_id = (c_id + len(machinery_list[self.inventory_tile].inv["in"])+1)*2
                        self.surface.blit(
                                pg.transform.scale(
                                        self.sprites["ui_inv_tile"],(int(32*self.multiplier),int(32*self.multiplier))
                                ),((((cell_id%16)+2)*32)*self.multiplier+self.draw_offset[0],(int(cell_id/16)+2*32)*self.multiplier+self.draw_offset[1])
                            )
                        self.surface.blit(
                                pg.transform.scale(pg.transform.rotate(
                                        self.sprites["ui_inv_tile"],90),(int(32*self.multiplier),int(32*self.multiplier))
                                ),((((cell_id%16)+2)*32)*self.multiplier+self.draw_offset[0],((int(cell_id/16)+2+1)*32)*self.multiplier+self.draw_offset[1])
                            )
                        self.surface.blit(
                                pg.transform.scale(pg.transform.rotate(
                                        self.sprites["ui_inv_tile"],180),(int(32*self.multiplier),int(32*self.multiplier))
                                ),((((cell_id%16)+2+1)*32)*self.multiplier+self.draw_offset[0],((int(cell_id/16)+2+1)*32)*self.multiplier+self.draw_offset[1])
                            )
                        self.surface.blit(
                                    pg.transform.scale(pg.transform.rotate(
                                            self.sprites["ui_inv_tile"],270),(int(32*self.multiplier),int(32*self.multiplier))
                                    ),((((cell_id%16)+2+1)*32)*self.multiplier+self.draw_offset[0],((int(cell_id/16)+2)*32)*self.multiplier+self.draw_offset[1])
                                )
                        if cell != {} and cell["item"] != "":
                            self.surface.blit(
                                    pg.transform.scale(
                                            self.sprites[f"item_{cell['item']}"],(int(64*self.multiplier),int(64*self.multiplier))
                                    ),((((cell_id%16)+2)*32)*self.multiplier+self.draw_offset[0],((int(cell_id/16)+2)*32)*self.multiplier+self.draw_offset[1])
                                )
                            if cell['amount'] > 1:
                                item_amonut = self.font.render(str(cell['amount']), False, (255, 255, 255))
                                self.surface.blit(item_amonut, (((cell_id%16)+2)*32*self.multiplier+self.draw_offset[0]+2,(int(cell_id/16+4)*32)*self.multiplier+self.draw_offset[1]-12))
                if machinery_list[self.inventory_tile].recepie != None:
                    cell_id = len(machinery_list[self.inventory_tile].inv["in"])*2
                    if machinery_list[self.inventory_tile].timer != -1:
                        self.surface.blit(pg.transform.scale(self.sprites["processing_base"],(int(64*self.multiplier),int(64*self.multiplier))), (((cell_id%16)+2)*32*self.multiplier+self.draw_offset[0],(int(cell_id/16+2)*32)*self.multiplier+self.draw_offset[1]))
                        pg.draw.rect(self.surface,(131,131,131),(
                            ((cell_id%16)+4)*32*self.multiplier+self.draw_offset[0]-4-int(machinery_list[self.inventory_tile].timer/(machinery_list[self.inventory_tile].recepies[machinery_list[self.inventory_tile].recepie]["time"]*60)*56),
                            (int(cell_id/16+2)*32)*self.multiplier+self.draw_offset[1],
                            int(machinery_list[self.inventory_tile].timer/(machinery_list[self.inventory_tile].recepies[machinery_list[self.inventory_tile].recepie]["time"]*60)*56),
                            64))
                    self.surface.blit(pg.transform.scale(self.sprites["processing_overlay"],(int(64*self.multiplier),int(64*self.multiplier))), (((cell_id%16)+2)*32*self.multiplier+self.draw_offset[0],(int(cell_id/16+2)*32)*self.multiplier+self.draw_offset[1]))
                    cell_id = (len(machinery_list[self.inventory_tile].inv["in"])+(len(machinery_list[self.inventory_tile].inv["out"]) if "out" in machinery_list[self.inventory_tile].inv else 0)+1)*2
                    self.surface.blit(pg.transform.scale(self.sprites["configure"],(int(64*self.multiplier),int(64*self.multiplier))), (((cell_id%16)+2)*32*self.multiplier+self.draw_offset[0],((int(cell_id/16)+2)*32)*self.multiplier+self.draw_offset[1]))
                    recepie_name = self.descriptions[self.recepies[machinery_list[self.inventory_tile].type][machinery_list[self.inventory_tile].recepie]['display_out']][0] if machinery_list[self.inventory_tile].recepie != -1 else "None" 
                    text_recepie= self.font.render(f"Selected Recepie: {recepie_name}", False, (0, 0, 0))
                    self.surface.blit(text_recepie, (2*32*self.multiplier+self.draw_offset[0]-16,8*32*self.multiplier+self.draw_offset[1]))

                if hasattr(machinery_list[self.inventory_tile],"power_net"):
                    self.surface.blit(pg.transform.scale(self.sprites["power_ui_counter_edge"],(32,32)), (12*32*self.multiplier+self.draw_offset[0],6*32*self.multiplier+self.draw_offset[1]))
                    self.surface.blit(pg.transform.scale(self.sprites["power_ui_counter"],(32,32)), (13*32*self.multiplier+self.draw_offset[0],6*32*self.multiplier+self.draw_offset[1]))
                    self.surface.blit(pg.transform.rotate(pg.transform.scale(self.sprites["power_ui_counter_edge"],(32,32)),180), (14*32*self.multiplier+self.draw_offset[0],6*32*self.multiplier+self.draw_offset[1]))
                    self.surface.blit(pg.transform.scale(self.sprites["power_ui_arrow"],(32,32)), (12*32*self.multiplier+self.draw_offset[0],5*32*self.multiplier+self.draw_offset[1]))
                    self.surface.blit(pg.transform.scale(self.sprites["power_ui_arrow"],(32,32)), (13*32*self.multiplier+self.draw_offset[0],5*32*self.multiplier+self.draw_offset[1]))
                    self.surface.blit(pg.transform.scale(self.sprites["power_ui_arrow"],(32,32)), (14*32*self.multiplier+self.draw_offset[0],5*32*self.multiplier+self.draw_offset[1]))
                    self.surface.blit(pg.transform.rotate(pg.transform.scale(self.sprites["power_ui_arrow"],(32,32)),180), (12*32*self.multiplier+self.draw_offset[0],7*32*self.multiplier+self.draw_offset[1]))
                    self.surface.blit(pg.transform.rotate(pg.transform.scale(self.sprites["power_ui_arrow"],(32,32)),180), (13*32*self.multiplier+self.draw_offset[0],7*32*self.multiplier+self.draw_offset[1]))
                    self.surface.blit(pg.transform.rotate(pg.transform.scale(self.sprites["power_ui_arrow"],(32,32)),180), (14*32*self.multiplier+self.draw_offset[0],7*32*self.multiplier+self.draw_offset[1]))
                    net = str(machinery_list[self.inventory_tile].power_net)
                    while len(net) < 3:
                        net = "0"+net
                    self.surface.blit(pg.transform.scale(self.sprites[f"power_ui_counter_{net[2]}"],(32,32)), (12*32*self.multiplier+self.draw_offset[0],6*32*self.multiplier+self.draw_offset[1]))
                    self.surface.blit(pg.transform.scale(self.sprites[f"power_ui_counter_{net[1]}"],(32,32)), (13*32*self.multiplier+self.draw_offset[0],6*32*self.multiplier+self.draw_offset[1]))
                    self.surface.blit(pg.transform.scale(self.sprites[f"power_ui_counter_{net[0]}"],(32,32)), (14*32*self.multiplier+self.draw_offset[0],6*32*self.multiplier+self.draw_offset[1]))

                    
            elif self.inventory_state == "machine_recepie":
                text = self.font.render("Recepie selection:", False, (0, 0, 0))
                self.surface.blit(text, (7*32*self.multiplier+self.draw_offset[0]-16,2*32*self.multiplier+self.draw_offset[1]))
                display_recepies = machinery_list[self.inventory_tile].recepies
                for i, recepie in enumerate(display_recepies):
                    cell_id = i * 2
                    self.surface.blit(pg.transform.scale(self.sprites["recepie_tile"],(int(64*self.multiplier),int(64*self.multiplier))), (((cell_id%8)+2)*32*self.multiplier+self.draw_offset[0],((int(cell_id/8)+3)*32)*self.multiplier+self.draw_offset[1]))
                    self.surface.blit(pg.transform.scale(self.sprites[f"item_{recepie['display_out']}"],(int(64*self.multiplier),int(64*self.multiplier))), (((cell_id%8)+2)*32*self.multiplier+self.draw_offset[0],((int(cell_id/8)+3)*32)*self.multiplier+self.draw_offset[1]))


                                
        if self.inventory_state != "none":
            draw_pos = m_pos[0] if m_pos[0] <= self.draw_offset[0]+20*32-(128+64) else m_pos[0]-(128+64)
            self.surface.blit(
                pg.transform.scale(
                        self.sprites["ui_cursor"],(int(32*self.multiplier),int(32*self.multiplier))
                ),(m_pos[0],m_pos[1])
            )
            if self.inventory_cell != {}:
                    draw_pos = m_pos[0] if m_pos[0] <= self.draw_offset[0]+20*32-64 else m_pos[0]-64
                    self.surface.blit(
                        pg.transform.scale(
                                self.sprites[f"item_{self.inventory_cell['item']}"],(int(64*self.multiplier),int(64*self.multiplier))
                        ),(draw_pos+4,m_pos[1]+4)
                    )
            if self.inventory_state == "player":
                for x in range(2,18,2):
                    for y in range(2,8,2):
                        if m_pos[0] >(x*32)*self.multiplier+self.draw_offset[0] and m_pos[0] <((x+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[1]>(y*32)*self.multiplier+self.draw_offset[1] and m_pos[1]<((2+y)*32)*self.multiplier+self.draw_offset[1]:
                            item = self.inv[int((x/2-1)+(y/2-1)*8)]
                            draw_pos = m_pos[0] if m_pos[0] <= self.draw_offset[0]+20*32-(128+64) else m_pos[0]-(128+64)
                            if self.inventory_cell == {} and item != {} and item["item"] != "":
                                self.surface.blit(
                                    pg.transform.scale(
                                            self.sprites["inv_description"],(int(128+64*self.multiplier),int(64+32*self.multiplier))
                                    ),(draw_pos+16,m_pos[1]+16)
                                )
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][0], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16))
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][1], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*2))
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][2], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*3))
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][3], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*4))
            elif self.inventory_state == "machine":
                for x in range(2,18,2):
                    for y in range(10,16,2):
                        if m_pos[0] >(x*32)*self.multiplier+self.draw_offset[0] and m_pos[0] <((x+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[1]>(y*32)*self.multiplier+self.draw_offset[1] and m_pos[1]<((2+y)*32)*self.multiplier+self.draw_offset[1]:
                            item = self.inv[int((x/2-1)+((y-8)/2-1)*8)]
                            if item != {} and item["item"] != "" and self.inventory_cell == {}:
                                self.surface.blit(
                                    pg.transform.scale(
                                            self.sprites["inv_description"],(int(128+64*self.multiplier),int(64+32*self.multiplier))
                                    ),(draw_pos+16,m_pos[1]+16)
                                )
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][0], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16))
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][1], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*2))
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][2], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*3))
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][3], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*4))
                for c_id, item in enumerate(machinery_list[self.inventory_tile].inv["in"]):
                    cell_id = c_id*2
                    if m_pos[0] >(((cell_id%16)+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[0] <((((cell_id%16)+2)+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[1]>((int(cell_id/16)+2)*32)*self.multiplier+self.draw_offset[1] and m_pos[1]<((2+(int(cell_id/16)+2))*32)*self.multiplier+self.draw_offset[1]:
                        draw_pos = m_pos[0] if m_pos[0] <= self.draw_offset[0]+20*32-(128+64) else m_pos[0]-(128+64)
                        if "item" in item and item != {} and item["item"] != "" and self.inventory_cell == []:
                            self.surface.blit(
                                pg.transform.scale(
                                        self.sprites["inv_description"],(int(128+64*self.multiplier),int(64+32*self.multiplier))
                                ),(draw_pos+16,m_pos[1]+16)
                            )
                            text_rotation = self.small_font.render(self.descriptions[item["item"]][0], False, (0, 255, 0))
                            self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16))
                            text_rotation = self.small_font.render(self.descriptions[item["item"]][1], False, (0, 255, 0))
                            self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*2))
                            text_rotation = self.small_font.render(self.descriptions[item["item"]][2], False, (0, 255, 0))
                            self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*3))
                            text_rotation = self.small_font.render(self.descriptions[item["item"]][3], False, (0, 255, 0))
                            self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*4))
                
                if "out" in machinery_list[self.inventory_tile].inv:
                    for c_id, item in enumerate(machinery_list[self.inventory_tile].inv["out"]):
                        cell_id = (c_id + len(machinery_list[self.inventory_tile].inv["in"])+1)*2
                        if m_pos[0] >(((cell_id%16)+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[0] <((((cell_id%16)+2)+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[1]>((int(cell_id/16)+2)*32)*self.multiplier+self.draw_offset[1] and m_pos[1]<((2+(int(cell_id/16)+2))*32)*self.multiplier+self.draw_offset[1]:
                            draw_pos = m_pos[0] if m_pos[0] <= self.draw_offset[0]+20*32-(128+64) else m_pos[0]-(128+64)
                            if item != {} and item["item"] != "" and self.inventory_cell == {}:
                                self.surface.blit(
                                    pg.transform.scale(
                                            self.sprites["inv_description"],(int(128+64*self.multiplier),int(64+32*self.multiplier))
                                    ),(draw_pos+16,m_pos[1]+16)
                                )
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][0], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16))
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][1], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*2))
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][2], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*3))
                                text_rotation = self.small_font.render(self.descriptions[item["item"]][3], False, (0, 255, 0))
                                self.surface.blit(text_rotation, (draw_pos+16+12,m_pos[1]+16+16*4))
            elif self.inventory_state == "machine_recepie":
                display_recepies = machinery_list[self.inventory_tile].recepies
                for i, recepie in enumerate(display_recepies):
                    cell_id = i * 2
                    if m_pos[0] > ((cell_id%8)+2)*32*self.multiplier+self.draw_offset[0] and m_pos[1] > ((int(cell_id/8)+3)*32)*self.multiplier+self.draw_offset[1] and m_pos[0] < ((cell_id%8)+4)*32*self.multiplier+self.draw_offset[0] and m_pos[1] < ((int(cell_id/8)+5)*32)*self.multiplier+self.draw_offset[1]:
                        length = 2 + len(recepie["requires"]) + len(recepie["outputs"])
                        texts = ["Requires:"]+recepie["requires"]+["Output(s):"]+recepie["outputs"]
                        self.surface.blit(
                                pg.transform.scale(
                                        self.sprites["recepie_description_top"],(int(128+64*self.multiplier),int(32*self.multiplier))
                                ),(draw_pos+16,m_pos[1]+16)
                            )
                        for i, t in enumerate(texts):
                            if i+1 == len(texts):
                                self.surface.blit(
                                    pg.transform.scale(
                                        pg.transform.flip(
                                            self.sprites["recepie_description_top"],False,True
                                        ),(int(128+64*self.multiplier),int(32*self.multiplier))
                                    ),(draw_pos+16,m_pos[1]+16+32*(1+(i/2)))
                                )
                            elif i % 2 == 0:
                                self.surface.blit(
                                pg.transform.scale(
                                        self.sprites["recepie_description_middle"],(int(128+64*self.multiplier),int(32*self.multiplier))
                                    ),(draw_pos+16,m_pos[1]+16+32*(1+(i/2)))
                                )
                            text = t if type(t) == str else self.descriptions[t[0]][0]
                            text_recepie = self.small_font.render(text, False, (0, 255, 0))
                            self.surface.blit(text_recepie, (draw_pos+16+12,m_pos[1]+32+16*i))
        elif self.cursor_state != "none" and self.cursor_state[0] == "build":
            click_tile_pos = [int((m_pos[0]+self.offset[0]-self.draw_offset[0])/(32*self.multiplier)),int((m_pos[1]+self.offset[1]-self.draw_offset[1 ])/(32*self.multiplier))]
            if self.cursor_state[1] == "conveyor_belt":
                if self.cursor_state[2] == 0:
                    self.surface.blit(
                        pg.transform.scale(
                                pg.transform.flip(self.sprites["ui_conv0"],True,False),(int(32*self.multiplier),int(32*self.multiplier))
                        ),(click_tile_pos[0]*32*self.multiplier+self.draw_offset[0],click_tile_pos[1]*32*self.multiplier+self.draw_offset[1])
                    )
                elif self.cursor_state[2] == 90:
                    self.surface.blit(
                        pg.transform.scale(
                                self.sprites["ui_conv90"],(int(32*self.multiplier),int(42*self.multiplier))
                        ),(click_tile_pos[0]*32*self.multiplier+self.draw_offset[0],(click_tile_pos[1]*32-10)*self.multiplier+self.draw_offset[1])
                    )
                elif self.cursor_state[2] == 180:
                    self.surface.blit(
                        pg.transform.scale(
                                self.sprites["ui_conv0"],(int(32*self.multiplier),int(32*self.multiplier))
                        ),(click_tile_pos[0]*32*self.multiplier+self.draw_offset[0],click_tile_pos[1]*32*self.multiplier+self.draw_offset[1])
                    )
                elif self.cursor_state[2] == 270:
                    self.surface.blit(
                        pg.transform.scale(
                                self.sprites["ui_conv270"],(int(32*self.multiplier),int(42*self.multiplier))
                        ),(click_tile_pos[0]*32*self.multiplier+self.draw_offset[0],(click_tile_pos[1]*32-10)*self.multiplier+self.draw_offset[1])
                    )
            elif self.cursor_state[1] == "furnace":
                    self.surface.blit(
                        pg.transform.scale(
                                self.sprites["furnace_wireframe"],(int(64*self.multiplier),int(64*self.multiplier))
                        ),(click_tile_pos[0]*32*self.multiplier+self.draw_offset[0],(click_tile_pos[1]*32)*self.multiplier+self.draw_offset[1])
                    )
            else:
                self.surface.blit(
                        pg.transform.scale(
                                self.sprites[f"{self.cursor_state[1]}_wireframe"],(int(32*self.multiplier),int(32*self.multiplier))
                        ),(click_tile_pos[0]*32*self.multiplier+self.draw_offset[0],(click_tile_pos[1]*32)*self.multiplier+self.draw_offset[1])
                    )
            pg.draw.rect(self.surface, (75, 75, 75), ((1.5*32)*self.multiplier+self.draw_offset[0], (17*32)*self.multiplier+self.draw_offset[1], 32*self.multiplier*17, 32*2*self.multiplier))
            pg.draw.rect(self.surface, (0, 0, 0), ((1.5*32+6)*self.multiplier+self.draw_offset[0], (17*32+6)*self.multiplier+self.draw_offset[1], 32*self.multiplier*17-12, 32*2*self.multiplier-12))
            text_rotation = self.font.render(f"rot: {self.cursor_state[2]}", False, (0, 255, 0))
            self.surface.blit(text_rotation, ((1.5*32+8)*self.multiplier+self.draw_offset[0], (17*32+12)*self.multiplier+self.draw_offset[1]))
        elif self.cursor_state != "none" and self.cursor_state == "buldoze":
            
            pg.draw.rect(self.surface, (75, 75, 75), ((1.5*32)*self.multiplier+self.draw_offset[0], (17*32)*self.multiplier+self.draw_offset[0], 32*self.multiplier*17, 32*2*self.multiplier))
            pg.draw.rect(self.surface, (0, 0, 0), ((1.5*32+6)*self.multiplier+self.draw_offset[0], (17*32+6)*self.multiplier+self.draw_offset[0], 32*self.multiplier*17-12, 32*2*self.multiplier-12))
            text_rotation = self.font.render("Buldozing mode", False, (0, 255, 0))
            self.surface.blit(text_rotation, ((1.5*32+8)*self.multiplier+self.draw_offset[0], (17*32+12)*self.multiplier+self.draw_offset[0]))
            self.surface.blit(
                pg.transform.scale(
                        self.sprites["ui_cursor_delete"],(int(32*self.multiplier),int(32*self.multiplier))
                ),(m_pos[0],m_pos[1])
            )
        elif self.cursor_state != "none" and self.cursor_state[0] == "link":
            
            pg.draw.rect(self.surface, (75, 75, 75), ((1.5*32)*self.multiplier+self.draw_offset[0], (17*32)*self.multiplier+self.draw_offset[0], 32*self.multiplier*17, 32*2*self.multiplier))
            pg.draw.rect(self.surface, (0, 0, 0), ((1.5*32+6)*self.multiplier+self.draw_offset[0], (17*32+6)*self.multiplier+self.draw_offset[0], 32*self.multiplier*17-12, 32*2*self.multiplier-12))
            text_rotation = self.font.render("Power cable linking", False, (0, 255, 0))
            self.surface.blit(text_rotation, ((1.5*32+8)*self.multiplier+self.draw_offset[0], (17*32+12)*self.multiplier+self.draw_offset[0]))
            self.surface.blit(
                pg.transform.scale(
                        self.sprites["ui_cursor_cable"],(int(32*self.multiplier),int(32*self.multiplier))
                ),(m_pos[0],m_pos[1])
            )
        else:
            self.surface.blit(
                pg.transform.scale(
                        self.sprites["ui_cursor"],(int(32*self.multiplier),int(32*self.multiplier))
                ),(m_pos[0],m_pos[1])
            )


        
    def click(self,pos,m_evt, world, machinery_list,wiring_nets):
        changes = []
        machinery_append=[]
        machinery_delete=[]
        machinery_changes=[]
        m_pos = pos
        if self.mode == "game":
            click_tile_pos = [int((pos[0]+self.offset[0]-self.draw_offset[0])/(32*self.multiplier)),int((pos[1]+self.offset[1]-self.draw_offset[1 ])/(32*self.multiplier))]
            if self.inventory_state != "none" and m_evt:
                if self.inventory_state == "player":
                    for x in range(2,18,2):
                        for y in range(2,8,2):
                            if m_pos[0] >(x*32)*self.multiplier+self.draw_offset[0] and m_pos[0] <((x+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[1]>(y*32)*self.multiplier+self.draw_offset[1] and m_pos[1]<((2+y)*32)*self.multiplier+self.draw_offset[1]:
                                item = self.inv[int((x/2-1)+(y/2-1)*8)]
                                if self.inventory_cell == {} and item != {} and item["item"] != "":
                                    self.inventory_cell = item.copy()
                                    self.inv[int((x/2-1)+(y/2-1)*8)] = {}
                                elif self.inventory_cell != {} and (item == {} or item["item"] == ""):
                                    self.inv[int((x/2-1)+(y/2-1)*8)] = self.inventory_cell.copy()
                                    self.inventory_cell = {}
                                elif self.inventory_cell != {} and "item" in item and self.inventory_cell["item"] == item["item"] and item["amount"] < 100:
                                    if item["amount"] + self.inventory_cell["amount"] <= 100:
                                        self.inv[int((x/2-1)+(y/2-1)*8)]["amount"] += self.inventory_cell["amount"]
                                        self.inventory_cell = {}
                                    else:
                                        self.inventory_cell["amount"] -= (100-item["amount"])
                                        self.inv[int((x/2-1)+(y/2-1)*8)]["amount"] = 100

                elif self.inventory_state == "machine":
                    for x in range(2,18,2):
                        for y in range(10,16,2):
                            if m_pos[0] >(x*32)*self.multiplier+self.draw_offset[0] and m_pos[0] <((x+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[1]>(y*32)*self.multiplier+self.draw_offset[1] and m_pos[1]<((2+y)*32)*self.multiplier+self.draw_offset[1]:
                                item = self.inv[int((x/2-1)+((y-8)/2-1)*8)]
                                if self.inventory_cell == {} and item != {} and item["item"] != "":
                                    self.inventory_cell = item.copy()
                                    self.inv[int((x/2-1)+((y-8)/2-1)*8)] = {"item":"","amount":0}
                                elif self.inventory_cell != {} and (item == {} or item["item"]== ""):
                                    self.inv[int((x/2-1)+((y-8)/2-1)*8)] = self.inventory_cell.copy()
                                    self.inventory_cell = {}
                                elif self.inventory_cell != {} and "item" in item and self.inventory_cell["item"] == item["item"] and item["amount"] < 100:
                                    if item["amount"] + self.inventory_cell["amount"] <= 100:
                                        self.inv[int((x/2-1)+(y/2-1)*8)]["amount"] += self.inventory_cell["amount"]
                                        self.inventory_cell = {}
                                    else:
                                        self.inventory_cell["amount"] -= (100-item["amount"])
                                        self.inv[int((x/2-1)+(y/2-1)*8)]["amount"] = 100
                    for c_id, item in enumerate(machinery_list[self.inventory_tile].inv["in"]):
                        cell_id = c_id*2
                        if m_pos[0] >(((cell_id%16)+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[0] <((((cell_id%16)+2)+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[1]>((int(cell_id/16)+2)*32)*self.multiplier+self.draw_offset[1] and m_pos[1]<((2+(int(cell_id/16)+2))*32)*self.multiplier+self.draw_offset[1]:
                            draw_pos = m_pos[0] if m_pos[0] <= self.draw_offset[0]+20*32-(128+64) else m_pos[0]-(128+64)
                            if "item" in item and item["item"] != "" and self.inventory_cell == {}:
                                self.inventory_cell = item.copy()
                                machinery_list[self.inventory_tile].inv["in"][c_id] ={"item":"","amount":0}
                                machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])
                            elif self.inventory_cell != {} and (item == {} or item["item"] == ""):
                                machinery_list[self.inventory_tile].inv["in"][c_id] =self.inventory_cell.copy()
                                self.inventory_cell = {}
                                machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])
                            elif self.inventory_cell != {} and item != {} and item["item"] == self.inventory_cell["item"] and item["amount"] < 100:
                                if item["amount"] + self.inventory_cell["amount"] <= 100:
                                    item["amount"] += self.inventory_cell["amount"]
                                    self.inventory_cell = {}
                                    machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])
                                else:
                                    self.inventory_cell["amount"] -= (100-item["amount"])
                                    item["amount"] = 100
                                    machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])


                    if "out" in machinery_list[self.inventory_tile].inv:
                        for c_id, item in enumerate(machinery_list[self.inventory_tile].inv["out"]):
                            cell_id = (c_id + len(machinery_list[self.inventory_tile].inv["in"])+1)*2
                            if m_pos[0] >(((cell_id%16)+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[0] <((((cell_id%16)+2)+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[1]>((int(cell_id/16)+2)*32)*self.multiplier+self.draw_offset[1] and m_pos[1]<((2+(int(cell_id/16)+2))*32)*self.multiplier+self.draw_offset[1]:
                                draw_pos = m_pos[0] if m_pos[0] <= self.draw_offset[0]+20*32-(128+64) else m_pos[0]-(128+64)
                                if item != {} and item["item"] != "" and self.inventory_cell == {}:
                                    self.inventory_cell = item.copy()
                                    machinery_list[self.inventory_tile].inv["out"][c_id] ={}
                                    machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])
                    cell_id = ((len(machinery_list[self.inventory_tile].inv["out"]) if "out" in machinery_list[self.inventory_tile].inv else 0) + len(machinery_list[self.inventory_tile].inv["in"])+1)*2
                    if m_pos[0] >(((cell_id%16)+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[0] <((((cell_id%16)+2)+2)*32)*self.multiplier+self.draw_offset[0] and m_pos[1]>((int(cell_id/16)+2)*32)*self.multiplier+self.draw_offset[1] and m_pos[1]<((2+(int(cell_id/16)+2))*32)*self.multiplier+self.draw_offset[1]:
                        self.inventory_state = "machine_recepie"
                    if hasattr(machinery_list[self.inventory_tile], "power_net"):
                        net = str(machinery_list[self.inventory_tile].power_net)
                        while len(net) < 3:
                            net = "0"+net
                        if m_pos[0] >= 12*32*self.multiplier+self.draw_offset[0] and m_pos[0] < 13*32*self.multiplier+self.draw_offset[0] and m_pos[1] >= 5*32*self.multiplier+self.draw_offset[1] and m_pos[1] < 6*32*self.multiplier+self.draw_offset[1]:
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.remove(self.inventory_tile)
                            net = net[:2]+(str(int(net[2])+1) if net[2] != "9" else "0")
                            machinery_list[self.inventory_tile].power_net = int(net)
                            machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.append(self.inventory_tile)
                        elif m_pos[0] >= 13*32*self.multiplier+self.draw_offset[0] and m_pos[0] < 14*32*self.multiplier+self.draw_offset[0] and m_pos[1] >= 5*32*self.multiplier+self.draw_offset[1] and m_pos[1] < 6*32*self.multiplier+self.draw_offset[1]:
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.remove(self.inventory_tile)
                            net = net[0]+(str(int(net[1])+1) if net[1] != "9" else "0")+net[2]
                            machinery_list[self.inventory_tile].power_net = int(net)
                            machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.append(self.inventory_tile)
                        elif m_pos[0] >= 14*32*self.multiplier+self.draw_offset[0] and m_pos[0] < 15*32*self.multiplier+self.draw_offset[0] and m_pos[1] >= 5*32*self.multiplier+self.draw_offset[1] and m_pos[1] < 6*32*self.multiplier+self.draw_offset[1]:
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.remove(self.inventory_tile)
                            net = (str(int(net[0])+1) if net[0] != "9" else "0") + net[1:]
                            machinery_list[self.inventory_tile].power_net = int(net)
                            machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.append(self.inventory_tile)
                        elif m_pos[0] >= 12*32*self.multiplier+self.draw_offset[0] and m_pos[0] < 13*32*self.multiplier+self.draw_offset[0] and m_pos[1] >= 7*32*self.multiplier+self.draw_offset[1] and m_pos[1] < 8*32*self.multiplier+self.draw_offset[1]:
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.remove(self.inventory_tile)
                            net = net[:2]+(str(int(net[2])-1) if net[2] != "0" else "9")
                            machinery_list[self.inventory_tile].power_net = int(net)
                            machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.append(self.inventory_tile)
                        elif m_pos[0] >= 13*32*self.multiplier+self.draw_offset[0] and m_pos[0] < 14*32*self.multiplier+self.draw_offset[0] and m_pos[1] >= 7*32*self.multiplier+self.draw_offset[1] and m_pos[1] < 8*32*self.multiplier+self.draw_offset[1]:
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.remove(self.inventory_tile)
                            net = net[0]+(str(int(net[1])-1) if net[1] != "0" else "9")+net[2]
                            machinery_list[self.inventory_tile].power_net = int(net)
                            machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.append(self.inventory_tile)
                        elif m_pos[0] >= 14*32*self.multiplier+self.draw_offset[0] and m_pos[0] < 15*32*self.multiplier+self.draw_offset[0] and m_pos[1] >= 7*32*self.multiplier+self.draw_offset[1] and m_pos[1] < 8*32*self.multiplier+self.draw_offset[1]:
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.remove(self.inventory_tile)
                            net = (str(int(net[0])-1) if net[0] != "0" else "9") + net[1:]
                            machinery_list[self.inventory_tile].power_net = int(net)
                            machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])
                            wiring_nets[machinery_list[self.inventory_tile].power_net].points.append(self.inventory_tile)
                        
                elif self.inventory_state == "machine_recepie":
                    display_recepies = machinery_list[self.inventory_tile].recepies
                    for i, recepie in enumerate(display_recepies):
                        cell_id = i * 2
                        if m_pos[0] > ((cell_id%8)+2)*32*self.multiplier+self.draw_offset[0] and m_pos[1] > ((int(cell_id/8)+3)*32)*self.multiplier+self.draw_offset[1] and m_pos[0] < ((cell_id%8)+4)*32*self.multiplier+self.draw_offset[0] and m_pos[1] < ((int(cell_id/8)+5)*32)*self.multiplier+self.draw_offset[1]:
                            self.inventory_state = "machine"
                            machinery_list[self.inventory_tile].recepie = i
                            machinery_changes.append([self.inventory_tile,machinery_list[self.inventory_tile]])
            elif self.cursor_state == "none":
                if world[click_tile_pos[0]+self.pos[0]+((self.pos[1]+click_tile_pos[1])*self.world_dimensions[0])]["block"] in self.openable_machines:
                    if str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]) in machinery_list:
                        self.inventory_tile = str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1])
                        self.inventory_state = "machine"
                elif "link_obj_" in world[click_tile_pos[0]+self.pos[0]+((self.pos[1]+click_tile_pos[1])*self.world_dimensions[0])]["block"]:
                    self.inventory_state = "machine"
                    if str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]) in machinery_list and machinery_list[str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1])].links in machinery_list:
                        self.inventory_tile = machinery_list[str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1])].links
                        self.inventory_state = "machine"
            elif self.cursor_state[0] == "build" and world[click_tile_pos[0]+self.pos[0]+((self.pos[1]+click_tile_pos[1])*self.world_dimensions[0])]["block"] in self.build_blocks:
                if self.cursor_state[1] in self.buildings:
                    building = copy.deepcopy(self.buildings[self.cursor_state[1]])
                    can_build = True
                    to_clear = []
                    to_substract = []
                    for position in [[0,0]]+building["requires_space"]:
                        if world[click_tile_pos[0]+self.pos[0]+position[0]+((self.pos[1]+click_tile_pos[1]+position[1])*self.world_dimensions[0])]["block"] in self.build_blocks:
                            pass
                        else:
                            can_build = False
                    for item in building["requires_materials"]:
                        amount = item["amount"]
                        for cell_id, inv_item in enumerate(self.inv):
                            if inv_item != {} and inv_item["item"] == item["item"]:
                                amount -= inv_item["amount"]
                                if amount >=0:
                                    to_clear.append(cell_id)
                                else:
                                    to_substract.append([cell_id,inv_item["amount"]+amount])
                        if amount > 0:
                            can_build = False

                    if can_build:
                        for cell_id in to_clear:
                            self.inv[cell_id] = {}
                        for cell_info in to_substract:
                            self.inv[cell_info[0]]["amount"] -= cell_info[1]
                        changes.append([(click_tile_pos[0]+self.pos[0]+((self.pos[1]+click_tile_pos[1])*self.world_dimensions[0])),{"block":self.cursor_state[1]}])
                        if building["rotatable"]:changes[-1][1]["rotation"]=self.cursor_state[2]
                        if building["requires_space"] != []:
                            i = 2
                            for position in building["requires_space"]:
                                changes.append([(click_tile_pos[0]+self.pos[0]+position[0]+((self.pos[1]+click_tile_pos[1]+position[1])*self.world_dimensions[0])),{"block":f"link_obj_{self.cursor_state[1]}_part{i}"}])
                                i+=1
                        inv = building["machine_args"]["inv"].copy()
                        if building["machine_args"]["recepies"] == None:
                            machinery_append.append([str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]),Machine([click_tile_pos[0]+self.pos[0],click_tile_pos[1]+self.pos[1]],self.cursor_state[1],inv,rotation=self.cursor_state[2])])
                        else:
                            machinery_append.append([str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]),Machine([click_tile_pos[0]+self.pos[0],click_tile_pos[1]+self.pos[1]],self.cursor_state[1],inv,recepies=self.recepies[building["machine_args"]["recepies"]],rotation=self.cursor_state[2])])
                            machinery_append[-1][1].recepie = -1
                        if "power_net" in building:
                            machinery_append[-1][1].power_net = 0
                            if building["power"] < 0:
                                machinery_append[-1][1].power = building["power"]
                                machinery_append[-1][1].working = False
                                wiring_nets[0].points["consumers"].append(str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]))
                            else:
                                machinery_append[-1][1].power = building["power"]
                                wiring_nets[0].points["generators"].append(str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]))

                        if "timer" in building["machine_args"]: machinery_append[-1][1].timer = building["machine_args"]["timer"]
                        if building["requires_space"] != []:
                            tiles = []
                            for position in building["requires_space"]:
                                tiles.append([click_tile_pos[0]+self.pos[0]+position[0],self.pos[1]+click_tile_pos[1]+position[1]])
                            machinery_append[-1][1].links = tiles.copy()
                            for position in building["requires_space"]:
                                machinery_append.append([str(click_tile_pos[0]+self.pos[0]+position[0])+"_"+str(click_tile_pos[1]+self.pos[1]+position[1]),Machine([click_tile_pos[0]+self.pos[0]+position[0],click_tile_pos[1]+self.pos[1]+position[1]],"link_mach",[],0,[],str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]))])
            elif self.cursor_state == "buldoze":
                machine_position = []
                click_tile_pos = [int((pos[0]+self.offset[0]-self.draw_offset[0])/(32*self.multiplier)),int((pos[1]+self.offset[1]-self.draw_offset[1 ])/(32*self.multiplier))]
                if world[click_tile_pos[0]+self.pos[0]+((self.pos[1]+click_tile_pos[1])*self.world_dimensions[0])]["block"] in self.buildings or "link_obj_" in world[click_tile_pos[0]+self.pos[0]+((self.pos[1]+click_tile_pos[1])*self.world_dimensions[0])]["block"]:
                    if world[click_tile_pos[0]+self.pos[0]+((self.pos[1]+click_tile_pos[1])*self.world_dimensions[0])]["block"] in self.buildings:
                        machine_position = str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1])
                        building = self.buildings[world[click_tile_pos[0]+self.pos[0]+((self.pos[1]+click_tile_pos[1])*self.world_dimensions[0])]["block"]].copy()
                    elif "link_obj_" in world[click_tile_pos[0]+self.pos[0]+((self.pos[1]+click_tile_pos[1])*self.world_dimensions[0])]["block"]:
                        link_pos = []
                        if str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]) in machinery_list:
                            link_pos = machinery_list[str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1])].links
                        if link_pos in machinery_list:
                            building = self.buildings[world[machinery_list[link_pos].pos[0]+((machinery_list[link_pos].pos[1])*self.world_dimensions[0])]["block"]].copy()
                        machine_position = link_pos
                    if machine_position in machinery_list:
                        machine_id = machine_position
                    can_remove = True
                    machine = machinery_list[machine_id]
                    player_inv = self.inv.copy()
                    items_return = machine.inv["in"].copy()
                    items_return += machine.inv["out"].copy() if "out" in machine.inv else []
                    items_return += building["requires_materials"]
                    for item in items_return:
                        if item != {} and item != "":
                            amount = item["amount"] if type(item) != str else 1
                            item_item = item["item"] if type(item) != str else item
                            for item_id, inv_item in enumerate(player_inv):
                                if inv_item != {} and amount > 0 and inv_item["amount"] + amount <= 100 and inv_item["item"] == item_item:
                                    inv_item["amount"] += amount
                                    amount = 0
                                elif inv_item != {} and amount > 0  and inv_item["item"] == item_item:
                                    amount -= (100-inv_item["amount"])
                                    inv_item["amount"] = 100
                                elif inv_item == {} and amount > 0 or inv_item != {} and inv_item["item"] == "" and amount > 0:
                                    if amount <= 100:
                                        inv_item = {"item":item_item,"amount":amount}
                                        amount = 0
                                    else:
                                        inv_item = {"item":item_item,"amount":100}
                                        amount -= 100
                                player_inv[item_id] = inv_item
                            if amount > 0:
                                can_remove = False
                    if can_remove:
                        self.inv = player_inv.copy()
                        self.explosions = [[machine.pos[0],machine.pos[1],0]]
                        if hasattr(machine,"power_net"):
                            if machine.power < 0:
                                wiring_nets[machine.power_net].points["consumers"].remove(machine_id)
                            else:
                                wiring_nets[machine.power_net].points["generators"].remove(machine_id)
                        for i in building["requires_space"]:
                            self.explosions.append([machine.pos[0]+i[0],machine.pos[1]+i[1],0])
                        for position in [[0,0]]+building["requires_space"]:
                            changes.append([(int(machine_position.split("_")[0])+position[0]+((int(machine_position.split("_")[1])+position[1])*self.world_dimensions[0])),{"block":"stone","rotation":0}])
                        for position in [[0,0]]+building["requires_space"]:
                            if str(int(machine_position.split("_")[0])+position[0])+"_"+str(int(machine_position.split("_")[1])+position[1]) in machinery_list:
                                machinery_delete.append(str(int(machine_position.split("_")[0])+position[0])+"_"+str(int(machine_position.split("_")[1])+position[1]))
            elif self.cursor_state[0] == "link":
                if str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]) in machinery_list:
                    machine = machinery_list[str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1])]
                    if self.cursor_state[1] == None:
                        print("a",hasattr(machine, "wire_limit"), hasattr(machine,"wire_connections"))
                        if hasattr(machine, "wire_limit") and hasattr(machine,"wire_connections"):
                            self.cursor_state[1] = str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1])
                            print("b")
                    else:
                        if hasattr(machine, "wire_limit") and hasattr(machine,"wire_connections"):
                            if self.cursor_state[1] in machine.wire_connections:
                                machine.wire_connections.remove(self.cursor_state[1])
                                machinery_changes.append([str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]), machinery_list[str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1])]])
                                machinery_list[self.cursor_state[1]].wire_connections.remove(str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]))
                                machinery_changes.append([self.cursor_state[1], machinery_list[self.cursor_state[1]]])
                            elif len(machine.wire_connections) < machine.wire_limit and self.cursor_state[1] != machine.pos:
                                machine.wire_connections.append(self.cursor_state[1])
                                machinery_changes.append([str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]), machinery_list[str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1])]])
                                machinery_list[self.cursor_state[1]].wire_connections.append(str(click_tile_pos[0]+self.pos[0])+"_"+str(click_tile_pos[1]+self.pos[1]))
                                machinery_changes.append([self.cursor_state[1], machinery_list[self.cursor_state[1]]])
                                        

        return changes, machinery_append, machinery_delete, machinery_changes, wiring_nets


    def pos_sync(self):
        x = self.player_pos[0]-10 if self.player_pos[0] > 9 and self.player_pos[0] <245 else 0
        x = x if self.player_pos[0] <245 else 235
        y = self.player_pos[1]-10 if self.player_pos[1] > 9 and self.player_pos[1] <245 else 0
        y = y if self.player_pos[1] <245 else 235
        self.pos = [x,y]
        self.offset=[self.player_offset[0]%32 if self.player_pos[0] > 9 and self.player_pos[0] <245 else 0 ,self.player_offset[1]%32 if self.player_pos[1] > 9 and self.player_pos[1] <245 else 0]

    def gamecycle(self,working,display, fullscreen,clock,tick,evt_k,machinery_list, world,screen_size,m_evt,wire_nets):
        k = {}
        changes, machinery_append, machinery_delete, machinery_changes = [],[],[],[]
        
        if working:
            rm = []
            for l,i in enumerate(self.explosions):
                i[2] += 120/clock.get_fps() if clock.get_fps() != 0 else 1
                if i[2] >= 120:
                    rm.append(l)
            for l in reversed(sorted(rm)):
                self.explosions.pop(l)
            w, h = pg.display.get_surface().get_size()
            frac, nat = math.modf((h/20)/32)
            frac*=100
            frac = 0 if frac < 25 else 25 if frac <50 else 50 if frac<75 else 75
            self.multiplier = float(str(int(nat))+"."+str(frac))
            self.draw_offset = ((w-(32*20*self.multiplier))/2,(h-(32*20*self.multiplier))/2)
            self.draw(pg.mouse.get_pos(),tick,machinery_list,world)
            fps_counter = self.font.render(str(int(clock.get_fps())), False, (255, 255, 255))
            self.surface.blit(fps_counter, (0, 0))
            pg.display.update()
            k = pg.key.get_pressed()
            arrow_keys = [k[pg.K_LEFT],k[pg.K_RIGHT],k[pg.K_UP],k[pg.K_DOWN]]
            movement_speed = 120/clock.get_fps() if clock.get_fps() != 0 else 1
            if self.inventory_state=="none": #self.tick%32==0 and 
                if arrow_keys[0]:
                    if self.player_offset[0] > 0:
                        self.player_offset[0]-=movement_speed
                        if self.player_offset[0] < 0: self.player_offset[0] = 0
                    self.player_rotation =90 
                elif arrow_keys[1]:
                    if self.player_offset[0] < 32*256:
                        self.player_offset[0]+=movement_speed
                        if self.player_offset[0] > 32*256: self.player_offset[0] = 32*256
                    self.player_rotation =270 
                if arrow_keys[2]:
                    if self.player_offset[1] > 0:
                        self.player_offset[1]-=movement_speed
                        if self.player_offset[1] < 0: self.player_offset[1] = 0
                    self.player_rotation =0 
                elif arrow_keys[3]:
                    if self.player_offset[1] < 32*256:
                        self.player_offset[1]+=movement_speed
                        if self.player_offset[1] > 32*256: self.player_offset[1] = 32*256
                    self.player_rotation =180 
                self.player_pos = [int(self.player_offset[0]/32),int(self.player_offset[1]/32)]
            if evt_k != {} and (evt_k[pg.K_LCTRL] or evt_k[pg.K_RCTRL]):
                if k[pg.K_q]:
                    working=False
                elif k[pg.K_f]:
                    if fullscreen:
                        display = pg.display.set_mode(screen_size,pg.RESIZABLE, pg.SRCALPHA)#|pg.SCALED)
                        fullscreen = False
                        self.multiplier = 1
                        self.draw_offset=(0,0)
                    else:
                        display = pg.display.set_mode(screen_size,pg.FULLSCREEN, pg.SRCALPHA)#|pg.SCALED)
                        fullscreen = True
            elif evt_k != {} and evt_k[pg.K_v]:
                if self.cursor_state != "none" and self.cursor_state[0] == "link":
                    self.cursor_state = "none"
                else:
                    self.cursor_state = ["link",None]
            elif evt_k != {} and evt_k[pg.K_b]:
                if self.cursor_state != "none" and self.cursor_state[0] == "build":
                    self.cursor_state = "none"
                else:
                    self.build_id = 0
                    for i,l in enumerate(self.buildings):
                        if i == self.build_id:
                            self.cursor_state =["build",l,0]
                            break
            elif evt_k != {} and evt_k[pg.K_n]:
                if self.cursor_state != "none" and self.cursor_state == "buldoze":
                    self.cursor_state = "none"
                else:
                    self.cursor_state ="buldoze"
            elif evt_k != {} and evt_k[pg.K_TAB]:
                if self.cursor_state[0] == "build":
                    self.build_id +=1
                    if self.build_id == len(self.buildings):
                        self.build_id =0
                    for i,l in enumerate(self.buildings):
                        if i == self.build_id:
                            self.cursor_state =["build",l,0]
                            break
            elif evt_k != {} and evt_k[pg.K_r] and not (evt_k[pg.K_LSHIFT] or evt_k[pg.K_RSHIFT]):
                if self.cursor_state != "none" and len(self.cursor_state) == 3:
                    self.cursor_state[2] += 90
                    if self.cursor_state[2] ==360: self.cursor_state[2]=0
            elif evt_k != {} and evt_k[pg.K_r] and (evt_k[pg.K_LSHIFT] or evt_k[pg.K_RSHIFT]):
                if self.cursor_state != "none" and len(self.cursor_state) == 3:
                    self.cursor_state[2] -= 90
                    if self.cursor_state[2] ==-90: self.cursor_state[2]=270
            elif evt_k != {} and evt_k[pg.K_e]:
                if self.inventory_state != "none":
                    self.inventory_state = "none"
                else:
                    self.inventory_state = "player"

            if pg.mouse.get_pressed()[0]:
                changes, machinery_append, machinery_delete, machinery_changes,wire_nets= self.click(pg.mouse.get_pos(),m_evt, world, machinery_list,wire_nets)
            old_k = k
            self.pos_sync()
            return (changes,machinery_append, machinery_delete, machinery_changes,wire_nets)