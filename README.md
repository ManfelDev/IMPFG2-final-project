# Robot vs Drones
## By: Rafael José - a22202078

### Instructions:
To run the program, the player needs to have Python installed, as well as the Pygame library. Then simply run the main.py file in the folder. The player will see the main menu, where they can choose the "Play" option to start the game. In the game, the player must use space or the W key to jump, A to move left and D to move right, and shoot using the mouse position and clicking the left button. The player must hit the drones to earn points. The player earns more points if they hit the drone and it falls into a water tank. All this in 60 seconds of play, which increases by one second for each point in the player's score. The player can lose the game instantly if they hit a drone while jumping or when the drone is in freefall and falls on them, or if they crash into a water tank. At the end, if the player scores higher than the top 10 on the *leaderboard*, they can enter their initials to enter the table.

### Introduction:
The project in question consists of developing a game using the Python programming language and the Pygame library. The aim is to create a game that is graphically simple but enjoyable to watch and play, following good game design practices. The game implements various aspects of kinematic physics, such as free fall, projectile/ball movement, friction and friction forces, collisions, buoyancy physics and jumping with physics and acceleration. 

The main objectives of this project were to offer players a fun and engaging experience, applying concepts of kinematic physics in a practical way, through a robot, with a cannon instead of an arm, which fires bullets with the aim of destroying the drones that are in its direction, each drone down gives 1 point in the player's score, and if he hits that drone in a water tank it will give him another 5 in the score, but beware the drone must all be in the water tank, otherwise it will ignore it and just fall, for a greater challenge. The whole game is controlled by time, and each point in the score adds 1 second to the timer. To achieve these objectives, it was necessary to implement the game's logic, create the graphic elements, manage the player's interactions with the environment and carry out the appropriate physical calculations for each interaction required. 

At the end of development, the game achieved satisfactory results, providing fluid and engaging gameplay. Aspects of kinematic physics were implemented realistically, allowing objects to move and interact according to the corresponding physical laws. The use of graphics, sounds and interactions contributed to the player's immersion in the game environment.

### Methodology
Starting with the player, physics is applied to all his movements through two functions. (applyGravity) the player's vertical velocity (self.velocity) is updated by multiplying the acceleration (self.acceleration) by gravity (g) and adding it to the current velocity. This simulates the effect of gravity on the player, and causes them to accelerate downwards, this is given for a more realistic jumping effect. (applyFriction) This method applies friction to the player, the friction behavior depends on whether the player is on the ground or in the air. It adjusts the horizontal velocity (self.velocity\_x) based on the friction coefficients (self.friction\_coefficient and self.kinetic\_friction\_coefficient) multiplied by gravity (g). It also contains a component that checks the position of the mouse from which the player will aim their cannon, which is also transformed into an angle so that the projection of the projectile through the tip of the cannon can later be calculated. It also has a collider based on its position on each axis, x and y, and its height and length.

The bullet fired from the tip of the player's cannon has a ball shape and is launched by calculating the velocity on each axis at its initial moment (Vx = V0 \* cos(theta) & Vy = V0 \* sen(theta)), and then updating its position on each of its axes, x and y (x = x0 + (vx \* dt) & y = y0 - (vy \* dt) + (½ \* g \* dt\*\*2)). It also has a collider based on its position on each axis, x and y, and its radius.

The drones, which are placed in the game with a random y position and a random spawn time, need to check their status in order to update their movement. If a drone has not been hit by the player, it will have a negative uniform rectilinear movement along the x axis (x = x - v), this speed is constant and can vary from drone to drone. If it is hit by the player, it will begin a free-fall movement, where the x component stops updating, and where the y axis starts updating, where the force of gravity (g) will accelerate the object in y until it reaches the bottom of the screen. Finally, if the drone hits a water tank while it is falling, it will undergo a buoyancy effect, where the immersion depth is calculated (submerged\_depth = (y + height) - water level), the immersion volume (submerged\_volume = 0. 4 \* submerged\_depth/ height), the buoyancy force (F buoyant = water density \* g \* submerged\_volume), the net force is calculated (net\_force = mass \* g - F buoyant) and finally it is applied to the drone's position (acceleration = net\_force / mass) & (y += acceleration), and when it reaches the bottom of the tank it stops.

