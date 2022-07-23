
class Machine():
    def __init__(self,pos=[0,0],mach_type="casing",inv={"in":[],"out":[]},rotation = 0,recepies=[],links=[],machine_list = []):
        self.pos = pos
        self.type = mach_type
        self.inv = inv
        self.recepies = recepies
        self.recepie = None
        self.rotaion =rotation
        self.timer = 0 if mach_type != "conveyor_belt" else [0,0,0,0]
        self.clear = False
        self.links = links
        if self.type == "link_mach":
            for i in machine_list:
                if i.pos == self.links:
                    self.inv = i.inv
                    break

    def update(self,world,world_dimensions,machine_list,decrement,io_blocks):
        side1 = world[self.pos[0]+(self.pos[1]-1)*256] if self.pos[1] > 0 else None
        side2 = world[(self.pos[0]+1)+self.pos[1]*256] if self.pos[0] < 255 else None
        side3 = world[self.pos[0]+(self.pos[1]+1)*256] if self.pos[1] < 255  else None
        side4 = world[(self.pos[0]-1)+self.pos[1]*256] if self.pos[0] > 0 else None
        if self.type == "conveyor_belt":
            inputs = [
                str(self.pos[0])+"_"+str(self.pos[1]-1) if side1 == {"block":"conveyor_belt","rotation":90} or (side1["block"] in io_blocks and self.rotaion == 90) or "link_obj_" in side1["block"] else False,
                str(self.pos[0]+1)+"_"+str(self.pos[1]) if side2 == {"block":"conveyor_belt","rotation":180} or (side2["block"] in io_blocks and self.rotaion == 180) or "link_obj_" in side2["block"] else False,
                str(self.pos[0])+"_"+str(self.pos[1]+1) if side3 == {"block":"conveyor_belt","rotation":270} or (side3["block"] in io_blocks and self.rotaion == 270) or "link_obj_" in side3["block"] else False,
                str(self.pos[0]-1)+"_"+str(self.pos[1]) if side4 == {"block":"conveyor_belt","rotation":0} or (side4["block"] in io_blocks and self.rotaion == 0) or "link_obj_" in side4["block"] else False
            ]
            for i in [0,1,2,3]:
                self.timer[i]-=decrement
                if self.timer[i] < 0:self.timer[i]=0
            if self.clear and self.timer[3] == 0:
                self.clear=False
                self.inv["in"][3]=""
            if self.timer[2] <= 0 and self.inv["in"][3] =="" and self.inv["in"][2] !="":
                self.inv["in"][3] =self.inv["in"][2]
                self.inv["in"][2] = ""
                self.timer[3]=60
            if self.timer[1] <= 0 and self.inv["in"][2] =="" and self.inv["in"][1] !="":
                self.inv["in"][2] =self.inv["in"][1]
                self.inv["in"][1] = ""
                self.timer[2]=60
            if self.timer[0] <= 0 and self.inv["in"][1] =="" and self.inv["in"][0] !="":
                self.inv["in"][1] =self.inv["in"][0]
                self.inv["in"][0] = ""
                self.timer[1]=60
            if self.inv["in"][0] == "":
                for i in inputs:
                    if i!=False:
                        if i in machine_list:
                            i1 = machine_list[i]
                            if not "out" in i1.inv and type(i1.timer) == list and i1.timer[3]<=0 and not i1.clear:
                                self.inv["in"][0] = i1.inv["in"][3]
                                self.timer[0] = 60
                                i1.clear=True
                                break
                            elif "out" in i1.inv:
                                for item_id, item in enumerate(i1.inv["out"]):
                                    if item != {} and item["item"] != "":
                                        if item["amount"] > 1:
                                            self.inv["in"][0] = item["item"]
                                            i1.inv["out"][item_id]["amount"] -= 1
                                            self.timer[0] = 60
                                        elif item["amount"] == 1:
                                            self.inv["in"][0] = item["item"]
                                            i1.inv["out"][item_id] = {}
                                            self.timer[0] = 60
                            elif i1.type != "link_mach" and "in" in i1.inv and i1.type != "conveyor_belt":
                                for item_id, item in enumerate(i1.inv["in"]):
                                    if item != {} and item["item"] != "":
                                        if item["amount"] > 1:
                                            self.inv["in"][0] = item["item"]
                                            i1.inv["in"][item_id]["amount"] -= 1
                                            self.timer[0] = 60
                                        elif item["amount"] == 1:
                                            self.inv["in"][0] = item["item"]
                                            i1.inv["in"][item_id] = {}
                                            self.timer[0] = 60
                            elif i1.type == "link_mach":
                                if i1.links in machine_list:
                                    i2 = machine_list[i1.links]
                                    if "out" in i2.inv:
                                        for item_id, item in enumerate(i2.inv["out"]):
                                            if item != {} and item["item"] != "":
                                                if item["amount"] > 1:
                                                    self.inv["in"][0] = item["item"]
                                                    i2.inv["out"][item_id]["amount"] -= 1
                                                    self.timer[0] = 60
                                                elif item["amount"] == 1:
                                                    self.inv["in"][0] = item["item"]
                                                    i2.inv["out"][item_id] = {}
                                                    self.timer[0] = 60
        else:
            if self.type == "link_mach":
                inputs = [
                    str(self.pos[0])+"_"+str(self.pos[1]-1) if side1 == {"block":"conveyor_belt","rotation":90} else False,
                    str(self.pos[0]+1)+"_"+str(self.pos[1]) if side2 == {"block":"conveyor_belt","rotation":180} else False,
                    str(self.pos[0])+"_"+str(self.pos[1]+1) if side3 == {"block":"conveyor_belt","rotation":270} else False,
                    str(self.pos[0]-1)+"_"+str(self.pos[1]) if side4 == {"block":"conveyor_belt","rotation":0} else False
                ]
                host_mach = None
                if self.links in machine_list:
                    host_mach = machine_list[self.links]
                for i in inputs:
                    if i!=False:
                        if i in machine_list:
                            i1 = machine_list[i]
                            if i1.timer[3]<=0 and not i1.clear:
                                if host_mach.recepie != None and host_mach.recepie > -1:
                                    for cell_id, item in enumerate(host_mach.recepies[host_mach.recepie]["requires"]):
                                        if (host_mach.inv["in"][cell_id] != {} and host_mach.inv["in"][cell_id]["item"] == i1.inv["in"] and i1.inv["in"][3] == item[0] and host_mach.inv["in"][cell_id]["amount"] < 100 or host_mach.inv["in"][cell_id] == {} and i1.inv["in"][3] == item[0]):
                                            if host_mach.inv["in"][cell_id] == {}:
                                                host_mach.inv["in"][cell_id]["item"] = i1.inv["in"][3]
                                                host_mach.inv["in"][cell_id]["amount"] = 1
                                            else:
                                                host_mach.inv["in"][cell_id]["amount"] += 1
                                            i1.clear=True
                                            break
                                elif host_mach.recepie == None:
                                    for cell_id, item in enumerate(host_mach.inv["in"]):
                                        if item["item"] == i1.inv["in"][3] and host_mach.inv["in"][cell_id]["amount"] < 100:
                                            host_mach.inv["in"][cell_id]["amount"] += 1
                                            i1.clear=True
                                            break
                                        elif item == {}:
                                            host_mach.inv["in"][cell_id]["item"] = i1.inv["in"][3]
                                            host_mach.inv["in"][cell_id]["amount"] = 1
                                            i1.clear=True
                                            break

            else:
                inputs = [
                    str(self.pos[0])+"_"+str(self.pos[1]-1) if side1 == {"block":"conveyor_belt","rotation":90} else False,
                    str(self.pos[0]+1)+"_"+str(self.pos[1]) if side2 == {"block":"conveyor_belt","rotation":180} else False,
                    str(self.pos[0])+"_"+str(self.pos[1]+1) if side3 == {"block":"conveyor_belt","rotation":270} else False,
                    str(self.pos[0]-1)+"_"+str(self.pos[1]) if side4 == {"block":"conveyor_belt","rotation":0} else False
                ]
                for i in inputs:
                    if i!=False:
                        if i in machine_list:
                            i1 = machine_list[i]
                            if not "out" in i1.inv and type(i1.timer) == list and i1.timer[3]<=0 and not i1.clear:
                                if self.recepie != None and self.recepie > -1:
                                    for cell_id, item in enumerate(self.recepies[self.recepie]["requires"]):
                                        if item["item"] == i1.inv["in"][3] and (self.inv["in"][cell_id] != {} and self.inv["in"][cell_id]["item"] == i1.inv["in"][3] or self.inv["in"][cell_id] == {}) and self.inv["in"][cell_id]["amount"] < 100:
                                            if self.inv["in"][cell_id] == {}:
                                                self.inv["in"][cell_id]["item"] = i1.inv["in"][3]
                                                self.inv["in"][cell_id]["amount"] = 1
                                            else:
                                                self.inv["in"][cell_id]["amount"] += 1
                                            i1.clear=True
                                            break
                                elif self.recepie == None:
                                    for cell_id, item in enumerate(self.inv["in"]):
                                        if "item" in item and i1.inv["in"][3] != "" and item["item"] == i1.inv["in"][3] and self.inv["in"][cell_id]["amount"] < 100:
                                            self.inv["in"][cell_id]["amount"] += 1
                                            i1.clear=True
                                            break
                                        elif item == {} and i1.inv["in"][3] != "":
                                            self.inv["in"][cell_id]["item"] = str(i1.inv["in"][3])
                                            self.inv["in"][cell_id]["amount"] = 1
                                            i1.clear=True
                                            break


        if "out" in self.inv and self.inv["out"] != []:
            if self.recepie != -1:
                if self.timer == -1:
                    recepie = self.recepies[self.recepie]
                    advance = True
                    for l,i in enumerate(recepie["requires"]):
                        if self.inv["in"][l] != {} and self.inv["in"][l]["item"] == i[0] and self.inv["in"][l]["amount"] >= i[1]:
                            pass
                        else:
                            advance = False
                    for l, i in enumerate(recepie["outputs"]):
                        if self.inv["out"][l] == {} or self.inv["out"][l]["item"] == i[0] and self.inv["out"][l]["amount"] + i[1] <= 100:
                            pass
                        else:
                            advance = False
                    if advance:
                        self.timer = 60*recepie["time"]
                elif self.timer > 0:
                    recepie = self.recepies[self.recepie]
                    advance = True
                    for l,i in enumerate(recepie["requires"]):
                        if self.inv["in"][l] != {} and self.inv["in"][l]["item"] == i[0] and self.inv["in"][l]["amount"] >= i[1]:
                            pass
                        else:
                            advance = False
                    if advance and (hasattr(self,"working") and self.working == True or not hasattr(self,"working")):
                        self.timer -= decrement
                        if self.timer < 0:
                            for l,i in enumerate(recepie["requires"]):
                                if l not in recepie["not_consumable"]:
                                    self.inv["in"][l]["amount"] -= i[1]
                                    if self.inv["in"][l]["amount"] < 1:
                                        self.inv["in"][l] = {}
                            for l,i in enumerate(recepie["outputs"]):
                                if self.inv["out"][l] == {}:
                                    self.inv["out"][l] = {"item":i[0],"amount":i[1]}
                                else:
                                    self.inv["out"][l]["amount"] += i[1]
                            
                    else:
                        self.timer = -1

                elif self.timer <= 0 and self.timer > -1:
                    self.timer = -1
            else:
                self.timer = -1
        elif hasattr(self,"recepie") and self.recepie != None and self.recepie != -1:
            if self.recepie != -1:
                if self.timer == -1:
                    recepie = self.recepies[self.recepie]
                    advance = True
                    for l,i in enumerate(recepie["requires"]):
                        if self.inv["in"][l] != {} and self.inv["in"][l]["item"] == i[0] and self.inv["in"][l]["amount"] >= i[1]:
                            pass
                        else:
                            advance = False
                    if advance:
                        self.timer = 60*recepie["time"]
                        for l,i in enumerate(recepie["requires"]):
                            if l not in recepie["not_consumable"]:
                                self.inv["in"][l]["amount"] -= i[1]
                                if self.inv["in"][l]["amount"] < 1:
                                    self.inv["in"][l] = {}
                elif self.timer > 0:
                    recepie = self.recepies[self.recepie]
                    advance = True
                    if advance and (hasattr(self,"working") and self.working == True or not hasattr(self,"working")):
                        self.timer -= decrement
                            
                    else:
                        self.timer = -1

                elif self.timer <= 0 and self.timer > -1:
                    self.timer = -1
            else:
                self.timer = -1