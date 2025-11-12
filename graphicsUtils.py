# graphicsUtils.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# Modified to use pygame instead of Tkinter for better Windows 11 compatibility


import sys
import math
import random
import time
import pygame

_Windows = sys.platform == 'win32'  # True if on Win95/98/NT

_screen = None      # The pygame display surface
_canvas_xs = None      # Size of canvas object
_canvas_ys = None
_canvas_x = None      # Current position on canvas
_canvas_y = None
_canvas_col = None      # Current colour (set to black below)
_canvas_tsize = 12
_canvas_tserifs = 0
_bg_color = None
_clock = None

# Storage for drawn objects (each item is a dict with type and properties)
_drawn_objects = {}
_next_object_id = 0

def formatColor(r, g, b):
    """Convert RGB values (0-1) to pygame Color object"""
    return pygame.Color(int(r * 255), int(g * 255), int(b * 255))

def colorToVector(color):
    """Convert pygame Color to normalized RGB list"""
    if isinstance(color, pygame.Color):
        return [color.r / 255.0, color.g / 255.0, color.b / 255.0]
    # Handle hex string format from old code
    if isinstance(color, str) and color.startswith('#'):
        return list(map(lambda x: int(x, 16) / 256.0, [color[1:3], color[3:5], color[5:7]]))
    return color

if _Windows:
    _canvas_tfonts = ['timesnewroman', 'lucidaconsole']
else:
    _canvas_tfonts = ['times', 'lucidasans-24']

def sleep(secs):
    global _screen, _clock
    if _screen is None:
        time.sleep(secs)
    else:
        pygame.display.flip()
        _clock.tick(int(1.0 / secs) if secs > 0 else 60)
        pygame.event.pump()

def begin_graphics(width=640, height=480, color=formatColor(0, 0, 0), title=None):
    global _screen, _canvas_x, _canvas_y, _canvas_xs, _canvas_ys, _bg_color, _clock
    global _drawn_objects, _next_object_id

    # Initialize pygame
    pygame.init()

    # Save the canvas size parameters
    _canvas_xs, _canvas_ys = width - 1, height - 1
    _canvas_x, _canvas_y = 0, _canvas_ys
    _bg_color = color

    # Create the display window
    _screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title or 'Graphics Window')

    _clock = pygame.time.Clock()
    _drawn_objects = {}
    _next_object_id = 0

    draw_background()
    pygame.display.flip()

_leftclick_loc = None
_rightclick_loc = None
_ctrl_leftclick_loc = None

def _handle_events():
    """Process pygame events and update click locations"""
    global _leftclick_loc, _rightclick_loc, _ctrl_leftclick_loc

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    _ctrl_leftclick_loc = event.pos
                else:
                    _leftclick_loc = event.pos
            elif event.button == 3:  # Right click
                _rightclick_loc = event.pos

def wait_for_click():
    """Wait for a mouse click and return the location and button"""
    global _leftclick_loc, _rightclick_loc, _ctrl_leftclick_loc

    while True:
        _handle_events()

        if _leftclick_loc is not None:
            val = _leftclick_loc
            _leftclick_loc = None
            return val, 'left'
        if _rightclick_loc is not None:
            val = _rightclick_loc
            _rightclick_loc = None
            return val, 'right'
        if _ctrl_leftclick_loc is not None:
            val = _ctrl_leftclick_loc
            _ctrl_leftclick_loc = None
            return val, 'ctrl_left'
        sleep(0.05)

def draw_background():
    """Fill the screen with background color"""
    global _screen, _bg_color
    if _screen:
        _screen.fill(_bg_color)

def end_graphics():
    """Clean up and close the graphics window"""
    global _screen, _clock
    try:
        sleep(1)
        pygame.quit()
    except SystemExit as e:
        print('Ending graphics raised an exception:', e)
    finally:
        _screen = None
        _clock = None
        _clear_keys()

def clear_screen(background=None):
    """Clear the screen and redraw background"""
    global _canvas_x, _canvas_y, _drawn_objects, _next_object_id
    _drawn_objects = {}
    _next_object_id = 0
    draw_background()
    _canvas_x, _canvas_y = 0, _canvas_ys
    pygame.display.flip()

