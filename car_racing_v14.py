# This version add comments to the program.

# Import necessary libraries for GUI (Tkinter), game development (Pygame),
# image processing (PIL), and system functions
import random
import sys
import tkinter as tk
from tkinter import ttk

import pygame as p
from PIL import Image, ImageTk

p.init()  # Initialize pygame module

root = tk.Tk()  # Create the main window using tkinter

# List of car attributes: [side speed, acceleration, max speed]
car_attributes = [
    [3, 0.01, 5],  # Car 1
    [3.2, 0.012, 5.5],  # Car 2
    [3.8, 0.017, 6.5],  # Car 3
    [2.5, 0.008, 4.5],  # Car 4
    [2.8, 0.009, 4.8],  # Car 5
    [3.5, 0.015, 6]  # Car 6
]


def select_car(index, car_index, buttons):
    car_index.set(index)  # Save selected car index
    for button in buttons:
        button.config(bg="SystemButtonFace")  # Reset all button colors
    buttons[index].config(bg="blue")  # Highlight selected button


def select_difficulty(level, challenge_level, easy_btn, normal_btn, hard_btn):
    challenge_level.set(
        level)  # Set the chosen difficulty level (Easy, Normal, Hard)

    # Reset all button colors to default
    easy_btn.config(bg="systemButtonFace")
    normal_btn.config(bg="systemButtonFace")
    hard_btn.config(bg="systemButtonFace")

    # Highlight selected difficulty with a different color
    if level == "Easy":
        easy_btn.config(bg="green")
    elif level == "Normal":
        normal_btn.config(bg="yellow")
    elif level == "Hard":
        hard_btn.config(bg="red")


def close_window():
    root.destroy()  # Close the Tkinter window
    sys.exit()  # Exit the program completely


def start_menu():
    root.title("Car Game")  # Set window title
    root.iconbitmap("./Assets/game_icon.ico")  # Set window icon
    root.geometry("900x650")  # Set window size
    root.resizable(False, False)  # Disable window resizing

    # Image paths for the cars
    car_images_tk = [
        "./Assets/car_1.png", "./Assets/car_2.png", "./Assets/car_3.png",
        "./Assets/car_4.png", "./Assets/car_5.png", "./Assets/car_6.png"
    ]

    car_index = tk.IntVar(value=0)  # Store selected car index
    buttons = []  # Store car selection buttons
    image_refs = []  # Keep image references to avoid garbage collection

    # Create a frame for car attributes text
    label_frame = tk.Frame(root, width=150, height=200)
    label_frame.place(x=30, y=200)

    # Attribute labels: speed, acceleration, max speed
    tk.Label(label_frame, text="Lateral Speed",
             font=("Arial", 12, "bold")).place(x=10, y=70)
    tk.Label(label_frame, text="Acceleration",
             font=("Arial", 12, "bold")).place(x=10, y=100)
    tk.Label(label_frame, text="Max Speed", font=("Arial", 12, "bold")).place(
        x=10, y=130)

    # Show cars and their attributes
    for image_id, image_path in enumerate(car_images_tk):
        image = Image.open(image_path)  # Load image
        image = image.resize((80, 160))  # Resize image
        photo = ImageTk.PhotoImage(image)  # Convert to PhotoImage for Tkinter
        image_refs.append(photo)

        img_x = 175 + image_id * 120
        img_y = 100
        tk.Label(root, image=photo).place(x=img_x,
                                          y=img_y)  # Display car image

        attr_x = img_x + 15
        # Show car attributes (×10 for better visual values)
        tk.Label(root, text=f"{int(car_attributes[image_id][0] * 10)}",
                 font=("Arial", 10), justify="center", width=6).place(x=attr_x,
                                                                      y=270)
        tk.Label(root, text=f"{car_attributes[image_id][1] * 10}",
                 font=("Arial", 10), justify="center", width=6).place(x=attr_x,
                                                                      y=300)
        tk.Label(root, text=f"{int(car_attributes[image_id][2] * 10)}",
                 font=("Arial", 10), justify="center", width=6).place(x=attr_x,
                                                                      y=330)

        # "Choose" button to select this car
        btn = tk.Button(root, text="Choose",
                        command=lambda index=image_id: select_car(index,
                                                                  car_index,
                                                                  buttons))
        btn.place(x=img_x + 15, y=360)
        buttons.append(btn)

    buttons[0].config(bg="blue")  # Highlight first car as default

    # Difficulty selection buttons
    challenge_level = tk.StringVar(value="Normal")
    difficulty_x = 300
    difficulty_y = 430

    easy_btn = tk.Button(root, text="Easy", width=10,
                         command=lambda: select_difficulty("Easy",
                                                           challenge_level,
                                                           easy_btn,
                                                           normal_btn,
                                                           hard_btn))
    easy_btn.place(x=difficulty_x, y=difficulty_y)

    normal_btn = tk.Button(root, text="Normal", width=10,
                           command=lambda: select_difficulty("Normal",
                                                             challenge_level,
                                                             easy_btn,
                                                             normal_btn,
                                                             hard_btn))
    normal_btn.place(x=difficulty_x + 120, y=difficulty_y)

    hard_btn = tk.Button(root, text="Hard", width=10,
                         command=lambda: select_difficulty("Hard",
                                                           challenge_level,
                                                           easy_btn,
                                                           normal_btn,
                                                           hard_btn))
    hard_btn.place(x=difficulty_x + 240, y=difficulty_y)

    normal_btn.config(bg="yellow")  # Set default difficulty to Normal

    # Start game button
    start_btn = ttk.Button(root, text="Start Game", command=root.destroy,
                           style="Large.TButton")
    start_btn.place(x=450 - 75, y=500)

    # Set button style
    style = ttk.Style()
    style.configure("Large.TButton", font=("Arial", 14, "bold"), padding=15)

    root.protocol("WM_DELETE_WINDOW",
                  close_window)  # Handle window close button
    root.mainloop()  # Start the Tkinter event loop

    return car_index.get(), challenge_level.get()  # Return user selections


