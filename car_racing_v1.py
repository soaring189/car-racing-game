# This version implements a scrolling background for the 2D racing game using Pygame, with adjustable speed and seamless looping.
import pygame as p
import sys

p.init()
screen_size = (600, 800)
game_screen = p.display.set_mode(screen_size)
p.display.set_caption("car game")
icon = p.image.load("./Assets/game_icon.png").convert_alpha()
p.display.set_icon(icon)
bg_images = [
    p.transform.scale(p.image.load("./Assets/bg-0.png").convert_alpha(), (600, 800)),
    p.transform.scale(p.image.load("./Assets/bg-1.png").convert_alpha(), (600, 800))
]
scroll_speed = 1
fps_clock = p.time.Clock()
FPS = 200


class Background:
    def __init__(self, images, speed):
        self.images = images
        self.speed = speed
        self.y0 = 0
        self.y1 = -800
        self.bg_num = 0

    def update(self, speed):
        self.speed = speed
        self.y0 += self.speed
        self.y1 += self.speed
        if self.y0 >= 800:
            self.bg_num = (self.bg_num + 1) % 4
            self.y0 = -800

        if self.y1 >= 800:
            self.y1 = -800

    def draw(self, screen):
        if self.bg_num < 3:
            screen.blit(self.images[0], (0, self.y0))
        else:
            screen.blit(self.images[1], (0, self.y0))
        screen.blit(self.images[0], (0, self.y1))


bg = Background(bg_images, scroll_speed)
running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
    bg.update(scroll_speed)
    bg.draw(game_screen)
    p.display.update()
    fps_clock.tick(FPS)
p.quit()
sys.exit()
