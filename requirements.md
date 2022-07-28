# Software Requirements
## Vision

This product seeks to alleviate stress through the power of entertainment while simultaneously providing real-time
cryptocurrency rates through a fun little crypto mining game. People should care because, like it or not, blockchain
and, by extension, cryptocurrency has become relevant in our modern lives. But simply checking it online can be 
stressful, so combining it with a smile inducing game may counterbalance that stress. 

## Scope (In/Out)
* IN - This product will:
  * Let the player traverse a 2D plane to fly through space, land on asteroids, and mine ores.
  * Allow the user to look up crypto prices in real time using an API.
  * The player can upgrade their character to mine more efficiently and fight off enemies.
  * The game will include animated 16x16 graphics.

* OUT - This product will not:
  * This app will not trade cryptocurrency.
  * This game will not support multiplayer.

### Minimum Viable Product:

Our MVP will include a single player object that can navigate several 2D tile maps to interact with other objects such 
as asteroids, ores, and alien enemies. The player will be able to upgrade their ship and their character to travel and 
mine more efficiently. The game will track high score based on currency earned and the game ends with the player's death.

### Stretch
- Build a backend application with full CRUD functionality that the main game module can make API calls on.
- Host the backend in serverless function services like AWS Lambda or Vercel


## Functional Requirements
A user can start, save, and load a game.

### Data Flow
Through the pygame module the player will use the keyboard to navigate the map which will update per movement pressed.
Periodically the code will update the values of the cryptocurrency by requesting it from an API.

## Non-Functional Requirements (301 & 401 only)

1. Testability: The game is graphical and ran mostly through a module so most of the testing will have to be done
manually to check for bugs. The backend functionality can have tests written for it through standard methods through
assertion.

2. Usability: The user needs to be able to download and install the game to run. If pygame itself doesn't have the
functionality to export the game as an executable, we will have to come up with an alternative that includes complete
instructions that are both concise and universal.