def polygon(coords, outlineColor, fillColor=None, filled=1, smoothed=1, behind=0, width=1):
    """Draw a polygon on the screen"""
    global _screen, _next_object_id, _drawn_objects

    if fillColor is None:
        fillColor = outlineColor
    if filled == 0:
        fillColor = None

    obj_id = _next_object_id
    _next_object_id += 1

    _drawn_objects[obj_id] = {
        'type': 'polygon',
        'coords': list(coords),
        'outline': outlineColor,
        'fill': fillColor,
        'filled': filled,
        'width': width,
        'behind': behind
    }

    _draw_object(obj_id)
    return obj_id

def _draw_object(obj_id):
    """Draw a single object from the drawn_objects dict"""
    global _screen, _drawn_objects

    if obj_id not in _drawn_objects or _screen is None:
        return

    obj = _drawn_objects[obj_id]

    if obj['type'] == 'polygon':
        if obj['filled'] and obj['fill'] is not None:
            pygame.draw.polygon(_screen, obj['fill'], obj['coords'])
        if obj['width'] > 0 and obj['outline'] is not None:
            pygame.draw.polygon(_screen, obj['outline'], obj['coords'], obj['width'])

    elif obj['type'] == 'circle':
        pos = (int(obj['x']), int(obj['y']))
        r = int(obj['r'])
        if obj['fill'] is not None:
            pygame.draw.circle(_screen, obj['fill'], pos, r)
        if obj['width'] > 0 and obj['outline'] is not None:
            pygame.draw.circle(_screen, obj['outline'], pos, r, obj['width'])

        # Handle arc drawing for endpoints
        if obj.get('endpoints') is not None:
            start_angle = math.radians(obj['endpoints'][0])
            end_angle = math.radians(obj['endpoints'][1])
            rect = pygame.Rect(pos[0] - r, pos[1] - r, 2*r, 2*r)
            pygame.draw.arc(_screen, obj['outline'], rect, start_angle, end_angle, obj['width'])

    elif obj['type'] == 'line':
        pygame.draw.line(_screen, obj['color'], obj['start'], obj['end'], obj['width'])

    elif obj['type'] == 'text':
        font = pygame.font.SysFont(obj['font'], obj['size'])
        if obj['style'] == 'bold':
            font.set_bold(True)
        text_surface = font.render(obj['text'], True, obj['color'])

        # Handle anchor positions
        rect = text_surface.get_rect()
        if obj['anchor'] == 'nw':
            rect.topleft = obj['pos']
        elif obj['anchor'] == 'center':
            rect.center = obj['pos']
        else:
            rect.topleft = obj['pos']

        _screen.blit(text_surface, rect)

def square(pos, r, color, filled=1, behind=0):
    """Draw a square"""
    x, y = pos
    coords = [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)]
    return polygon(coords, color, color, filled, 0, behind=behind)

def circle(pos, r, outlineColor, fillColor, endpoints=None, style='pieslice', width=2):
    """Draw a circle or arc"""
    global _screen, _next_object_id, _drawn_objects

    x, y = pos

    obj_id = _next_object_id
    _next_object_id += 1

    _drawn_objects[obj_id] = {
        'type': 'circle',
        'x': x,
        'y': y,
        'r': r,
        'outline': outlineColor,
        'fill': fillColor,
        'endpoints': endpoints,
        'style': style,
        'width': width
    }

    _draw_object(obj_id)
    return obj_id

def image(pos, file="../../blueghost.gif"):
    """Load and draw an image (not implemented for pygame)"""
    # Note: Image loading would need to be implemented if used
    return None

def refresh():
    """Update the display"""
    global _screen
    if _screen:
        pygame.display.flip()
        _handle_events()

def moveCircle(id, pos, r, endpoints=None):
    """Move and update a circle"""
    global _drawn_objects

    if id in _drawn_objects and _drawn_objects[id]['type'] == 'circle':
        x, y = pos
        _drawn_objects[id]['x'] = x
        _drawn_objects[id]['y'] = y
        _drawn_objects[id]['r'] = r
        if endpoints is not None:
            _drawn_objects[id]['endpoints'] = endpoints
        _redraw_all()

