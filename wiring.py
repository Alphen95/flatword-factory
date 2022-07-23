#провода существуют, но в абстракции. зато на один анальный зонд меньше.

class WiringNet():
    def __init__(self):
        self.points = {"generators":[],"consumers":[]}
        self.capacity = 0
        self.capacity_left = 0

    def update(self,machine_list):
        for point in self.points["generators"]:
            if machine_list[point].timer > 0:
                self.capacity += machine_list[point].power
        self.capacity_left = self.capacity
        for point in self.points["consumers"]:
            self.capacity_left += machine_list[point].power
            if self.capacity_left <= 0:machine_list[point].working = False
            else: machine_list[point].working = True

        return machine_list