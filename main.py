import pygame, sys, math, random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Essential variables
g = 1  # Gravity
bullets = [] # List of bullets
drones = [] # List of drones
game_duration = 60  # Game duration in seconds
game_start_time = pygame.time.get_ticks() # Game start time
reset = False # Reset the game
currentScreen = "Main Menu" # Set screens to display

# Set up the window
width = 1200
height = 600
screen_center_x = width/2
screen_center_y = height/2
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Robot vs Drones")

# Set up the clock
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
GREY = (128, 128, 128)

# Sounds
shotSound = pygame.mixer.Sound("sounds/shot.wav")
explosionSound = pygame.mixer.Sound("sounds/explosion.mp3")
splashSound = pygame.mixer.Sound("sounds/splash.wav")
jumpSound = pygame.mixer.Sound("sounds/jump.wav")
loseSound = pygame.mixer.Sound("sounds/lose.wav")
buttonsSound = pygame.mixer.Sound("sounds/buttons.wav")
        

################################ PLAYER ################################
class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("images/player.png")
        self.x = 100
        self.mass = 30
        self.y = height - self.image.get_height() - 10
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.jumpForce = 15
        self.acceleration = 0.5
        self.t = 0.05
        self.velocity = 0
        self.score = 0
        self.onGround = True
        self.angle = 0
        self.update_collider()
        self.velocity_x = 0
        self.static_friction_coefficient = 1.2
        self.kinetic_friction_coefficient = 1
        self.move_speed = 80
        
    # Apply gravity
    def applyGravity(self):
        self.velocity += self.acceleration * g
        self.y += self.velocity
    
    # Apply friction
    def applyFriction(self):
        if self.onGround:
            if self.velocity_x > 0:
                self.velocity_x -= self.static_friction_coefficient * g
                if self.velocity_x < 0:
                    self.velocity_x = 0
            elif self.velocity_x < 0:
                self.velocity_x += self.static_friction_coefficient * g
                if self.velocity_x > 0:
                    self.velocity_x = 0
        else:
            if self.velocity_x > 0:
                self.velocity_x -= self.kinetic_friction_coefficient * g
                if self.velocity_x < 0:
                    self.velocity_x = 0
            elif self.velocity_x < 0:
                self.velocity_x += self.kinetic_friction_coefficient * g
                if self.velocity_x > 0:
                    self.velocity_x = 0
                 
    # Move left   
    def moveLeft(self):
        self.velocity_x = -self.move_speed
    
    # Move right
    def moveRight(self):
        self.velocity_x = self.move_speed
    
    # Jump with gravity
    def jump(self):
        if self.onGround:
            self.velocity = -self.jumpForce
            self.onGround = False
    
    # Update the player's collider
    def update_collider(self):
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)  
            
    def update(self):
        # Apply gravity
        self.applyGravity()
        
        # Apply friction
        self.applyFriction()
        
        # Update player's position on the x-axis
        self.x += self.velocity_x * self.t
        
        # Check if the player is off the screen
        if self.x < 0:
            self.x = 0
        elif self.x > width - self.width:
            self.x = width - self.width
        # Check if the player is on the ground
        if self.y >= height - self.height - 80:
            self.onGround = True
            self.y = height - self.height - 80
            self.velocity = 0
        else:
            self.y += g
        # Check if the player is off the screen
        if self.y > height:
            self.y = 0

        # Mouse input
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(self.y - mouse_y, mouse_x - self.x)
        self.angle = min(max(angle, -math.pi/15), math.pi/2.5)
        
        self.update_collider()
    
    # Draws the player
    def draw(self):
        # Draw player
        screen.blit(self.image, (self.x, self.y))
        
        # Draw cannon
        end_x = self.x + 25 * math.cos(self.angle)
        end_y = self.y - 25 * math.sin(self.angle)
        pygame.draw.line(screen, BLACK, (self.x + 20, self.y + 35), (end_x + 20, end_y + 35), 5)
    
    # Get the player's score
    def getScore(self):
        return self.score
        
    # Reset the player
    def reset(self):
        # Reset the player object to its original state
        self.__init__()