def read_high_score():
    try:
        # Try to open the file and read the high score
        with open("high_score.txt", "r") as file:
            return int(
                file.read().strip())  # Return the high score as an integer
    except FileNotFoundError:
        # If file doesn't exist, create it and write "0"
        with open("high_score.txt", "w") as file:
            file.write("0")
        return 0  # Return 0 as the default high score


def write_high_score(new_score):
    with open("high_score.txt", "w") as file:  # Open the file for writing
        file.write(str(new_score))  # Save the new high score as a string


class Background:
    def __init__(self, images, speed):
        self.images = images  # List of background images
        self.speed = speed  # Background scroll speed
        self.y0 = 0  # Y position of first background image
        self.y1 = -800  # Y position of second background image (on top)
        self.bg_num = 0  # Background switch counter

    def update(self, speed):
        # Move both background images down
        self.y0 += speed
        self.y1 += speed

        # If first image goes off-screen, reset its position
        if self.y0 >= 800:
            self.y0 = self.y1 - 800
            self.bg_num = (self.bg_num + 1) % len(
                self.images)  # Switch background type

        # If second image goes off-screen, reset its position too
        if self.y1 >= 800:
            self.y1 = self.y0 - 800

    def draw(self, screen):
        # Draw different backgrounds depending on bg_num
        if self.bg_num < 3:
            screen.blit(self.images[0], (0, self.y0))  # Main background
        else:
            screen.blit(self.images[1], (0, self.y0))  # Alternate background
        screen.blit(self.images[0],
                    (0, self.y1))  # Always draw second background


