# Pygame Migration Documentation

## Overview
This project has been successfully migrated from Tcl/Tk (tkinter) to pygame for better compatibility with Windows 11 in corporate environments.

## Changes Made

### 1. Graphics System Replacement
- **graphicsUtils.py**: Completely rewritten to use pygame instead of tkinter
  - All drawing functions (polygon, circle, line, text, etc.) now use pygame primitives
  - Maintained the same API to ensure compatibility with existing code
  - Implemented object tracking system to support editing and moving drawn objects
  - Event handling updated to use pygame event system

### 2. Dependencies
- **requirements.txt**: Created with pygame>=2.5.0 dependency

### 3. Bug Fixes
- **capture.py**: Fixed importlib.util import issue (line 61)

## Installation

### Prerequisites
- Python 3.x
- pip

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Or install pygame directly
pip install pygame
```

## Running the Game

The game can be run the same way as before:

```bash
# Start a game with default settings
python capture.py

# Start with keyboard controls for player 0
python capture.py --keys0

# Start with custom teams
python capture.py -r baselineTeam -b myTeam

# Run in text mode (no graphics)
python capture.py -t

# See all options
python capture.py --help
```

## Compatibility

### What Works
- All game modes (CTF, standard, etc.)
- Keyboard controls
- Team AI agents
- Text-only mode
- All command-line options

### Platform Support
- ✅ Linux
- ✅ macOS
- ✅ Windows 10/11 (including corporate environments)

### Key Improvements for Windows 11
1. **No Tcl/Tk Dependencies**: Eliminates issues with Tcl/Tk installations in restricted corporate environments
2. **Better Performance**: pygame provides more efficient rendering
3. **Modern Graphics**: pygame is actively maintained and supports modern display systems
4. **Easier Installation**: Single `pip install pygame` command

## Technical Details

### Architecture
The pygame implementation maintains full API compatibility with the original tkinter version:
- All function signatures remain the same
- Object IDs are still used for tracking and updating drawn elements
- Color format conversion is handled automatically

### Key Differences
1. **Rendering**: Uses pygame's surface-based rendering instead of tkinter canvas
2. **Event Loop**: pygame event pump integrated into sleep() and refresh() functions
3. **Object Storage**: Objects stored in dictionary for redrawing on updates (pygame doesn't have native object tracking like tkinter canvas)

### Performance Considerations
- The implementation redraws all objects when one is updated (necessary due to pygame's immediate-mode rendering)
- For typical Pacman games, this has negligible performance impact
- Frame rate is controlled by the clock system for smooth animation

## Troubleshooting

### Display Issues
If you encounter display issues on headless systems or in certain environments:
```bash
# Use text mode
python capture.py -t

# Or quiet mode
python capture.py -q
```

### pygame Import Errors
```bash
# Make sure pygame is installed
pip install --upgrade pygame

# On some systems, you may need
pip3 install --upgrade pygame
```

### Font Issues
If text doesn't display correctly, pygame will fall back to default fonts. The system maps common fonts:
- Helvetica → Arial
- Times → Times New Roman
- Consolas → Consolas
- Courier → Courier

## Development

### Running Tests
```bash
# Test in text mode
python capture.py -t -n 1

# Test with specific layout
python capture.py -l RANDOM

# Test with multiple games
python capture.py -n 10 -q
```

### Creating Custom Teams
The migration doesn't affect team development. Continue creating teams in Python files with the `createTeam` function as before.

## Rollback
If you need to rollback to tkinter for any reason, the original tkinter version can be restored from git history:
```bash
git checkout <previous-commit> graphicsUtils.py
```

However, note that the tkinter version may have compatibility issues on Windows 11 in corporate settings.

## Credits
- Original Pacman AI projects: UC Berkeley (John DeNero, Dan Klein, Brad Miller, Nick Hay, Pieter Abbeel)
- Python 3 port: Christian Shelton
- Pygame migration: 2025

## License
Same as original project - free for educational use with attribution to UC Berkeley.