def edit(id, *args):
    """Edit properties of a drawn object"""
    global _drawn_objects

    if id not in _drawn_objects:
        return

    updates = dict(args)
    obj = _drawn_objects[id]

    if 'fill' in updates:
        obj['fill'] = updates['fill']
    if 'outline' in updates:
        obj['outline'] = updates['outline']
    if 'start' in updates:
        obj['start_angle'] = updates['start']
    if 'extent' in updates:
        obj['extent'] = updates['extent']

    _redraw_all()

def text(pos, color, contents, font='Helvetica', size=12, style='normal', anchor="nw"):
    """Draw text on the screen"""
    global _screen, _next_object_id, _drawn_objects

    x, y = pos

    # Map font names
    font_map = {
        'Helvetica': 'arial',
        'Times': 'timesnewroman',
        'Consolas': 'consolas',
        'Courier': 'courier'
    }
    font_name = font_map.get(font, font.lower().replace(' ', ''))

    obj_id = _next_object_id
    _next_object_id += 1

    _drawn_objects[obj_id] = {
        'type': 'text',
        'pos': (x, y),
        'color': color,
        'text': contents,
        'font': font_name,
        'size': size,
        'style': style,
        'anchor': anchor
    }

    _draw_object(obj_id)
    return obj_id

def changeText(id, newText, font=None, size=12, style='normal'):
    """Update the text of a text object"""
    global _drawn_objects

    if id in _drawn_objects and _drawn_objects[id]['type'] == 'text':
        _drawn_objects[id]['text'] = newText
        if font is not None:
            _drawn_objects[id]['font'] = font
            _drawn_objects[id]['size'] = size
            _drawn_objects[id]['style'] = style
        _redraw_all()

def changeColor(id, newColor):
    """Change the color of an object"""
    global _drawn_objects

    if id in _drawn_objects:
        if _drawn_objects[id]['type'] == 'text':
            _drawn_objects[id]['color'] = newColor
        else:
            _drawn_objects[id]['fill'] = newColor
        _redraw_all()

def line(here, there, color=formatColor(0, 0, 0), width=2):
    """Draw a line"""
    global _screen, _next_object_id, _drawn_objects

    x0, y0 = here[0], here[1]
    x1, y1 = there[0], there[1]

    obj_id = _next_object_id
    _next_object_id += 1

    _drawn_objects[obj_id] = {
        'type': 'line',
        'start': (x0, y0),
        'end': (x1, y1),
        'color': color,
        'width': width
    }

    _draw_object(obj_id)
    return obj_id

def _redraw_all():
    """Redraw all objects in the correct order"""
    global _drawn_objects, _screen

    if _screen is None:
        return

    draw_background()

    # Sort by behind value (higher = more behind = draw first)
    sorted_objects = sorted(_drawn_objects.items(),
                          key=lambda x: x[1].get('behind', 0),
                          reverse=True)

    for obj_id, obj in sorted_objects:
        _draw_object(obj_id)

##############################################################################
### Keypress handling ########################################################
##############################################################################

_keysdown = {}
_keyswaiting = {}
_got_release = None

def _clear_keys(event=None):
    global _keysdown, _got_release, _keyswaiting
    _keysdown = {}
    _keyswaiting = {}
    _got_release = None

def keys_pressed():
    """Return list of currently pressed keys"""
    global _keysdown, _got_release

    _handle_events()

    # Update key states from pygame
    pressed = pygame.key.get_pressed()
    _keysdown = {}

    # Map pygame keys to string names
    key_map = {
        pygame.K_a: 'a', pygame.K_s: 's', pygame.K_d: 'd', pygame.K_w: 'w',
        pygame.K_LEFT: 'Left', pygame.K_RIGHT: 'Right',
        pygame.K_UP: 'Up', pygame.K_DOWN: 'Down',
        pygame.K_q: 'q', pygame.K_ESCAPE: 'Escape',
        pygame.K_l: 'l', pygame.K_SEMICOLON: 'semicolon',
        pygame.K_COMMA: 'comma', pygame.K_p: 'p'
    }

    for key, name in key_map.items():
        if pressed[key]:
            _keysdown[name] = 1

    return list(_keysdown.keys())

