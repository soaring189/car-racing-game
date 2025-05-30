# This version of the game allows players to choose to restart or quit after game over.
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
    p.transform.smoothscale(p.image.load("./Assets/bg-0.png").convert_alpha(), (600, 800)),
    p.transform.smoothscale(p.image.load("./Assets/bg-1.png").convert_alpha(), (600, 800))
]
car_images = [
    p.transform.smoothscale(p.image.load("./Assets/car_1.png").convert_alpha(), (80, 160)),
    p.transform.smoothscale(p.image.load("./Assets/car_2.png").convert_alpha(), (80, 160)),
    p.transform.smoothscale(p.image.load("./Assets/car_3.png").convert_alpha(), (80, 160)),
    p.transform.smoothscale(p.image.load("./Assets/car_4.png").convert_alpha(), (80, 160)),
    p.transform.smoothscale(p.image.load("./Assets/car_5.png").convert_alpha(), (80, 160)),
    p.transform.smoothscale(p.image.load("./Assets/car_6.png").convert_alpha(), (80, 160))
]
game_over_image = p.transform.smoothscale(p.image.load("./Assets/game_over.png").convert_alpha(), (530.5, 74))
restart_image = p.transform.smoothscale(p.image.load("./Assets/restart_or_quit.png").convert_alpha(), (377.5, 80.83))
scroll_speed = 0
collide_car_speed = 0
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
            self.y0 = self.y1 - 800
            self.bg_num = (self.bg_num + 1) % len(self.images)

        if self.y1 >= 800:
            self.y1 = self.y0 - 800

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
        self.image = self.images[self.car_num]
        self.mask = p.mask.from_surface(self.image)

    def check_collision(self, other_car):
        other_image = other_car.images[other_car.car_num]
        other_mask = p.mask.from_surface(other_image)
        offset_x = other_car.x_pos_list[other_car.x_pos_num] - self.x
        offset_y = other_car.y - self.y
        return self.mask.overlap(other_mask, (offset_x, offset_y))

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
    def __init__(self, images, existing_cars):
        self.x_pos_list = [68, 195, 321, 448]
        self.images = images
        self.x_pos_num = None
        self.y = None
        self.car_num = None
        self.speed = None
        self.reset_position(existing_cars)

    def reset_position(self, existing_cars):
        occupied_lanes = [vehicle.x_pos_num for vehicle in existing_cars]
        free_lanes = []
        for lane in range(4):
            if lane not in occupied_lanes:
                free_lanes.append(lane)
        self.x_pos_num = random.choice(free_lanes)
        self.y = random.randint(-2500, -1200)
        self.car_num = random.randint(0, len(self.images) - 1)
        self.speed = random.uniform(0.8, 2)

    def update(self, bg_speed, existing_cars):
        self.y += (bg_speed + self.speed)
        if self.y > screen_size[1] + self.images[self.car_num].get_height():
            self.reset_position(existing_cars)

    def draw(self, screen):
        rotated_image = p.transform.rotate(self.images[self.car_num], 180)
        screen.blit(rotated_image, (self.x_pos_list[self.x_pos_num], self.y))


def game_state(bg_speed, obstacle_car_speed):
    global running, car
    if game_over:
        game_screen.blit(game_over_image, (34.75, 363))
        if car.y < 800:
            car.y += bg_speed + obstacle_car_speed
        bg_speed = max(0, bg_speed - 0.02)
        if bg_speed == 0:
            game_screen.blit(restart_image, (111.25, 500))
            keys = p.key.get_pressed()
            if keys[p.K_r]:
                reset_game()
            if keys[p.K_q]:
                running = False
    return bg_speed


def reset_game():
    global game_over, car, obstacle_cars, bg
    game_over = False
    car = Car(260, 600, 0, 3, 0.01, 5, car_images)
    obstacle_cars = []
    for j in range(3):
        if j == 0:
            obstacle_cars.append(ObstacleCar(car_images, []))
        else:
            obstacle_cars.append(ObstacleCar(car_images, obstacle_cars))
    bg = Background(bg_images, scroll_speed)


game_over = False
car = Car(260, 600, 0, 3, 0.01, 5, car_images)
obstacle_cars = []
for i in range(3):
    if i == 0:
        obstacle_cars.append(ObstacleCar(car_images, []))
    else:
        obstacle_cars.append(ObstacleCar(car_images, obstacle_cars))
bg = Background(bg_images, scroll_speed)
running = True
while running:
    events = p.event.get()
    for event in events:
        if event.type == p.QUIT:
            running = False
    if not game_over:
        scroll_speed = car.update(scroll_speed)
    bg.update(scroll_speed)
    bg.draw(game_screen)
    car.draw(game_screen)
    for obstacle_car in obstacle_cars:
        obstacle_car.update(scroll_speed, obstacle_cars)
        obstacle_car.draw(game_screen)
        if car.check_collision(obstacle_car):
            collide_car_speed = obstacle_car.speed
            game_over = True
    scroll_speed = game_state(scroll_speed, collide_car_speed)
    p.display.update()
    p.time.Clock().tick(FPS)
p.quit()
sys.exit()
