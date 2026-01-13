==========================================
        SIMPLE POKÉMON BATTLE GAME
==========================================

A turn-based Pokémon-style battle game built using Python and Pygame.
Inspired by classic Pokémon battles with animations, sound effects,
and clean modular code structure.

------------------------------------------
AUTHOR DETAILS
------------------------------------------
Name    : Aditya Bhardwaj
Section : D2
Roll No : 08
Course  : B.Tech
Branch  : Computer Science & Engineering

------------------------------------------
PROJECT OVERVIEW
------------------------------------------
This project simulates a 1v1 Pokémon battle between Charmander
and Squirtle. The game includes turn-based mechanics, animated
text, HP bars, sound effects, and win/lose screens.

The code is modularized across multiple files to improve
readability, maintainability, and scalability.

------------------------------------------
FEATURES
------------------------------------------
- Turn-based Pokémon battle system
- Animated dialogue (typewriter effect)
- HP bar animation with color change
- Move selection menu
- Pokémon cries & attack sounds
- Screen vibration on damage
- Background music
- Win / Lose screen
- Restart battle using ENTER key

------------------------------------------
CONTROLS
------------------------------------------
Arrow Keys : Navigate menus
ENTER      : Select / Continue
ESC        : Quit game

------------------------------------------
PROJECT STRUCTURE
------------------------------------------
battle/
│
├── main.py
├── config.py
├── colors.py
├── paths.py
├── ui_constants.py
├── battle_constants.py
├── Pokemon_Data.py
│
├── Pokemon/
│   ├── 4.png
│   └── 7.png
│
├── Sound/
│   ├── theme.mp3
│   ├── blip.wav
│   ├── BattleWInSound.mp3
│   ├── Charmander.ogg
│   ├── Squirtle.ogg
│   └── Attacks/
│       ├── Scratch.mp3
│       ├── Growl.mp3
│       └── Tackle.mp3
│
├── New folder/
│   ├── WON.jpg
│   └── Lost.jpg
│
└── Demo/
    ├── Battle.JPG
    └── Demo.gif

------------------------------------------
REQUIREMENTS
------------------------------------------
Python 3.10+
Pygame

Install dependency:
pip install pygame

------------------------------------------
HOW TO RUN
------------------------------------------
1. Open terminal in project folder
2. Run the game using:

   python main.py

------------------------------------------
GAME DEMO
------------------------------------------

Gameplay Demo (GIF):
------------------------------------------
![Gameplay Demo](Demo/Demo.gif)

Battle Screenshot:
------------------------------------------
![Battle Screen](Demo/Battle.JPG)

------------------------------------------
CONCEPTS USED
------------------------------------------
- Game loop & event handling
- Modular programming
- State management
- Animation handling
- Sound integration
- UI design for games

------------------------------------------
FUTURE IMPROVEMENTS
------------------------------------------
- Add more Pokémon
- Type-based damage system
- Items (Potions, Revives)
- Pokémon switching
- Difficulty levels
- Start & pause menu

------------------------------------------
CONCLUSION
------------------------------------------
This project demonstrates the fundamentals of game development
using Python and Pygame. It combines logic, visuals, and audio
to deliver a complete mini-game experience.

==========================================
