import pygame


class fpsClass():
    def __init__(self, fpss):
        self.fpss = fpss

    def get_fps(self):
        return self.fpss

    def slow_fps(self):
        self.fpss = 4

    def normal_fps(self):
        self.fpss = 30

    def isNormal(self):
        if self.fpss == 4:
            return False
        else:
            return True