class Car:
    def __init__(self, x, y, car_num, car_x_speed, car_y_speed, max_speed,
                 images):
        self.x = x  # Car's x position
        self.y = y  # Car's y position
        self.car_num = car_num  # Index for car image
        self.car_x_speed = car_x_speed  # How fast the car moves left/right
        self.car_y_speed = car_y_speed  # How fast the car accelerates/decelerates
        self.max_speed = max_speed  # Car's top speed
        self.images = images  # All car images
        self.angle = 0  # Rotation angle
        self.image = self.images[self.car_num]  # Current image of the car
        self.mask = p.mask.from_surface(
            self.image)  # Used for pixel-perfect collision

    def check_collision(self, other_car):
        other_image = other_car.images[
            other_car.car_num]  # Get other car's image
        other_mask = p.mask.from_surface(
            other_image)  # Create mask for other car
        offset_x = other_car.x_pos_list[
                       other_car.x_pos_num] - self.x  # Distance between cars (x)
        offset_y = other_car.y - self.y  # Distance between cars (y)
        return self.mask.overlap(other_mask, (
            offset_x, offset_y))  # Check if masks overlap

    def update(self, speed):
        keys = p.key.get_pressed()  # Get key states

        # Move left
        if keys[p.K_LEFT] or keys[p.K_a]:
            if self.x > 45:
                self.x -= self.car_x_speed * (speed / self.max_speed)
                self.angle = min(15.0, self.angle + 0.6 * (
                        speed / self.max_speed))  # Turn left

        # Move right
        if keys[p.K_RIGHT] or keys[p.K_d]:
            if (self.x + 45) < (screen_size[0] -
                                car_images[self.car_num].get_width() - 100):
                self.x += self.car_x_speed * (speed / self.max_speed)
                self.angle = max(-15.0, self.angle - 0.6 * (
                        speed / self.max_speed))  # Turn right

        # Gradually straighten the car if no side keys are pressed
        if not (keys[p.K_LEFT] or
                keys[p.K_a] or
                keys[p.K_RIGHT] or
                keys[p.K_d]):
            if self.angle > 0:
                self.angle = max(0,
                                 self.angle - 0.6 * (speed / self.max_speed))
            elif self.angle < 0:
                self.angle = min(0,
                                 self.angle + 0.6 * (speed / self.max_speed))

        # Speed up
        if keys[p.K_UP] or keys[p.K_w]:
            if speed < self.max_speed:
                speed += self.car_y_speed
        else:
            speed = max(0,
                        speed - self.car_y_speed)  # Slowly reduce speed when not accelerating

        # Brake
        if keys[p.K_DOWN] or keys[p.K_s]:
            speed = max(0, speed - self.car_y_speed * 2)

        return speed  # Return updated speed

    def draw(self, screen):
        # Rotate the car image based on the angle
        rotated_image = p.transform.rotate(self.images[self.car_num],
                                           self.angle)
        # Get the new position after rotation (keep it centered)
        rotated_rect = rotated_image.get_rect(center=(
            self.x + car_images[self.car_num].get_width() // 2,
            self.y + car_images[self.car_num].get_height() // 2))
        screen.blit(rotated_image,
                    rotated_rect.topleft)  # Draw the rotated car


class ObstacleCar:
    def __init__(self, images, existing_cars):
        self.x_pos_list = [68, 195, 321, 448]  # Possible X positions (lanes)
        self.images = images  # List of car images
        self.x_pos_num = None  # Lane index
        self.y = None  # Y position of the car
        self.car_num = None  # Index of car image
        self.speed = None  # Vertical speed of the car
        self.passed = False  # If the player already passed this car
        self.reset_position(existing_cars)  # Place the car on screen

    def reset_position(self, existing_cars):
        self.passed = False  # Reset passed status

        # Find lanes that are not occupied by other cars
        occupied_lanes = [vehicle.x_pos_num for vehicle in existing_cars]
        free_lanes = []
        for lane in range(4):
            if lane not in occupied_lanes:
                free_lanes.append(lane)

        self.x_pos_num = random.choice(free_lanes)  # Choose a free lane
        # Random Y position above the screen (spawn point)
        self.y = random.randint(int(-3000 / difficulty_num),
                                int(-1500 / difficulty_num))
        self.car_num = random.randint(0,
                                      len(self.images) - 1)  # Random car image
        self.speed = random.uniform(0.8, 2)  # Random speed

    def update(self, bg_speed, existing_cars):
        self.y += (
                bg_speed + self.speed)  # Move down based on background speed

        # If the car moves off-screen, reset its position
        if self.y > screen_size[1] + self.images[self.car_num].get_height():
            self.reset_position(existing_cars)

    def draw(self, screen):
        # Draw the car upside down (facing the player)
        rotated_image = p.transform.rotate(self.images[self.car_num], 180)
        screen.blit(rotated_image, (self.x_pos_list[self.x_pos_num], self.y))


def game_state(bg_speed_current, obstacle_speed, is_game_over, player_score,
               best_score, player_car, game_running,
               current_obstacle_cars, current_bg):
    # Check if the game is over
    if is_game_over:
        # If player's score is higher than high score, update it
        if player_score > best_score:
            write_high_score(player_score)

        # Show "Game Over" image on the screen
        game_screen.blit(game_over_image, (34.75, 363))

        # Slowly move the player's car downward
        if player_car.y < 800:
            player_car.y += bg_speed_current + obstacle_speed

        # Gradually slow down background speed to 0
        bg_speed_current = max(0, bg_speed_current - 0.02)

        # Once speed reaches 0, show restart/quit options
        if bg_speed_current == 0:
            game_screen.blit(restart_image, (111.25, 500))
            keys = p.key.get_pressed()  # Check keyboard input

            if keys[p.K_r]:
                # Restart game if R key is pressed
                is_game_over, player_score, best_score, player_car, \
                    current_obstacle_cars, current_bg = \
                    reset_game(player_score, best_score)

                # Return updated game state
                return bg_speed_current, game_running, player_score, \
                    best_score, player_car, current_obstacle_cars, \
                    current_bg, is_game_over

            if keys[p.K_q]:
                # Quit game if Q key is pressed
                return bg_speed_current, False, player_score, best_score, \
                    player_car, current_obstacle_cars, current_bg, is_game_over

    # Return unchanged values if game is still running
    return bg_speed_current, game_running, player_score, best_score, \
        player_car, current_obstacle_cars, current_bg, is_game_over


def reset_game(current_score, current_high_score):
    # Update high score if current score is greater
    if current_score > current_high_score:
        current_high_score = current_score

    current_score = 0  # Reset the score to zero

    # Create a new player car with initial position and selected car's attributes
    player_car = Car(260, 600, car_id,
                     car_attributes[car_id][0],  # side speed
                     car_attributes[car_id][1],  # acceleration
                     car_attributes[car_id][2],  # max speed
                     car_images)

    # Generate a new list of obstacle cars
    current_obstacle_cars = []
    for j in range(3):
        if j == 0:
            # First obstacle car has an empty car list (no lane conflicts)
            current_obstacle_cars.append(ObstacleCar(car_images, []))
        else:
            # Later cars check against existing cars to avoid same lane
            current_obstacle_cars.append(
                ObstacleCar(car_images, current_obstacle_cars))

    # Create a new background with current scroll speed
    current_bg = Background(bg_images, scroll_speed)

    # Return the new game state
    return False, current_score, current_high_score, player_car, current_obstacle_cars, current_bg


def display_stats(speed, max_speed, current_distance, current_score,
                  current_game_state, current_high_score,
                  current_needle_angle):
    # Draw the side panel background
    game_screen.blit(bg_images[2], (600, 0))
    game_screen.blit(speedometer_image, (600, 700))  # Draw speedometer image
    game_screen.blit(circle_image, (645, 745))  # Draw center circle

    # Update needle angle if game is running
    if not current_game_state:
        current_needle_angle = 145 - 290 * (speed / max_speed)
    else:
        # Slowly return needle to the left when game is over
        if current_needle_angle < 145:
            current_needle_angle += 5

    # Rotate the needle and draw it
    rotated_needle = p.transform.rotate(needle_image, current_needle_angle)
    rotated_rect = rotated_needle.get_rect(center=(650, 750))
    game_screen.blit(rotated_needle, rotated_rect.topleft)

    # Increase distance while game is active
    if not current_game_state:
        current_distance += 0.033 * speed

    # Draw 4-digit distance (bottom to top)
    for n in range(4):
        digit = (int(current_distance) // (10 ** n)) % 10
        game_screen.blit(number_list[digit], (626, 375 - (n * 100)))

    game_screen.blit(m_image, (626, 475))  # Unit indicator ("m")

    # Draw 3-digit high score (small font)
    for n in range(3):
        digit = (current_high_score // (10 ** n)) % 10
        game_screen.blit(small_number_list[digit], (670 - (n * 30), 600))

    # Draw 3-digit current score (small font)
    for n in range(3):
        digit = (current_score // (10 ** n)) % 10
        game_screen.blit(small_number_list[digit], (670 - (n * 30), 650))

    return current_distance, current_score  # Return updated values


car_id, difficulty = start_menu()  # Launch the start menu and get selected car and difficulty

screen_size = (700, 800)  # Set game window size
game_screen = p.display.set_mode(screen_size)  # Create Pygame display
p.display.set_caption("car game")  # Set window title
p.display.set_icon(
    p.image.load("./Assets/game_icon.png").convert_alpha())  # Set window icon

# Load background images: [scrolling bg 1, scrolling bg 2, right panel]
bg_images = [
    p.transform.smoothscale(p.image.load("./Assets/bg-0.png").convert_alpha(),
                            (600, 800)),
    p.transform.smoothscale(p.image.load("./Assets/bg-1.png").convert_alpha(),
                            (600, 800)),
    p.image.load("./Assets/bg-right.png").convert_alpha()
]

# Load and resize 6 car images
car_images = []
for i in range(1, 7):
    car_image = p.image.load(f"./Assets/car_{i}.png").convert_alpha()
    car_images.append(p.transform.smoothscale(car_image, (80, 160)))

# Load 0–9 large number images for distance display
number_list = []
for i in range(0, 10):
    number = p.image.load(f"./Assets/{i}.png").convert_alpha()
    modified_number = p.transform.smoothscale(number, (48, 72))
    number_list.append(modified_number)

# Load 0–9 small number images for score and high score display
small_number_list = []
for i in range(0, 10):
    number = p.image.load(f"./Assets/{i}.png").convert_alpha()
    modified_number = p.transform.smoothscale(number, (24, 36))
    small_number_list.append(modified_number)

# Load supporting UI images
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

high_score = read_high_score()  # Load saved high score from file
distance = 0  # Initial distance
score = 0  # Initial score

# Set FPS and difficulty multiplier based on selected difficulty
if difficulty == "Easy":
    FPS = 150
    difficulty_num = 1
elif difficulty == "Normal":
    FPS = 175
    difficulty_num = 2
else:
    FPS = 200
    difficulty_num = 3

game_over = False  # Game is running
scroll_speed = 0  # Initial background speed
collide_car_speed = 0  # Speed of the car that causes collision
needle_angle = 145  # Initial angle of the speedometer needle

# Create the player car using selected car's stats
car = Car(260, 600, car_id,
          car_attributes[car_id][0],  # side speed
          car_attributes[car_id][1],  # acceleration
          car_attributes[car_id][2],  # max speed
          car_images)

# Create obstacle cars based on difficulty level
obstacle_cars = []
for i in range(difficulty_num):
    if i == 0:
        obstacle_cars.append(
            ObstacleCar(car_images, []))  # First car — no conflict check
    else:
        obstacle_cars.append(
            ObstacleCar(car_images, obstacle_cars))  # Avoid same lane

# Create background object
bg = Background(bg_images, scroll_speed)
running = True  # Game loop control flag
while running:
    events = p.event.get()  # Get all events
    for event in events:
        if event.type == p.QUIT:  # If user closes the window, exit the loop
            running = False

    # Update game elements only if the game is not over
    if not game_over:
        scroll_speed = car.update(scroll_speed)  # Update player car's speed

    bg.update(scroll_speed)  # Move background based on scroll speed
    bg.draw(game_screen)  # Draw background
    car.draw(game_screen)  # Draw player car

    # Update and draw obstacle cars
    for obstacle_car in obstacle_cars:
        obstacle_car.update(scroll_speed,
                            obstacle_cars)  # Move obstacle car down
        obstacle_car.draw(game_screen)  # Draw obstacle car

        # Check collision between player car and obstacle car
        if car.check_collision(obstacle_car):
            collide_car_speed = obstacle_car.speed  # Save the speed of colliding car
            game_over = True  # End the game

        # If an obstacle car moves off the screen, update score
        if obstacle_car.y > screen_size[1]:
            if not obstacle_car.passed and not game_over:
                score += difficulty_num  # Increase score based on difficulty
                obstacle_car.passed = True  # Mark car as passed

    # Update game state variables (speed, running status, score, etc.)
    scroll_speed, running, score, high_score, car, obstacle_cars, bg, game_over \
        = game_state(scroll_speed, collide_car_speed, game_over, score,
                     high_score, car, running, obstacle_cars, bg)

    # Update stats display (speed, distance, score)
    distance, score = display_stats(scroll_speed, car.max_speed, distance,
                                    score, game_over, high_score, needle_angle)

    p.display.update()  # Refresh screen with updated graphics
    p.time.Clock().tick(FPS)  # Control frame rate

# Quit the game after exiting the loop
p.quit()
sys.exit()