def keys_waiting():
    """Return list of keys that were pressed since last check"""
    global _keyswaiting

    # Process events to update waiting keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            key_map = {
                pygame.K_a: 'a', pygame.K_s: 's', pygame.K_d: 'd', pygame.K_w: 'w',
                pygame.K_LEFT: 'Left', pygame.K_RIGHT: 'Right',
                pygame.K_UP: 'Up', pygame.K_DOWN: 'Down',
                pygame.K_q: 'q', pygame.K_ESCAPE: 'Escape',
                pygame.K_l: 'l', pygame.K_SEMICOLON: 'semicolon',
                pygame.K_COMMA: 'comma', pygame.K_p: 'p'
            }
            if event.key in key_map:
                _keyswaiting[key_map[event.key]] = 1

    keys = list(_keyswaiting.keys())
    _keyswaiting = {}
    return keys

def wait_for_keys():
    """Block until a key is pressed"""
    keys = []
    while keys == []:
        keys = keys_pressed()
        sleep(0.05)
    return keys

def remove_from_screen(x):
    """Remove an object from the screen"""
    global _drawn_objects

    if x in _drawn_objects:
        del _drawn_objects[x]
        _redraw_all()

def move_to(object, x, y=None):
    """Move an object to a new position"""
    global _drawn_objects

    if y is None:
        try:
            x, y = x
        except:
            raise Exception('incomprehensible coordinates')

    if object not in _drawn_objects:
        return

    obj = _drawn_objects[object]

    if obj['type'] == 'polygon':
        if len(obj['coords']) > 0:
            current_x, current_y = obj['coords'][0]
            dx = x - current_x
            dy = y - current_y
            obj['coords'] = [(px + dx, py + dy) for px, py in obj['coords']]
    elif obj['type'] == 'circle':
        obj['x'] = x
        obj['y'] = y
    elif obj['type'] == 'text':
        obj['pos'] = (x, y)

    _redraw_all()

def move_by(object, x, y=None, lift=False):
    """Move an object by a relative amount"""
    global _drawn_objects

    if y is None:
        try:
            x, y = x
        except:
            raise Exception('incomprehensible coordinates')

    if object not in _drawn_objects:
        return

    obj = _drawn_objects[object]

    if obj['type'] == 'polygon':
        obj['coords'] = [(px + x, py + y) for px, py in obj['coords']]
    elif obj['type'] == 'circle':
        obj['x'] += x
        obj['y'] += y
    elif obj['type'] == 'text':
        obj['pos'] = (obj['pos'][0] + x, obj['pos'][1] + y)
    elif obj['type'] == 'line':
        obj['start'] = (obj['start'][0] + x, obj['start'][1] + y)
        obj['end'] = (obj['end'][0] + x, obj['end'][1] + y)

    _redraw_all()

def writePostscript(filename):
    """Save the current canvas to a postscript file (not implemented)"""
    # This would need to be implemented differently for pygame
    print(f"Warning: writePostscript not fully implemented for pygame")

# Ghost shape for testing
ghost_shape = [
    (0, - 0.5),
    (0.25, - 0.75),
    (0.5, - 0.5),
    (0.75, - 0.75),
    (0.75, 0.5),
    (0.5, 0.75),
    (- 0.5, 0.75),
    (- 0.75, 0.5),
    (- 0.75, - 0.75),
    (- 0.5, - 0.5),
    (- 0.25, - 0.75)
]

if __name__ == '__main__':
    begin_graphics()
    clear_screen()
    ghost_shape = [(x * 10 + 20, y * 10 + 20) for x, y in ghost_shape]
    g = polygon(ghost_shape, formatColor(1, 1, 1))
    move_to(g, (50, 50))
    circle((150, 150), 20, formatColor(0.7, 0.3, 0.0), formatColor(0.7, 0.3, 0.0), endpoints=[15, - 15])
    refresh()
    sleep(2)
