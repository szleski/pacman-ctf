# Repository Structure

This document describes the organization and structure of the pacman-ctf repository, a Python 3 implementation of UC Berkeley's CS 188 Pacman Capture the Flag project with pygame graphics.

## Overview

This is an educational AI project where students create intelligent agents to play Capture-the-Flag in a Pacman-like arena. The repository contains the game engine, graphics system, sample teams, and map layouts.

**Version:** v1.002  
**Python:** 3.x  
**Dependencies:** pygame >= 2.5.0

## Directory Structure

```
pacman-ctf/
├── layouts/              # Game map layouts (.lay files)
├── nonctf/              # Non-CTF game modes and utilities
├── origdoc/             # Original HTML documentation and assets
├── Core Game Files      # See below
└── Configuration Files  # See below
```

### Layouts Directory (`/layouts`)

Contains 12 pre-designed map layouts for Capture the Flag games:

- `defaultCapture.lay` - Standard balanced map
- `alleyCapture.lay` - Narrow corridor design
- `bloxCapture.lay` - Block-based obstacles
- `crowdedCapture.lay` - Dense obstacle layout
- `distantCapture.lay` - Long-distance map
- `fastCapture.lay` - Quick gameplay map
- `jumboCapture.lay` - Extra large map
- `mediumCapture.lay` - Medium-sized map
- `officeCapture.lay` - Office-themed layout
- `strategicCapture.lay` - Strategic chokepoints
- `testCapture.lay` - Testing/development map
- `tinyCapture.lay` - Small quick-play map

### Non-CTF Directory (`/nonctf`)

Contains files for non-Capture-the-Flag Pacman modes:

- `autograder.py` - Automated grading utilities
- `ghostAgents.py` - Ghost AI agents for classic Pacman
- `pacman.py` - Classic Pacman game runner
- `pacmanAgents.py` - Classic Pacman AI agents
- `testClasses.py` - Test framework classes
- `testParser.py` - Test configuration parser
- `unpack.py` - Utility for unpacking test files

### Original Documentation (`/origdoc`)

Contains original project documentation and visual assets:

- `contest.html` - Original contest rules and information
- `capture_the_flag.png` - Game screenshot example
- `capture_the_flag2.png` - Additional screenshot
- `bracket.png` - Tournament bracket visualization
- `contestLayout.png` - Layout visualization
- `projects.css` - Styling for HTML docs

## Core Python Modules

### Game Engine Core

#### `capture.py` (1,032 lines)
**Purpose:** Main game logic for Capture the Flag mode

**Key Components:**
- `GameState` class - Represents complete game state
- `CaptureRules` class - Implements CTF-specific rules
- Game constants (scoring, timing, vision range)
- Command-line interface for running games
- Agent loading and team management

**Key Functions:**
- `noisyDistance()` - Adds noise to distance observations
- Game state management and transitions
- Victory condition checking
- Move validation and processing

#### `game.py` (732 lines)
**Purpose:** Fundamental game data structures

**Key Classes:**
- `Agent` - Base class for all agents
- `Directions` - Movement direction constants
- `Grid` - 2D grid representation
- `Configuration` - Position and direction of an agent
- `AgentState` - Full state of a single agent
- `Game` - Core game loop and execution

#### `layout.py` (149 lines)
**Purpose:** Map layout loading and processing

**Key Functions:**
- `getLayout()` - Load layout from file or generate random
- `Layout` class - Parses and stores map structure
- Wall, food, and capsule placement
- Starting position determination

### Agent Framework

#### `captureAgents.py` (304 lines)
**Purpose:** Base classes for creating CTF agents

**Key Classes:**
- `CaptureAgent` - Base class for all CTF agents
  - Provides convenience methods for team-based gameplay
  - Handles observation history
  - Manages distance calculator
  - Provides food, capsule, and opponent tracking
  
**Key Methods:**
- `registerInitialState()` - Initialize agent
- `chooseAction()` - Main decision-making method (to be overridden)
- `getFood()`, `getCapsules()` - Get food/capsule locations
- `getOpponents()`, `getTeam()` - Team management
- `getMazeDistance()` - Calculate maze distances

#### `baselineTeam.py` (187 lines)
**Purpose:** Example implementation of a functional CTF team

