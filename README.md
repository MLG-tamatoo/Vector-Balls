# Vector-Balls
This is a game about vectors, Vector calculus, and balls. It was created for an Honors Enrichment Contract at Arizona State University for the MAT 267 Fall of 2023 for Dr. Scott Surgent by, engineering student, Connor Owens.

This project started as a way to represent the use of vectors with a simple collision simulation in Python. The current aim of this project is to create an accurate simulation of an 8-ball game.

# Future Goals With The Project
* fix the collision bug - If a ball hits the left bottom corner of the rectangle with a velocity vector A, the collision system returns the resultant velocity vector B. If another ball hits the top left corner of the ball with velocity vector A, the resultant vector would be B. This is because the collision calculation takes only the velocity vectors of the objects into account as if they are single-point particles. - fix this by updating the collision calculations to be dependent on the respective object positioning.
* Create a “true” 8-ball game mode - once the collision bug is fixed
* Create more interesting levels
* Create past-level playability - there is some code for this now but it doesn't work
* Add a level win animation/message or something

# A Project Review 2023
The file called project review was a review of the development for the project as part of the Honors Enrichment Contract this project stemmed from. I included this in the repo because I think it sheds light on why the code is structured the way it is: why use pack, variable names, ect. I think the code could be rewritten in a much more efficient and elegant manner to address the now 8-ball style of the game.
