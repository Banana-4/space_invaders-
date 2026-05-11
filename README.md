# About
This project is a simple clone of the game space invaders. The goal is to play around with pygame, python and programm design.
The end result should be a working game and not a perfect program.

# Space Invaders
The player task is to destroy a incoming invading alien fleet. For this purpose a defensive turret with a mounted gun is provided. The turret moves left and right and fires a plasma round at the incoming space ships.
As the fleet moves down in left right motion it gains speed and the space ships are firing at the turret. The player is protected by static shields in front of him that are destroyable, the turret has 3 hitpoints.
Each space ship gives the player points for destruction, the amount of points is determined by the line in which the space ships are:
1. first line gives 5 points
2. second line gives 10 points.
3. third line gives 15 points.
4. forth line gives 20 points.
There is also a spceial space ship that spawns randomly at the top and goes from right to left that gives extra points 50 on destruction.
Between each space ship there is a gap through which the plasma round can pass through.

## Game rules:
### Win lose conditions:
1. The player wins if he/her destroys all the space shhips of the fleet.
2. The invaders win if only one ship reachs the bottom.

### Player rules:
1. the player can move the turret left right, from one edge of the screen to the other.
2. The player can shoot a gun.
3. The turret can take 3 hits from the space ships.

### How the shooting works:
1. The round collides with and destroys any object it hits.
2. it does not penetrate anything and is destroyed on hit.
3. the Bullet is 2px wide and 5px heigh.

### Shields:
1. The shilds are made from destructiable pices.
2. The pices can be destroy by player or alien hits.
3. The shield have a max height of 20 px heigh and a min height of 15px. The width is 30px
4. The space between shields is 30 px wide.

### Space ships:
1. The move left or right. When one ship touches the end of the screen they move down and change direction.
2. One hit from the player destroies them.
3. At each down step theire speed increases by a amount based on the ships left in the fleet. 

# Instalation Instructions:

# Design
The main design principles are OOP. 

## Modules
1. Game - this module is responsiable for creating a environment and coordinating other modules to form the game loop.
2. Entities - this module is responsiable for storing and changing data of game entites.
3. GUI - for menus.
4. Sound - game sound engine.
5. File i/o - for saving and loading settings, highscores...
6. Event messaging subsystem.
7. Player input - for controlls.



## File organization:

