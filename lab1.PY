#task-1
'''
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

rain = []
dir_shift = 0
tilt = 0
bg_col = (0, 0, 0, 0)
house_col = (1.0, 1.0, 1.0)

def draw_pt(x, y):
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_ln(x1, y1, x2, y2, thick):
    glLineWidth(thick)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_tri(x1, y1, x2, y2, x3, y3):
    global house_col
    glBegin(GL_TRIANGLES)
    glColor3f(*house_col)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()

def init_rain():
   global rain
   rain = [(random.randint(0, 600), random.randint(300, 600)) for _ in range(120)]

def update_rain():
    global rain, dir_shift
    updated = []
    for (x, y) in rain:
      y -= 2
      x += dir_shift * 0.5
      if y < 0:
          y = random.randint(550, 600)
          x = random.randint(0, 600)
      updated.append((x, y))
    rain = updated

def render_rain():
    global tilt, house_col
    glColor3f(*house_col)
    for (x, y) in rain: 
        draw_ln(x + tilt, y, x, y - 12, 1)

def handle_keys(key, x, y):
    global dir_shift, tilt, bg_col, house_col
    if key == GLUT_KEY_LEFT:
        dir_shift = -1
        tilt += 4
    elif key == GLUT_KEY_RIGHT:
        dir_shift = 1
        tilt -= 3
    elif key == GLUT_KEY_DOWN:
        dir_shift = 0
    elif key == b'd':
        r, g, b, a = bg_col
        bg_col = min(r + 0.15, 1.0), min(g + 0.15, 1.0), min(b + 0.15, 1.0), a
        r, g, b = house_col
        house_col = max(r - 0.15, 0.0), max(g - 0.15, 0.0), max(b - 0.15, 0.0)
    elif key == b'n':
        r, g, b, a = bg_col
        bg_col = max(r - 0.15, 0.0), max(g - 0.15, 0.0), max(b - 0.15, 0.0), a
        r, g, b = house_col
        house_col = min(r + 0.15, 1.0), min(g + 0.15, 1.0), min(b + 0.15, 1.0)
    glutPostRedisplay()

def setup_projection():
    glViewport(0, 0, 600, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 600, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*bg_col)
    glLoadIdentity()
    setup_projection()
    glColor3f(*house_col)
    render_rain()
    draw_ln(150, 70, 450, 70, 8)
    draw_ln(150, 70, 150, 300, 8)
    draw_ln(450, 70, 450, 300, 8)
    draw_ln(200, 70, 200, 180, 2)
    draw_ln(280, 70, 280, 180, 2)
    draw_ln(200, 180, 280, 180, 2)
    draw_ln(350, 190, 430, 190, 2)
    draw_ln(350, 190, 350, 260, 2)
    draw_ln(430, 190, 430, 260, 2)
    draw_ln(430, 260, 350, 260, 2)
    draw_ln(390, 190, 390, 260, 2)
    draw_ln(350, 220, 430, 220, 2)
    draw_pt(215, 120)
    draw_tri(80, 280, 300, 400, 520, 280)
    draw_tri(100, 290, 300, 390, 500, 290)
    glutSwapBuffers()

def animate():
    update_rain()
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(600, 600)
glutInitWindowPosition(50, 50)
window = glutCreateWindow(b"Task 1: Building a House in Rainfall")
init_rain()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(handle_keys)
glutSpecialFunc(handle_keys)
glutMainLoop()
'''

#Task-2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

win_w, win_h = 700, 500
pts = []
is_blink = False
is_freeze = False
spd = 0.02
blink_delay = 20 

def create_point(px, py):
    return {
        "x": px,
        "y": py,
        "dx": random.choice([-1, 1]) * random.uniform(0.02, 0.03),
        "dy": random.choice([-1, 1]) * random.uniform(0.02, 0.03),
        "clr": [random.random(), random.random(), random.random()],
        "vis": True,
        "blink_timer": 0,  
    }


def update_points():
    global pts, spd
    for pt in pts:
        if not is_freeze:
            pt["x"] += pt["dx"] * spd
            pt["y"] += pt["dy"] * spd
            if pt["x"] > 1 or pt["x"] < -1:
                pt["dx"] *= -1
            if pt["y"] > 1 or pt["y"] < -1:
                pt["dy"] *= -1
            if is_blink:
                pt["blink_timer"] += 1
                if pt["blink_timer"] >= blink_delay:
                    pt["vis"] = not pt["vis"] 
                    pt["blink_timer"] = 0  


def render_points():
    for pt in pts:
        if is_blink and not pt["vis"]:
            continue
        glColor3f(*pt["clr"])
        glBegin(GL_POINTS)
        glVertex2f(pt["x"], pt["y"])
        glEnd()


def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT)
    render_points()
    glutSwapBuffers()


def handle_idle():
    update_points()
    glutPostRedisplay()
    time.sleep(0.04)


def mouse_input(btn, state, x, y):
    global is_blink
    if btn == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not is_freeze:
        px = (x / win_w) * 2 - 1
        py = -((y / win_h) * 2 - 1)
        pts.append(create_point(px, py))
    elif btn == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not is_freeze:
        is_blink = not is_blink


def keyboard_input(key, x, y):
    global spd, is_freeze, is_blink
    if key == b' ':
        is_freeze = not is_freeze
        if is_freeze:
            is_blink = False
    elif key == GLUT_KEY_UP and not is_freeze:
        spd += 0.02
    elif key == GLUT_KEY_DOWN and not is_freeze:
        spd = max(0.01, spd - 0.02)


def setup_window():
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    glPointSize(8)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(win_w, win_h)
glutCreateWindow(b"Task 2: Building The Amazing Box")
setup_window()
glutDisplayFunc(draw_scene)
glutIdleFunc(handle_idle)
glutMouseFunc(mouse_input)
glutKeyboardFunc(keyboard_input)
glutSpecialFunc(keyboard_input)
glutMainLoop()
