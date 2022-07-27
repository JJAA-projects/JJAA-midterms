class Ship():

    def __init__(self, x, y, img_path):
        self.x = x
        self.y = y
        self.img_path = img_path

    def fly(self, distance):
        self.x += distance
        self.y += distance


class Asteroid():
