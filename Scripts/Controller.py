class Controller:
    def __init__(self, id):
        self.id = id
        self.controls = {"up":[273, 0], "down":[274, 0], "left":[276, 0], "right":[275, 0], "return":[13, 0], "escape":[27, 0]}
        self.controltags = ["up", "down", "left", "right", "return"]

    def bind(self, name, key):
        self.controls[name] = key
        self.controltags.append(name)

    def unbind(self, name):
        self.controls.pop(name)
        self.controltags.remove(name)

    def update(self, events):
        for event in events:
            if event.type == 2:
                for key in self.controltags:
                    if event.key == self.controls[key][0]:
                        self.controls[key][1] = 0
            if event.type == 3:
                for key in self.controltags:
                    if event.key == self.controls[key][0]:
                        self.controls[key][1] = -3

        for key in self.controltags:
            if self.controls[key][1] < -1:
                self.controls[key][1] += 1
            if self.controls[key][1] >= 0:
                self.controls[key][1] += 1

    def get_press(self, name):
        if self.controls[name][1] == 1:
            return True
        return False

    def get_hold(self, name):
        if self.controls[name][1] > 1:
            return True
        return False

    def get_unpress(self, name):
        if self.controls[name][1] == -2:
            return True
        return False

    def get_unhold(self, name):
        if self.controls[name][1] == -1:
            return True
        return False