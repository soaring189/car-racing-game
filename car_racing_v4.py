# This version of the game implements  dynamic obstacle cars that spawn in random lanes and random speed.
import random
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
car_images = [
    p.transform.scale(p.image.load("./Assets/car_1.png").convert_alpha(), (80, 160)),
    p.transform.scale(p.image.load("./Assets/car_2.png").convert_alpha(), (80, 160)),
    p.transform.scale(p.image.load("./Assets/car_3.png").convert_alpha(), (80, 160)),
    p.transform.scale(p.image.load("./Assets/car_4.png").convert_alpha(), (80, 160)),
    p.transform.scale(p.image.load("./Assets/car_5.png").convert_alpha(), (80, 160)),
    p.transform.scale(p.image.load("./Assets/car_6.png").convert_alpha(), (80, 160))
]
scroll_speed = 0
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
        self.y0 += speed
        self.y1 += speed
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


class Car:
    def __init__(self, x, y, car_num, car_x_speed, car_y_speed, max_speed, images):
        self.x = x
        self.y = y
        self.car_num = car_num
        self.car_x_speed = car_x_speed
        self.car_y_speed = car_y_speed
        self.max_speed = max_speed
        self.images = images
        self.angle = 0

    def update(self, speed):
        keys = p.key.get_pressed()
        if keys[p.K_LEFT] or keys[p.K_a]:
            if self.x > 45:
                self.x -= self.car_x_speed * (speed / self.max_speed)
                self.angle = min(15.0, self.angle + 0.6 * (speed / self.max_speed))
            if self.angle < 0:
                self.angle += speed / self.max_speed
        if keys[p.K_RIGHT] or keys[p.K_d]:
            if (self.x + 45) < (screen_size[0] - car_images[self.car_num].get_width()):
                self.x += self.car_x_speed * (speed / self.max_speed)
                self.angle = max(-15.0, self.angle - 0.6 * (speed / self.max_speed))
            if self.angle > 0:
                self.angle -= speed / self.max_speed
        if not (keys[p.K_LEFT] or keys[p.K_a] or keys[p.K_RIGHT] or keys[p.K_d]):
            if self.angle > 0:
                self.angle -= 0.6 * (speed / self.max_speed)
            elif self.angle < 0:
                self.angle += 0.6 * (speed / self.max_speed)
        if keys[p.K_UP] or keys[p.K_w]:
            if speed < self.max_speed:
                speed += self.car_y_speed
        else:
            speed = max(0, speed - self.car_y_speed / 2)
        if keys[p.K_DOWN] or keys[p.K_s]:
            speed = max(0, speed - self.car_y_speed)
        return speed

    def draw(self, screen):
        rotated_image = p.transform.rotate(self.images[self.car_num],
                                           self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x + car_images[self.car_num].get_width() // 2, self.y + car_images[self.car_num].get_height() // 2))
        screen.blit(rotated_image, rotated_rect.topleft)


class ObstacleCar:
    def __init__(self, images):
        self.x_pos_list = [68, 195, 321, 448]
        self.x_pos_num = random.randint(0, len(self.x_pos_list) - 1)
        self.y = random.randint(-2500, -1200)
        self.car_num = random.randint(0, 5)
        self.speed = random.uniform(0.8, 2)
        self.images = images
        self.reset_position()

    def reset_position(self):
        self.x_pos_num = random.randint(0, len(self.x_pos_list)-1)
        self.y = random.randint(-2500, -1200)
        self.car_num = random.randint(0, len(self.images) - 1)
        self.speed = random.uniform(0.8, 2)

    def update(self, bg_speed):
        self.y += (bg_speed + self.speed)
        if self.y > screen_size[1] + self.images[self.car_num].get_height():
            self.reset_position()

    def draw(self, screen):
        rotated_image = p.transform.rotate(self.images[self.car_num], 180)
        screen.blit(rotated_image, (self.x_pos_list[self.x_pos_num], self.y))


bg = Background(bg_images, scroll_speed)
car = Car(260, 600, 0, 3, 0.01, 5, car_images)
obstacle_cars = []
for i in range(3):
    obstacle_cars.append(ObstacleCar(car_images))
running = True
while running:
    events = p.event.get()
    for event in events:
        if event.type == p.QUIT:
            running = False
    scroll_speed = car.update(scroll_speed)
    bg.update(scroll_speed)
    bg.draw(game_screen)
    for obstacle_car in obstacle_cars:
        obstacle_car.update(scroll_speed)
        obstacle_car.draw(game_screen)
    car.draw(game_screen)
    p.display.update()
    fps_clock.tick(FPS)
p.quit()
sys.exit()
