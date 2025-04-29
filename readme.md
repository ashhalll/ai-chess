# Advanced Chess Variant with AI 🎮
> A sophisticated chess implementation featuring special pawn movement rules and an intelligent AI opponent using Minimax with Alpha-Beta pruning.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.0-blue.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![python-chess](https://img.shields.io/badge/python--chess-1.9.4-green.svg)](https://python-chess.readthedocs.io/)

<p align="center">
  <img src="assets/gameplay.gif" alt="Chess Variant Gameplay" width="600"/>
</p>

## 📑 Table of Contents
- [Features](#-features)
- [Special Rules](#-special-rules)
- [AI Implementation](#-ai-implementation)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Team](#-team)
- [Performance](#-performance)

## ✨ Features
- **Modern GUI**: Clean, dark-themed interface using CustomTkinter
- **Special Pawn Movement**: Unique variant rules for enhanced gameplay
- **Advanced AI**: Sophisticated opponent using Minimax with Alpha-Beta pruning
- **Real-time Analysis**: Move validation and game state tracking
- **Comprehensive History**: Complete move tracking and game analysis

## 🎲 Special Rules
- Pawns can make double moves from any rank
- One-time use per pawn for special moves
- Traditional chess rules apply otherwise

## 🤖 AI Implementation
### Core Algorithm
- Minimax with Alpha-Beta pruning (depth 3)
- Transposition table optimization
- Advanced position evaluation

### Evaluation Metrics
- Material value
- Piece positioning (piece-square tables)
- Pawn structure analysis
- King safety evaluation
- Center control
- Mobility assessment

## 📥 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/chess-variant.git
cd chess-variant

# Create virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS

# Install dependencies
pip install -r requirements.txt
```

## 🎮 Usage
```bash
# Run the game
python src/chess_gui.py
```

### Controls
- Click to select piece
- Click destination square to move
- Game status displayed in info panel
- Move history tracked in right panel

## 📁 Project Structure
```
chess-variant/
├── src/
│   ├── ai.py           # AI engine implementation
│   ├── game.py         # Core game logic and rules
│   ├── main.py         # Game management
│   └── chess_gui.py    # GUI implementation
├── tests/
│   ├── test_ai.py
│   ├── test_game.py
│   └── test_main.py
├── assets/
│   └── gameplay.gif
├── requirements.txt
├── README.md
└── LICENSE
```

## 👥 Team
- **Ashhal** - Project Lead & GUI Development
  - Implemented modern user interface
  - Coordinated project development
  - Documentation management

- **Omer** - AI Algorithm Specialist
  - Developed Minimax implementation
  - Created evaluation functions
  - Optimized AI performance

- **Hassan** - Game Logic Developer
  - Implemented core chess rules
  - Created variant rule system
  - Testing and optimization

## 📊 Performance
- Average move calculation: ~2 seconds
- Evaluation depth: 3 moves ahead
- Memory optimization through transposition tables
- Sophisticated position evaluation

## 🛠️ Tech Stack
- **Python 3.9+**
- **Libraries**:
  - `python-chess`: Core chess logic
  - `customtkinter`: Modern GUI framework
  - `typing`: Type annotations

## 📝 Requirements
```txt
python-chess==1.9.4
customtkinter==5.2.0
pillow==9.5.0
```

## 🤝 Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by Team Chess Variant
</p>