################################ BULLETS ################################
class Bullet(object):
    def __init__(self, player, time):
        self.x0 = player.x + 25
        self.y0 = player.y + 30
        self.x = self.x0
        self.y = self.y0
        self.angle = player.angle
        self.radius = 5
        self.v0 = 100
        self.g = 9
        self.dt = time
        self.t = 0
        self.update_collider()

    # Update the bullet's position and velocity
    def update(self):
        # Update the time
        self.t += self.dt

        # Calculate the bullet's velocity on each axis
        self.vx0 = self.v0 * math.cos(self.angle)  # Initial horizontal velocity
        self.vy0 = self.v0 * math.sin(self.angle)  # Initial vertical velocity

        # Calculate the bullet's position on each axis
        self.x = self.x0 + (self.vx0 * self.t)  # Horizontal position
        self.y = self.y0 - (self.vy0 * self.t) + (0.5 * self.g * self.t**2)  # Vertical position
        
        # Update the bullet's collider
        self.update_collider()
    
    # Update the bullet's collider
    def update_collider(self):
        self.collider = pygame.Rect(self.x, self.y, self.radius, self.radius)

    # Draw the bullet
    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius)

################################ DRONES ################################
class Drone(object):
    def __init__(self):
        self.image = pygame.image.load("images/drone.png")
        self.x = 1300
        self.y = random.randint(50,400)
        self.mass = 1.5
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed_x = random.randint(4,6)
        self.speed_y = 0
        self.spawn_timer = random.randint(1000,2500) # Random time between 1,5 to 3 seconds
        self.alive = True
        self.insideWater = False
        self.scoreAdded = False
        self.update_collider()
    
    # Update the drone's collider
    def update_collider(self):
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
    
    # Update the drone's position based if it is alive or not and if it is inside the water
    def update(self, water_tank):
        # Check if the drone is alive
        if self.alive:
            self.x -= self.speed_x
        # Check if the drone is not alive
        elif not self.alive:
            self.speed_y += g
            self.y += self.speed_y
        # Check if the drone is on the water
        if self.insideWater:
            self.x = water_tank.x + 20
            
            # Calculate the submerged depth
            submerged_depth = (self.y + self.height) - water_tank.water_level
            
            # Calculate the submerged volume
            submerged_volume = 0.4 * submerged_depth / self.height
            
            # Calculate the buoyant force
            buoyant_force = water_tank.water_density * g * submerged_volume
            
            # Calculate the net force
            net_force = self.mass * g - buoyant_force
            
            # Apply the net force to the drone's position
            acceleration = net_force / self.mass
            self.y += acceleration
            
            # Check if the drone goes below the lowest point of the water tank
            if self.y + self.height >= water_tank.y + water_tank.height:
                # Stop the drone from going further down
                self.y = water_tank.y + water_tank.height - self.height 
    
        self.update_collider()
    
    # Draw the drone
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        
################################ WATER TANK ################################
class WaterTank(object):
    def __init__(self):
        self.image = pygame.image.load("images/water_tank.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = 1300
        self.y = height - 120
        self.water_level = height - 120
        self.water_density = 60
        self.move_speed = 3
        self.spawn_timer = random.randint(10000, 20000) # random spawn time between 10 and 20 seconds
        self.last_spawn_time = pygame.time.get_ticks() # keep track of the last spawn time
        self.update_collider()
    
    # Update the water tank's collider
    def update_collider(self):
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
    
    # Update the water tank's position and draw it
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_timer:
            self.last_spawn_time = current_time
            self.spawn_timer = random.randint(10000, 20000)
            self.start_time = pygame.time.get_ticks()
        if self.x > -(self.image.get_width()):
            screen.blit(self.image, (self.x, self.y))
            self.x -= self.move_speed
        else:
            self.x = 1300
        self.update_collider()
    
    # Reset the water tank's position
    def reset(self):
        # Reset the water tank's
        self.__init__()
    
################################ START SCREEN ################################
def startScreen():
    # Get the global variable currentScreen
    global currentScreen
    
    # Create Font 
    fontStartScreen = pygame.font.Font(None, 100)
    titleFont = pygame.font.Font(None, 150)
    
    # Create text labels for the tile, the start button and the exit button
    title = titleFont.render("ROBOT VS DRONES", True, GREY)
    startButton = fontStartScreen.render("Start", True, BLACK)
    leaderboardButton = fontStartScreen.render("Leaderboard", True, BLACK)
    exitButton = fontStartScreen.render("Exit", True, BLACK)

    # Create the buttons
    startButtonRect = startButton.get_rect()
    startButtonRect.center = (screen_center_x, screen_center_y - 50)
    leaderboardButtonRect = leaderboardButton.get_rect()
    leaderboardButtonRect.center = (screen_center_x, screen_center_y + 50)
    exitButtonRect = exitButton.get_rect()
    exitButtonRect.center = (screen_center_x, screen_center_y + 150)

    # Check if the mouse is over the buttons
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # If the mouse is over the start button
    if startButtonRect.collidepoint(mouse):
        # Change the color of the button to grey
        startButton = fontStartScreen.render("Start", True, GREY)
        
        if click[0] == 1:
            buttonsSound.play()
            currentScreen = "Game"
            
    # If the mouse is over the leaderboard button
    if leaderboardButtonRect.collidepoint(mouse):
        # Change the color of the button to grey
        leaderboardButton = fontStartScreen.render("Leaderboard", True, GREY)
        
        if click[0] == 1:
            buttonsSound.play()
            currentScreen = "Leaderboard"
            
    # If the mouse is over the exit button
    if exitButtonRect.collidepoint(mouse):
        # Change the color of the button to grey
        exitButton = fontStartScreen.render("Exit", True, GREY)
        
        if click[0] == 1:
            buttonsSound.play()
            pygame.quit()
            sys.exit()
    
    # Draw title
    screen.blit(title, (screen_center_x - title.get_width()/2, screen_center_y - 250))
    # Draw buttons
    screen.blit(startButton, startButtonRect)
    screen.blit(leaderboardButton, leaderboardButtonRect)
    screen.blit(exitButton, exitButtonRect)

################################ LEADERBOARD SCREEN ################################
def write_to_leaderboard(player, screen):
    # Read the scores from the leaderboard.txt file
    scores = []
    with open("leaderboard.txt", "r") as f:
        for line in f:
            score, initials = line.strip().split(",")
            scores.append((int(score), initials))
            
    # Sort the scores in descending order by score
    scores = sorted(scores, key=lambda x: x[0], reverse=True)
    font = pygame.font.Font(None, 25)
    prompt_font = pygame.font.Font(None, 40)
    
    # Prompt the player to enter their initials if their score is one of the top 10 scores
    if len(scores) < 10 or player.getScore() > scores[9][0]:
        input_box = pygame.Rect(screen_center_x - 50, screen_center_y - 30, 100, 30)
        color = BLACK
        text = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        initials = text.upper()
                        if len(initials) != 3:
                            print("Error: Initials must be 3 characters long.")
                        else:
                            with open("leaderboard.txt", "a") as f:
                                f.write(f"{player.getScore()},{initials}\n")
                            return
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif len(text)<3:
                        text += event.unicode
                text = text.upper()
            # Clear the screen
            screen.fill(WHITE)
            
            # Render the text
            txt_surface = font.render(text, True, color)
            txt_rect = txt_surface.get_rect(center=input_box.center)
            
            # Create input box
            pygame.draw.rect(screen, color, input_box, 2)
            
            # Blit the text
            screen.blit(txt_surface, txt_rect)
            
            # Render and blit the prompt text
            prompt_text_surface = prompt_font.render("Enter your initials (3 characters required):", True, color)
            prompt_text_rect = prompt_text_surface.get_rect()
            prompt_text_rect.center = (screen_center_x, screen_center_y - 75)
            screen.blit(prompt_text_surface, prompt_text_rect)
            
            pygame.display.flip()

def display_scores(scores, screen):
    # Create a font object
    font = pygame.font.Font(None, 40)
    leaderboard_font = pygame.font.Font(None, 100)
    score_surfaces = []
    score_rects = []
    y_offset = 0
    
    for score in scores:
        # Create a surface with the leaderboard text
        leaderboard_text = leaderboard_font.render("Leaderboard", True, GREY)
        # Get the dimensions of the surface
        leaderboard_rect = leaderboard_text.get_rect()
        # Set the position of the surface
        leaderboard_rect.center = (screen_center_x, 60)
        # Create a surface with the score
        score_surface = font.render(score, True, BLACK)
        # Get the dimensions of the surface
        score_rect = score_surface.get_rect()
        # Set the position of the surface
        score_rect.center = (screen_center_x, screen_center_y - 175 + y_offset)
        # Add the surface and rect to the lists
        score_surfaces.append(score_surface)
        score_rects.append(score_rect)
        # Increment the y offset
        y_offset += 50
        
    # Clear the screen
    screen.fill(WHITE)
    
    # Draw the scores surfaces on the screen
    for score_surface, score_rect in zip(score_surfaces, score_rects):
        screen.blit(score_surface, score_rect)
    screen.blit(leaderboard_text, leaderboard_rect)
    
    # Update the display
    pygame.display.flip()

def display_leaderboard(screen):
    scores = []
    with open("leaderboard.txt", "r") as f:
        for line in f:
            score, initials = line.strip().split(",")
            scores.append((int(score), initials))
            
    # Sort the scores in descending order by score
    scores = sorted(scores, key=lambda x: x[0], reverse=True)
    
    # Keep track of the number of scores that have been added to the leaderboard
    num_scores_added = 0
    leaderboard_text = []
    for i, (score, initials) in enumerate(scores[:10]):
        leaderboard_text.append(f"{initials}: {score}")
        num_scores_added += 1
        
    # Add the player's score and initials to the leaderboard if it is one of the top 10 scores
    if num_scores_added < 10 and Player.getScore() >= scores[num_scores_added][0]:
        leaderboard_text.append(f"{initials}: {Player.getScore()}")
        num_scores_added += 1
        
    # Display the scores on the screen
    display_scores(leaderboard_text, screen)
    
    # Update the display
    pygame.display.update()
    
    # Wait for 6 seconds or until the player exits the screen
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 6000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
    # Return to the main menu
    global currentScreen
    currentScreen = "Main Menu"

################################ GAME OVER SCREEN ################################
def gameOverScreen():
    # Set the background color to black
    screen.fill(WHITE)
    # Display the game over message
    font = pygame.font.Font(None, 170)
    text = font.render("GAME OVER", True, BLACK)
    text_rect = text.get_rect()
    text_rect.centerx = screen_center_x
    text_rect.centery = screen_center_y
    screen.blit(text, text_rect)
    loseSound.play()
    # Update the display
    pygame.display.flip()
    # Wait for 2 seconds
    pygame.time.delay(2000)

################################ GAME OVER ################################
def game_over(player):
    global reset
    reset = False
    # Display the game over screen
    gameOverScreen()
    # Write the player's score and initials to the leaderboard
    write_to_leaderboard(player, screen)
    # Display the leaderboard
    display_leaderboard(screen)

def gameReset(player, waterTank):
    # Call the global variables
    global game_duration, game_start_time
     # Reset the game
    drones.clear()
    bullets.clear()
    player.reset()
    waterTank.reset()
    # Reset game duration
    game_duration = 60
    # Reset the game start time
    game_start_time = pygame.time.get_ticks()

################################ GAME LOOP ################################
def main():
    # Check if the game is running
    running = True
    
    # Background stuff
    bg = pygame.image.load("images/BG.png").convert()
    bg_width = bg.get_width()
    scroll = 0
    tiles = math.ceil(width / bg_width) + 1
    
    # Track the time for bullet firing
    last_shot_time = 0
    fire_rate = 1  # Fire rate in seconds
    
    # Set the initial drone, hot ballon and blade spawn times
    last_drone_spawn_time = pygame.time.get_ticks()
    
    # Create the player
    player = Player()
    waterTank = WaterTank()
    
    # Score font
    score_font = pygame.font.Font(None, 30) # Score font
    time_font = pygame.font.Font(None, 30)  # Time font
    
    # Global variables
    global game_duration, game_start_time, reset
    
    while running:
        # Set the FPS
        clock.tick(FPS)
        
        # Get the current time
        current_time = pygame.time.get_ticks()
        
        # Calculate the elapsed time
        elapsed_time = (current_time - game_start_time) // 1000
        
        # Score text renderer
        score_text = score_font.render("Score: " + str(player.score), 1, WHITE) # Updating the score
        time_text = time_font.render("Time: " + str(game_duration - elapsed_time), 1, WHITE)  # Updating the time

        # Process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        
        # Current screen is the main menu
        if currentScreen == "Main Menu":
            startScreen()
        
        # Current screen is the game
        elif currentScreen == "Game":
            if not reset:
                gameReset(player, waterTank)
                reset = True
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and player.onGround:
                player.jump()
                jumpSound.play()
            # move player left and right
            if keys[pygame.K_a]:
                player.moveLeft()
            elif keys[pygame.K_d]:
                player.moveRight()    
            # Fire a bullet
            if pygame.mouse.get_pressed()[0]:
                current_time = pygame.time.get_ticks()  # Get current time in milliseconds
                # Check if enough time has elapsed since the last shot
                if current_time - last_shot_time >= fire_rate * 1000:
                    bullets.append(Bullet(player, 0.2))
                    last_shot_time = current_time  # Update the last shot time
                    shotSound.play()
            
            # Draw scrolling background
            for i in range (0, tiles):
                screen.blit(bg, (i * bg_width + scroll,0))
            scroll -= 3
            if abs(scroll) > bg_width:
                scroll = 0
                
            # Update and draw bullets
            for bullet in bullets:
                bullet.update()
                bullet.draw(screen)
                # Remove bullets that go off screen
                if (bullet.x > width or bullet.x < 0) or (bullet.y < -height):
                    bullets.remove(bullet)
                # Check collisions between bullets and drones
                for d in drones:
                    if bullet.collider.colliderect(d.collider):
                        if bullet not in bullets:
                            pass
                        else:
                            bullets.remove(bullet)
                        d.alive = False
                        player.score += 1
                        game_duration += 1
                        explosionSound.play()
                
            # Update and draw water tank
            waterTank.update()  
                
            # New drone update and draw
            new_drone = Drone()
            # Check if enough time has elapsed since the last drone spawn and if there are less than 5 drones on the screen
            if current_time - last_drone_spawn_time > new_drone.spawn_timer and len(drones) < 5:
                drones.append(new_drone)
                last_drone_spawn_time = current_time
            # Update and draw drones
            for d in drones:
                d.update(waterTank)
                # Check collisions between player and drones
                if d.collider.colliderect(player.collider):
                    game_over(player)
                # Check if drone gets out of the screen
                if d.x < -100:
                    drones.pop(drones.index(d))
                if d.y > height:
                    drones.remove(d)
                # Check if drone gets inside the water tank
                if (waterTank.x < d.x + d.width < waterTank.x + waterTank.width and waterTank.y <= d.y + d.height <= waterTank.y + waterTank.height) and (waterTank.x < d.x < waterTank.x + waterTank.width and waterTank.y <= d.y <= waterTank.y + waterTank.height) and (waterTank.x < d.x + d.width < waterTank.x + waterTank.width and waterTank.y <= d.y <= waterTank.y + waterTank.height) and (waterTank.x < d.x < waterTank.x + waterTank.width and waterTank.y <= d.y + d.height <= waterTank.y + waterTank.height):
                    d.insideWater = True
                    # Add player score and time
                    if d.insideWater and not d.scoreAdded:
                        player.score += 5
                        game_duration += 5
                        d.scoreAdded = True
                        splashSound.play()
                d.draw()
                
            # Check collisions between player and water tank
            if player.collider.colliderect(waterTank.collider):
                game_over(player)
                
            # Update the player
            player.update()    
            
            # Draw the player
            player.draw()
            
            # Show the score and time
            screen.blit(score_text, (width - score_text.get_width() - 25, 10))
            screen.blit(time_text, (width - time_text.get_width() - 25, 50))

            # Check game duration
            if elapsed_time >= game_duration:
                game_over(player)
        
        # Current screen is the leaderboard
        elif currentScreen == "Leaderboard":
            display_leaderboard(screen)

        pygame.display.flip()

# Run the main function
if __name__ == "__main__":
    main()