#!/usr/bin/env python3
"""
Screenshot utility for Pacman CTF game
Captures a screenshot of the game in action for documentation purposes
"""

import sys
import pygame
from capture import readCommand, runGames

# Global state for screenshot capture
original_update = None
screenshot_taken = False
frame_count = 0
target_frame = 100  # Capture after this many frames


def patched_update(self, newState):
    """Patched update method that captures a screenshot at the right moment"""
    global screenshot_taken, frame_count, original_update

    # Call original update to render the game
    original_update(self, newState)
    frame_count += 1

    # Capture screenshot after enough frames for agents to be active
    if not screenshot_taken and frame_count >= target_frame:
        try:
            import graphicsUtils
            if graphicsUtils._screen is not None:
                output_file = 'game_screenshot.png'
                pygame.image.save(graphicsUtils._screen, output_file)
                print(f"\n✓ Screenshot saved to {output_file} (frame {frame_count})")
                screenshot_taken = True
        except Exception as e:
            print(f"Error capturing screenshot: {e}")


def capture_screenshot(output_file='game_screenshot.png', zoom=1.5, frames=100):
    """
    Capture a screenshot of the game

    Args:
        output_file: Output filename for the screenshot
        zoom: Zoom level for the game display
        frames: Number of frames to wait before capturing
    """
    global target_frame, original_update
    target_frame = frames

    # Parse command line options for the game
    options = readCommand([f'--zoom={zoom}', '-i', '1000'])

    # Patch the display update method to capture screenshots
    import captureGraphicsDisplay
    original_update = captureGraphicsDisplay.PacmanGraphics.update
    captureGraphicsDisplay.PacmanGraphics.update = patched_update

    print(f"Starting game to capture screenshot after {frames} frames...")
    print("Teams: Red vs Blue (baseline agents)")

    # Run the game
    games = runGames(**options)

    print("Screenshot capture complete!")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Capture a screenshot of Pacman CTF')
    parser.add_argument('-o', '--output', default='game_screenshot.png',
                        help='Output filename (default: game_screenshot.png)')
    parser.add_argument('-z', '--zoom', type=float, default=1.5,
                        help='Zoom level (default: 1.5)')
    parser.add_argument('-f', '--frames', type=int, default=100,
                        help='Number of frames before capture (default: 100)')

    args = parser.parse_args()

    capture_screenshot(args.output, args.zoom, args.frames)
