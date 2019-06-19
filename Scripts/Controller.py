class Controller:#key input manager, it can allow for object control assignement, easier multiplayer, ect.
    def __init__(self, id):#initialization, id is mostly for recognizing different key maps
        self.id = id#identifiers
        self.controls = {"up":[273, -1], "down":[274, -1], "left":[276, -1], "right":[275, -1], "return":[13, -1], "escape":[27, -1]}
        #controlled keys, in the format : [key, timestamp] where the timestamp records how long a key has been pressed,
        #if it is just pressed, it was just released or simply not pressed at the time.
        self.controltags = ["up", "down", "left", "right", "return", "escape"]
        #this keeps track of all the keys in self.controls, so that humans can put actual name on it
        #and increase code readability

    def bind(self, name, key):#this can bind a new key into the controller, that way you can add keys
        self.controls[name] = [key, -1]#add a new key in the self.control, by default being unheld
        self.controltags.append(name)#add the given key name in the self.controltags, allowing it to be
        #updated each self.update() call, more on that later

    def unbind(self, name):#unbind the given key name (or index)
        if name.__class__.__name__ == "str":#if the key is given by name
            self.controls.pop(name)
            self.controltags.remove(name)
        if name.__class__.__name__ == "int":#if the key is given by index
            self.controls.pop(self.controltags[name])
            self.controltags.pop(name)

    def update(self, events):#update the keys' states with a given "pygame.EventList" object

        for event in events:#for each event in the given list
            #event types are checked in int so that we don't have to import the pygame library for this class

            if event.type == 2:#if the event's type corresponds to a button press
                for key in self.controltags:#checks each key in self.control if it is the pressed key
                    if event.key == self.controls[key][0]:#if it is:
                        self.controls[key][1] = 0#then we set it in the "just pressed" state

            if event.type == 3:#if the event's type corresponds to a button release
                for key in self.controltags:#checks each key in self.control if it is the released key
                    if event.key == self.controls[key][0]:#if it is:
                        self.controls[key][1] = -3#then we set it in the "just released" state

        for key in self.controltags:#then the function updates each key's hold time
            if self.controls[key][1] < -1:#if the key is in "just released" state:
                self.controls[key][1] += 1#then we set the key in the "released" state

            if self.controls[key][1] >= 0:#if the key is in "just pressed" state:
                self.controls[key][1] += 1#then we set the key in the "pressed" state

    def get_press(self, name):#we get if a key is in the "just pressed" state, by name or index
        if name.__class__.__name__ == 'str':#if the key is given by name
            if self.controls[name][1] == 1:#return True if it is just pressed
                return True
        elif name.__class__.__name__ == 'int':#if the key is given by index
            if self.controls[self.controltags[name]][1] == 1:#return True is it is just pressed
                return True
        return False#or if it isn't, then we return False

    def get_hold(self, name):#we get if a key is in the "pressed" state, by name or index
        if name.__class__.__name__ == 'str':#if the key is given by name
            if self.controls[name][1] > 1:#return True is it is pressed
                return True
        elif name.__class__.__name__ == 'int':#if the key is given by index
            if self.controls[self.controltags[name]][1] > 1:#return True is it is pressed
                return True
        return False#or if it isn't, then we return False

    def get_unpress(self, name):#we get if a key is in the "just released" state, by name or index
        if name.__class__.__name__ == 'str':#if the key is given by name
            if self.controls[name][1] == -2:#return True is it is just released
                return True
        elif name.__class__.__name__ == 'int':#if the key is given by index
            if self.controls[self.controltags[name]][1] == -2:#return True is it is just released
                return True
        return False#or if it isn't, then we return False

    def get_unhold(self, name):#we get if a key is in the "released" state, by name or index
        if name.__class__.__name__ == 'str':
            if self.controls[name][1] == -1:
                return True
        elif name.__class__.__name__ == 'int':
            if self.controls[self.controltags[name]][1] == -1:
                return True
        return False#or if it isn't, then we return False

    def get_time_hold(self, name):#we get the number of frames a key has been held
        if name.__class__.__name__ == 'str':#if the key is given by name
            if self.controls[name][1] > -1:#if the value isn't a "key" value
                return self.controls[name][1]#we return the hold time
        elif name.__class__.__name__ == 'int':#if the key is given by index
            if self.controls[self.controltags[name]][1] > -1:#if the value isn't a "key" value
                return self.controls[self.controltags[name]][1]#we return the hold time
        return 0#or the hold value isn't a "key" value, then we return 0

    def get_bind_name(self, id):#return a name by index
        return self.controltags[id]

    def get_bind_id(self, name):#return an index by name
        try:
            return self.controltags.index(name)
        except:
            return -1

if __name__ == "__main__":#demonstration code, not commented
    import pygame
    pygame.init()
    scr = pygame.display.set_mode((20, 20))
    control = Controller(0)
    control.unbind("up")
    control.bind("0", pygame.K_0)
    run = True
    clk = pygame.time.Clock()
    frames = 0
    while run:
        frames += 1
        control.update(pygame.event.get())
        print("FRAME " + str(frames) + ":")
        for i in range(len(control.controltags)):
            if control.get_press(i):
                print(" "+control.get_bind_name(i)+" was just pressed")
            elif control.get_hold(i):
                print(" " + control.get_bind_name(i) + " has been held for "+str(control.get_time_hold(i))+" frames")
            elif control.get_unpress(i):
                print(" "+control.get_bind_name(i)+" was just released")
            elif control.get_unhold(i):
                print(" "+control.get_bind_name(i)+" is currently released")
            if control.get_bind_name(i) == "escape":
                if control.get_press(i):
                    run = False
        clk.tick(10)