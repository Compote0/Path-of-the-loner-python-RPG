# Path of the Loner - Python RPG

🗡️ A Python RPG using Pygame ⚔️

---

## 📖 Introduction

**Path of the Loner** is a turn-based RPG developed in **Python** using the **Pygame** library. The player controls a lone warrior, engaging in battles against monsters, leveling up, earning coins, and interacting with a merchant to buy weapons and potions.

This game features:

- A **turn-based combat system** with strategic decisions.
- A **progression system** where players earn XP and level up and a saving system.
- A **merchant system** that appears every 5 encounters to buy useful items.
- Dynamic **enemy encounters**, each with unique stats, images, and backgrounds.

---

## 🚀 Installation

### 1. Prerequisites

Ensure you have Python **3.8 or later** installed:

```sh
python --version
```

Or:

```sh
python3 --version
```

### 2. Clone the Repository

```sh
git clone git@github.com:Compote0/Path-of-the-loner-python-RPG.git
cd path-of-the-loner
```

### 3. Install Dependencies

Before running the game, install the required dependencies:

```sh
pip install -r requirements.txt
```

Or:

```sh
pip3 install -r requirements.txt
```

---

## 🎮 How to Play

### 🏹 Game Modes

- **PvE (Player vs Environment)**: The player fights against randomly generated monsters.
- **PvP (Player vs Player - AI Controlled)**: The player fights against AI-controlled heroes.

### ⚔️ Combat System

- **Turn-based battles**: The player and the enemy take turns to attack.
- **Attacking**: Press `A` to attack during your turn.
- **Health System**: Both player and enemies have HP bars.
- **Status Effects**: Some enemies can inflict status conditions like _Frozen_ or _Stunned_.

### 🛒 Merchant System

- The **merchant appears every 5 battles**.
- The player can buy:
  - **Weapons** to increase attack power.
  - **Potions** to restore HP or temporarily boost stats.
- The player spends **coins** earned from battles to purchase these items.

### 🎚️ Leveling System

- Defeating enemies grants **XP**.
- If the player reaches the XP threshold, they **level up**.
- Leveling up increases:
  - **Maximum HP**
  - **Attack Power**
  - **Overall battle efficiency**
- A **level-up animation** is displayed when the player advances.

---

## 🖼️ Game Assets

The game uses multiple assets, categorized as follows:

- **Characters**: Stored in `assets/characters/`
- **Hero Backgrounds**: Stored in `assets/hero_backgrounds/`
- **Monster Backgrounds**: Stored in `assets/monsters_rooms/`
- **Monsters**: Stored in `assets/monsters/`
- **Merchant NPC**: Stored in `assets/PNJ/`

---

## 🛠️ Features Overview

- **Turn-based combat with AI-controlled opponents**.
- **Save game system in real time**
- **Procedural encounters with different enemy types**.
- **XP and Leveling system** to enhance player stats.
- **Merchant system every 5 fights to buy potions and weapons**.
- **Dynamic battle backgrounds based on the enemy encountered**.
- **Graphical UI using Pygame for health bars and visual effects**.
- **Pixel-art graphics to create an immersive RPG experience**.

---

## 🏗️ Project Structure

The project is structured as follows:

```
Path-of-the-Loner/
│── assets/                    # Game assets (characters, backgrounds, UI elements)
│── data/                      # JSON files storing enemy data, weapons, etc.
│── models/                    # python files handling classes
│── src/                       # Source code for game logic
│   │── character.py           # Character creation logic file
│   │── class_selection.py     # Character class selection logic
│   │── effects.py             # Special effects like status conditions
│   │── encounter.py           # Handles the encounter system
│   │── equipment_selection.py # Handles the weapons and armor selection
│   │── game_loop.py           # Handles the game loop system
│   │── menu.py                # Graphic menu
│   │── merchant.py            # Merchant system logic
│   │── pvp.py                 # Handles the pvp system
│   │── transition_screens.py  # UI for victory, defeat, and encounters
│   │── utility.py             # load json data from files
│── main.py                    # Main entry point of the game
│── README.md                  # Project documentation
│── requirements.txt           # Dependencies for Python environment
```

---

## 🎥 Demonstration

🎞️ _Screenshots or GIFs of the gameplay can be inserted here_.

---

## 🔧 How to Run the Game

To start playing, execute:

```sh
python main.py
```

Or, if Python 3 is required:

```sh
python3 main.py
```

---

## 🤝 Contributing

Contributions are welcome! If you wish to improve the game, please:

1. **Fork the repository**.
2. **Create a feature branch** (`git checkout -b feature-new`).
3. **Commit your changes** (`git commit -m "Added new feature"`).
4. **Push the branch** (`git push origin feature-new`).
5. **Create a Pull Request**.

For major changes, please open an issue first to discuss your ideas.

---

## 📬 Contact

For any inquiries, feedback, or issues, feel free to **open an issue** on GitHub or contact the project maintainer.

---

🎮 Happy Gaming! 🏆