**Agents:**
- `OffensiveReflexAgent` - Aggressive food-gathering agent
- `DefensiveReflexAgent` - Defensive patrolling agent
- `ReflexCaptureAgent` - Base reflex agent with evaluation function

**Usage:** Template for creating custom teams

#### `myTeam.py` (92 lines)
**Purpose:** Starter template for student teams

**Contents:**
- `createTeam()` function - Required team creation interface
- `DummyAgent` - Minimal example agent
- Skeleton code for students to implement their own agents

### Graphics and Display

#### `graphicsUtils.py` (605 lines)
**Purpose:** Low-level pygame graphics primitives

**Implementation:** Complete pygame-based rendering system (migrated from tkinter in 2025)

**Key Functions:**
- `formatColor()` - Color format conversion
- `polygon()`, `circle()`, `line()` - Shape drawing
- `text()` - Text rendering with font mapping
- `refresh()`, `sleep()` - Display update and timing
- Object tracking system for updates

#### `captureGraphicsDisplay.py` (740 lines)
**Purpose:** High-level CTF game visualization

**Key Classes:**
- `PacmanGraphics` - Main graphics controller
- `InfoPane` - Score and information display
- `AgentView` - Individual agent visualization

**Features:**
- Team colors (red/blue)
- Score display
- Agent position and direction rendering
- Food and capsule visualization
- Game state animation

#### `graphicsDisplay.py` (679 lines)
**Purpose:** Classic Pacman graphics (non-CTF mode)

Similar structure to `captureGraphicsDisplay.py` but for original Pacman gameplay.

#### `textDisplay.py` (81 lines)
**Purpose:** Text-only game display

Provides ASCII-art visualization for headless/terminal environments.

### Utilities

#### `util.py` (652 lines)
**Purpose:** Common data structures and algorithms

**Key Classes:**
- `Counter` - Dictionary with default value 0
- `PriorityQueue` - Heap-based priority queue
- `PriorityQueueWithFunction` - Priority queue with custom comparator
- `Queue` - FIFO queue
- `Stack` - LIFO stack

**Key Functions:**
- `manhattanDistance()` - Manhattan distance calculation
- `raiseNotDefined()` - Stub function marker
- `flipCoin()` - Random binary choice
- `normalize()` - Normalize probability distributions

#### `distanceCalculator.py` (157 lines)
**Purpose:** Efficient maze distance calculations

**Key Class:**
- `Distancer` - Pre-computes and caches maze distances using BFS

**Usage:** Automatically initialized for agents via `self.distancer`

#### `keyboardAgents.py` (84 lines)
**Purpose:** Human player keyboard control

**Key Classes:**
- `KeyboardAgent` - Keyboard controls for single agent
- `KeyboardAgent2` - Alternative control scheme

**Controls:**
- Player 1: W/A/S/D
- Player 2: P/L/;/,

### Map Generation

#### `mazeGenerator.py` (271 lines)
**Purpose:** Procedural maze generation

**Usage:** Generate random symmetric mazes for CTF games

**Features:**
- Random layout generation
- Symmetry enforcement for fair team gameplay
- Food and capsule placement

#### `generateTournamentLayouts.py` (46 lines)
**Purpose:** Batch generate tournament maps

Utility script for creating multiple random tournament-ready layouts.

### Utilities and Tools

#### `capture_screenshot.py` (81 lines)
**Purpose:** Take screenshots of games

Utility to capture game visuals for documentation or analysis.

## Configuration Files

### `requirements.txt`
```
pygame>=2.5.0
```

Single dependency: pygame for graphics rendering.

### `VERSION`
```
v1.002
```

Current version identifier.

### `.gitignore`
Excludes:
- Python bytecode (`__pycache__/`, `*.pyc`)
- Build artifacts (`build/`, `dist/`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)

## Documentation Files

### `README.md`
Main repository documentation covering:
- Installation instructions
- Quick start guide
- Game rules and mechanics
- Key data structures
- Team creation guide

### `PYGAME_MIGRATION.md`
Documents the 2025 migration from Tcl/Tk to pygame:
- Migration rationale (Windows 11 compatibility)
- Technical changes
- Platform support
- Performance considerations
- Troubleshooting guide

