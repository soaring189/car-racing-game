# This version of the game introduces a start menu, allowing users to freely select vehicles and adjust the difficulty.
import random
import sys
import tkinter as tk
from tkinter import ttk

import pygame as p
from PIL import Image, ImageTk

p.init()
root = tk.Tk()
root.title("Car Game")
root.iconbitmap("./Assets/game_icon.ico")
root.geometry("900x650")
root.resizable(False, False)
car_images_tk = [
    "./Assets/car_1.png", "./Assets/car_2.png", "./Assets/car_3.png",
    "./Assets/car_4.png", "./Assets/car_5.png", "./Assets/car_6.png"
]
car_attributes = [[3, 0.01, 5], [3.2, 0.012, 5.5], [3.8, 0.017, 6.5],
                  [2.5, 0.008, 4.5], [2.8, 0.009, 4.8], [3.5, 0.015, 6]]


def select_car(index):
    car_index.set(index)
    for button in buttons:
        button.config(bg="SystemButtonFace")
    buttons[index].config(bg="blue")


def select_difficulty(level):
    difficulty.set(level)
    easy_btn.config(bg="systemButtonFace")
    normal_btn.config(bg="systemButtonFace")
    hard_btn.config(bg="systemButtonFace")
    if level == "Easy":
        easy_btn.config(bg="green")
    elif level == "Normal":
        normal_btn.config(bg="yellow")
    elif level == "Hard":
        hard_btn.config(bg="red")


def close():
    root.destroy()
    sys.exit()


car_index = tk.IntVar(value=0)
buttons = []
image_refs = []
label_frame = tk.Frame(root, width=150, height=200)
label_frame.place(x=30, y=200)
tk.Label(label_frame, text="Lateral Speed", font=("Arial", 12, "bold")).place(
    x=10, y=70)
tk.Label(label_frame, text="Acceleration", font=("Arial", 12, "bold")).place(
    x=10, y=100)
tk.Label(label_frame, text="Max Speed", font=("Arial", 12, "bold")).place(x=10,
                                                                          y=130)
for image_id, image_path in enumerate(car_images_tk):
    image = Image.open(image_path)
    image = image.resize((80, 160))
    photo = ImageTk.PhotoImage(image)
    image_refs.append(photo)
    img_x = 175 + image_id * 120
    img_y = 100
    tk.Label(root, image=photo).place(x=img_x, y=img_y)
    attr_x = img_x + 15
    tk.Label(root, text=f"{int(car_attributes[image_id][0] * 10)}",
             font=("Arial", 10),
             justify="center", width=6).place(x=attr_x, y=270)
    tk.Label(root, text=f"{car_attributes[image_id][1] * 10}", font=("Arial", 10),
             justify="center", width=6).place(x=attr_x, y=300)
    tk.Label(root, text=f"{int(car_attributes[image_id][2] * 10)}",
             font=("Arial", 10),
             justify="center", width=6).place(x=attr_x, y=330)
    btn = tk.Button(root, text="Choose",
                    command=lambda index=image_id: select_car(index))
    btn.place(x=img_x + 15, y=360)
    buttons.append(btn)
buttons[0].config(bg="blue")
difficulty = tk.StringVar(value="Normal")
difficulty_x = 300
difficulty_y = 430
easy_btn = tk.Button(root, text="Easy", width=10,
                     command=lambda: select_difficulty("Easy"))
easy_btn.place(x=difficulty_x, y=difficulty_y)
normal_btn = tk.Button(root, text="Normal", width=10,
                       command=lambda: select_difficulty("Normal"))
normal_btn.place(x=difficulty_x + 120, y=difficulty_y)
hard_btn = tk.Button(root, text="Hard", width=10,
                     command=lambda: select_difficulty("Hard"))
hard_btn.place(x=difficulty_x + 240, y=difficulty_y)
normal_btn.config(bg="yellow")
start_btn = ttk.Button(root, text="Start Game", command=root.destroy,
                       style="Large.TButton")
start_btn.place(x=450 - 75, y=500)
style = ttk.Style()
style.configure("Large.TButton", font=("Arial", 14, "bold"), padding=15)
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
screen_size = (700, 800)
game_screen = p.display.set_mode(screen_size)
p.display.set_caption("car game")
icon = p.image.load("./Assets/game_icon.png").convert_alpha()
p.display.set_icon(icon)
bg_images = [
    p.transform.smoothscale(p.image.load("./Assets/bg-0.png").convert_alpha(),
                            (600, 800)),
    p.transform.smoothscale(p.image.load("./Assets/bg-1.png").convert_alpha(),
                            (600, 800)),
    p.image.load("./Assets/bg-right.png").convert_alpha()
]
car_images = [
    p.transform.smoothscale(p.image.load("./Assets/car_1.png").convert_alpha(),
                            (80, 160)),
    p.transform.smoothscale(p.image.load("./Assets/car_2.png").convert_alpha(),
                            (80, 160)),
    p.transform.smoothscale(p.image.load("./Assets/car_3.png").convert_alpha(),
                            (80, 160)),
    p.transform.smoothscale(p.image.load("./Assets/car_4.png").convert_alpha(),
                            (80, 160)),
    p.transform.smoothscale(p.image.load("./Assets/car_5.png").convert_alpha(),
                            (80, 160)),
    p.transform.smoothscale(p.image.load("./Assets/car_6.png").convert_alpha(),
                            (80, 160))
]
number_list = []
for i in range(0, 10):
    number = p.image.load(f"./Assets/{i}.png").convert_alpha()
    modified_number = p.transform.smoothscale(
        p.image.load(f"./Assets/{i}.png").convert_alpha(), (48, 72))
    number_list.append(modified_number)