The last object in play is the water tank, which contains all the variables of the water, such as its density and level. Like the drones, it has a random spawn time, but longer than the drones. It only has one speed, on the x-axis, just like the drones before they are hit (x = x - v). 

The main menu displays the game's home screen, showing the game title and the "Start", "Leaderboard" and "Exit" buttons. The buttons are interactive and respond to mouse clicks. Clicking "Start" starts the game, clicking "Leaderboard" displays the leaderboard and clicking "Exit" ends the game. This function is responsible for creating an intuitive user interface and allowing players to easily navigate through the options available at the start of the game.

The leaderboard is divided into several functions. The write\_to\_leaderboard function is responsible for this functionality. It reads the existing scores from a file called "leaderboard.txt" and stores them in a list. The scores are then sorted in descending order based on the score value. If the player's score is higher than the 10th score in the list, the player is prompted to enter their initials. A loop is run to capture the keys typed by the player, allowing them to enter their initials. With each iteration of the loop, the screen is updated to display the initials entered. When the player presses the "Enter" key, the initials are saved in the "leaderboard.txt" file along with the player's score.

The display\_scores function is responsible for displaying the scores on the screen. It receives a list of scores and iterates over them to create text surfaces with the scores. Each text surface is positioned vertically based on an offset, to ensure that all the scores are displayed correctly. The screen is cleaned and filled with the color white, and the text surfaces of the scores are drawn on the screen.

The display\_leaderboard function reads the existing scores from the "leaderboard.txt" file and stores them in a list. The scores are sorted in descending order based on the score value. A limited number of scores are then selected for display on the leaderboard. If the player's score is among the top 10 scores, it is added to the leaderboard. The scores are displayed on the screen using the display\_scores function. After that, the screen is refreshed and the game waits for a period of time before returning to the main menu.

Finally, the *game loop*, the main function where several essential steps are carried out for the game to work. This is where event detection is done to capture actions. Depending on the current game screen, the corresponding function is called. In the game, the keys pressed by the player are checked to move the character and shoot projectiles. The background is drawn and updated to create a displacement effect. Projectiles can be fired based on a time interval, guaranteeing a firing rate limit. The drones' behavior is updated and checked for collisions with the player, bullets, leaving the screen and entering the water tank. The player is also updated and drawn on the screen, as is the water tank. In addition, important information is displayed on the screen, such as the player's score and the remaining game time. There are checks to end the game if the time limit is reached.

### References
#### Art:
Anonymous. (2012, April 11). *Several scrolling backgrounds and layerable “runners.”* OpenGameArt.org. <https://opengameart.org/content/several-scrolling-backgrounds-and-layerable-runners> 

bubaproducer. (2012, April 8). *Laser shot silenced by Bubaproducer*. Freesound. <https://freesound.org/people/bubaproducer/sounds/151022/> 

cabled\_mess. (2016, December 22). *Lose\_Funny\_Retro\_Video game by cabled\_mess*. Freesound. <https://freesound.org/people/cabled_mess/sounds/371451/> 

JuveriSetila. (2020, April 19). *Medium explosion.mp3 by Juverisetila*. Freesound. <https://freesound.org/people/JuveriSetila/sounds/514133/> 

MATRIXXX\_. (2022, November 7). *SciFi inspect sound, UI, or in-game notification 01.wav by Matrixxx\_*. Freesound. <https://freesound.org/people/MATRIXXX_/sounds/657945/> 

simon.rue. (2008, October 28). *Boink\_v3.wav by simon.rue*. Freesound. <https://freesound.org/people/simon.rue/sounds/61847/>  