### `STRUCTURE.md` (This File)
Comprehensive repository structure documentation.

## Game Architecture

### Execution Flow

1. **Initialization**
   - Parse command-line arguments (`capture.py`)
   - Load layout from file or generate random
   - Initialize teams using `createTeam()` functions
   - Set up graphics display or text mode

2. **Game Loop**
   - For each agent in turn order:
     - Get legal actions
     - Call agent's `chooseAction()` method
     - Apply action and update game state
     - Check victory conditions
     - Update display

3. **Termination**
   - Game ends when:
     - One team eats all but 2 opponent food dots
     - 1200 moves completed (300 per agent)
     - Time limit reached
   - Display final score and statistics

### Agent Decision Making

Agents implement the following interface:

```python
def registerInitialState(self, gameState):
    """Setup phase - 15 second time limit"""
    
def chooseAction(self, gameState):
    """Return action - 1 second time limit per move"""
    return action
```

### State Representation

- **Position:** (x, y) integer coordinates
- **Direction:** North, South, East, West, Stop
- **Team State:** Score, food remaining, agent positions
- **Observations:** Visible opponents, noisy distances to all

## Creating Custom Teams

### Basic Template

```python
from captureAgents import CaptureAgent

def createTeam(firstIndex, secondIndex, isRed,
               first='MyAgent1', second='MyAgent2'):
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

class MyAgent1(CaptureAgent):
    def chooseAction(self, gameState):
        # Implement your strategy
        return action
```

### Key Methods Available

- `self.getFood(gameState)` - Get food locations
- `self.getCapsules(gameState)` - Get capsule locations
- `self.getOpponents(gameState)` - Get opponent agent indices
- `self.getMazeDistance(pos1, pos2)` - Get maze distance
- `gameState.getAgentState(index)` - Get agent state
- `gameState.getLegalActions(index)` - Get legal moves

## Running Games

### Basic Commands

```bash
# Default game (baseline vs baseline)
python capture.py

# Test your team as Red
python capture.py --red=myTeam

# Play with keyboard controls
python capture.py --keys0

# Specific layout
python capture.py -l mediumCapture

# Random layout
python capture.py -l RANDOM

# Text-only mode
python capture.py -t

# Multiple games
python capture.py -n 10 -q
```

### Command-Line Options

- `-r/--red` - Red team module
- `-b/--blue` - Blue team module
- `-l/--layout` - Map layout file
- `--keys0-3` - Enable keyboard control for agent
- `-t/--textgraphics` - Text-only display
- `-q/--quiet` - Minimal output
- `-n/--numGames` - Number of games to play
- `-z/--zoom` - Graphics zoom level
- `-f/--fixRandomSeed` - Fixed random seed

## Development Guidelines

### Time Limits
- **Initial Setup:** 15 seconds (`registerInitialState`)
- **Per Move:** 1 second (`chooseAction`)
- **Warning:** After 3 warnings or single 3+ second move
- **Forfeit:** Game ends on timeout

### Observations
- **Vision Range:** 5 Manhattan distance
- **Noisy Distances:** All agents (± random noise)
- **Perfect Knowledge:** Own team positions

### Testing Strategy
1. Test against baseline teams
2. Use text mode for fast iteration (`-t`)
3. Run multiple games for statistics (`-n 10`)
4. Test on different layouts
5. Verify time constraints are met

## Recent Changes (v1.002)

### Pygame Migration (2025)
- Replaced Tcl/Tk with pygame for graphics
- Improved Windows 11 compatibility
- Better performance and modern platform support
- Maintained full API compatibility

### Bug Fixes
- Fixed importlib.util import in capture.py

## License

This project is free for educational use with attribution to UC Berkeley. See README.md for full licensing details.

Original development: UC Berkeley (John DeNero, Dan Klein)  
Python 3 port: Christian Shelton (2020)  
Pygame migration: 2025

## Additional Resources

- **Original Documentation:** See `/origdoc/contest.html`
- **Example Screenshot:** `game_screenshot.png`
- **Baseline Team Code:** `baselineTeam.py` - Study this for strategy examples
- **Migration Notes:** `PYGAME_MIGRATION.md` - Technical details of pygame port