m_image = p.transform.smoothscale(
    p.image.load(f"./Assets/m.png").convert_alpha(), (48, 48))
speedometer_image = p.transform.smoothscale(
    p.image.load("./Assets/speedometer.png").convert_alpha(), (100, 100))
needle_image = p.transform.smoothscale(
    p.image.load("./Assets/needle.png").convert_alpha(), (10, 60))
circle_image = p.transform.smoothscale(
    p.image.load("./Assets/circle.png").convert_alpha(), (10, 10))
game_over_image = p.transform.smoothscale(
    p.image.load("./Assets/game_over.png").convert_alpha(), (530.5, 74))
restart_image = p.transform.smoothscale(
    p.image.load("./Assets/restart_or_quit.png").convert_alpha(),
    (377.5, 80.83))
car_id = car_index.get()
scroll_speed = 0
collide_car_speed = 0
score = 0
needle_angle = 145

if difficulty.get() == "Easy":
    FPS = 150
    difficulty_num = 1
elif difficulty.get() == "Normal":
    FPS = 175
    difficulty_num = 2
else:
    FPS = 200
    difficulty_num = 3
game_over = False
running = True


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
    def __init__(self, x, y, car_num, car_x_speed, car_y_speed, max_speed,
                 images):
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
                self.angle = min(15.0,
                                 self.angle + 0.6 * (speed / self.max_speed))
        if keys[p.K_RIGHT] or keys[p.K_d]:
            if (self.x + 45) < (screen_size[0] -
                                car_images[self.car_num].get_width() - 100):
                self.x += self.car_x_speed * (speed / self.max_speed)
                self.angle = max(-15.0,
                                 self.angle - 0.6 * (speed / self.max_speed))
        if not (keys[p.K_LEFT] or keys[p.K_a] or
                keys[p.K_RIGHT] or keys[p.K_d]):
            if self.angle > 0:
                self.angle = max(0,
                                 self.angle - 0.6 * (speed / self.max_speed))
            elif self.angle < 0:
                self.angle = min(0,
                                 self.angle + 0.6 * (speed / self.max_speed))
        if keys[p.K_UP] or keys[p.K_w]:
            if speed < self.max_speed:
                speed += self.car_y_speed
        else:
            speed = max(0, speed - self.car_y_speed)
        if keys[p.K_DOWN] or keys[p.K_s]:
            speed = max(0, speed - self.car_y_speed * 2)
        return speed

    def draw(self, screen):
        rotated_image = p.transform.rotate(self.images[self.car_num],
                                           self.angle)
        rotated_rect = rotated_image.get_rect(center=(
            self.x + car_images[self.car_num].get_width() // 2,
            self.y + car_images[self.car_num].get_height() // 2))
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
        self.y = random.randint(int(-3000 / difficulty_num),
                                int(-1500 / difficulty_num))
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
    global game_over, score, car, obstacle_cars, bg
    game_over = False
    score = 0
    car = Car(260, 600, car_id, car_attributes[car_id][0],
              car_attributes[car_id][1], car_attributes[car_id][2], car_images)
    obstacle_cars = []
    for j in range(3):
        if j == 0:
            obstacle_cars.append(ObstacleCar(car_images, []))
        else:
            obstacle_cars.append(ObstacleCar(car_images, obstacle_cars))
    bg = Background(bg_images, scroll_speed)


def display_stats(speed, max_speed):
    global needle_angle, score
    game_screen.blit(bg_images[2], (600, 0))
    game_screen.blit(speedometer_image, (600, 700))
    game_screen.blit(circle_image, (645, 745))
    if not game_over:
        needle_angle = 145 - 290 * (speed / max_speed)
    else:
        if needle_angle < 145:
            needle_angle += 5
    rotated_needle = p.transform.rotate(needle_image, needle_angle)
    rotated_rect = rotated_needle.get_rect(center=(650, 750))
    game_screen.blit(rotated_needle, rotated_rect.topleft)
    if not game_over:
        score += 0.033 * scroll_speed * difficulty_num
    for n in range(5):
        game_screen.blit(number_list[(int(score) // (10 ** n)) % 10],
                         (626, 475 - (n * 100)))
    game_screen.blit(m_image, (626, 575))


car = Car(260, 600, car_id, car_attributes[car_id][0],
          car_attributes[car_id][1], car_attributes[car_id][2], car_images)
obstacle_cars = []
for i in range(difficulty_num):
    if i == 0:
        obstacle_cars.append(ObstacleCar(car_images, []))
    else:
        obstacle_cars.append(ObstacleCar(car_images, obstacle_cars))
bg = Background(bg_images, scroll_speed)
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
    display_stats(scroll_speed, car.max_speed)
    p.display.update()
    p.time.Clock().tick(FPS)
p.quit()
sys.exit()
