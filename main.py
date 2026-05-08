import pygame
from pygame.locals import *
from OpenGL.GL import *
import random

# -------------------------
# Initialize
# -------------------------
pygame.init()

WIDTH = 800
HEIGHT = 800

pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Maze Generator and Solver")

# -------------------------
# Maze Settings
# -------------------------
ROWS = 10
COLS = 10
MARGIN = 0.12

northWall = [[1 for _ in range(COLS)] for _ in range(ROWS)]
eastWall = [[1 for _ in range(COLS)] for _ in range(ROWS)]

# -------------------------
# Draw Maze Walls
# -------------------------
def draw_walls():

    glColor3f(1, 1, 1)
    glLineWidth(2)

    glBegin(GL_LINES)

    for i in range(ROWS):
        for j in range(COLS):

            x = -1 + MARGIN + ((2 - 2 * MARGIN) * j / COLS)
            y = -1 + MARGIN + ((2 - 2 * MARGIN) * i / ROWS)

            x_next = -1 + MARGIN + ((2 - 2 * MARGIN) * (j + 1) / COLS)
            y_next = -1 + MARGIN + ((2 - 2 * MARGIN) * (i + 1) / ROWS)

            # Top wall
            if northWall[i][j] == 1:
                glVertex2f(x, y_next)
                glVertex2f(x_next, y_next)

            # Right wall
            if eastWall[i][j] == 1:
                glVertex2f(x_next, y)
                glVertex2f(x_next, y_next)
        # -------------------------
    # Draw Left Border
    # -------------------------
    for i in range(ROWS):

        y = -1 + MARGIN + ((2 - 2 * MARGIN) * i / ROWS)
        y_next = -1 + MARGIN + ((2 - 2 * MARGIN) * (i + 1) / ROWS)

        x = -1 + MARGIN

        # Leave entrance open
        if i != 0:
            glVertex2f(x, y)
            glVertex2f(x, y_next)

    # -------------------------
    # Draw Bottom Border
    # -------------------------
    for j in range(COLS):

        x = -1 + MARGIN + ((2 - 2 * MARGIN) * j / COLS)
        x_next = -1 + MARGIN + ((2 - 2 * MARGIN) * (j + 1) / COLS)

        y = -1 + MARGIN

        # Leave exit open
        if j != COLS - 1:
            glVertex2f(x, y)
            glVertex2f(x_next, y)
    glEnd()

# -------------------------
# Generate Maze
# -------------------------
def generate_maze():

    stack = []
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

    current = (0, 0)
    visited[0][0] = True

    while True:

        i, j = current

        neighbors = []

        # North
        if i > 0 and not visited[i - 1][j]:
            neighbors.append((i - 1, j, 'N'))

        # South
        if i < ROWS - 1 and not visited[i + 1][j]:
            neighbors.append((i + 1, j, 'S'))

        # West
        if j > 0 and not visited[i][j - 1]:
            neighbors.append((i, j - 1, 'W'))

        # East
        if j < COLS - 1 and not visited[i][j + 1]:
            neighbors.append((i, j + 1, 'E'))

        if neighbors:

            stack.append(current)

            ni, nj, direction = random.choice(neighbors)

            # Remove walls
            if direction == 'N':
                northWall[i - 1][j] = 0

            elif direction == 'S':
                northWall[i][j] = 0

            elif direction == 'W':
                eastWall[i][j - 1] = 0

            elif direction == 'E':
                eastWall[i][j] = 0

            current = (ni, nj)

            visited[ni][nj] = True

        elif stack:
            current = stack.pop()

        else:
            break

# -------------------------
# Solve Maze
# -------------------------
def solve_maze():

    stack = [(0, 0)]

    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

    while stack:

        i, j = stack[-1]

        if (i, j) == (ROWS - 1, COLS - 1):
            return stack

        visited[i][j] = True

        moved = False

        # North
        if i > 0 and northWall[i - 1][j] == 0 and not visited[i - 1][j]:
            stack.append((i - 1, j))
            moved = True

        # South
        elif i < ROWS - 1 and northWall[i][j] == 0 and not visited[i + 1][j]:
            stack.append((i + 1, j))
            moved = True

        # West
        elif j > 0 and eastWall[i][j - 1] == 0 and not visited[i][j - 1]:
            stack.append((i, j - 1))
            moved = True

        # East
        elif j < COLS - 1 and eastWall[i][j] == 0 and not visited[i][j + 1]:
            stack.append((i, j + 1))
            moved = True

        if not moved:
            stack.pop()

    return []

# -------------------------
# Draw Path
# -------------------------
def draw_path(path):

    glColor3f(1, 0, 0)

    glLineWidth(4)

    glBegin(GL_LINE_STRIP)

    cell_width = (2 - 2 * MARGIN) / COLS
    cell_height = (2 - 2 * MARGIN) / ROWS

    for i, j in path:

        x = -1 + MARGIN + (j * cell_width) + (cell_width / 2)
        y = -1 + MARGIN + (i * cell_height) + (cell_height / 2)

        glVertex2f(x, y)

    glEnd()

# -------------------------
# Draw Start and End Points
# -------------------------
def draw_points():

    glPointSize(14)

    glBegin(GL_POINTS)

    cell_width = (2 - 2 * MARGIN) / COLS
    cell_height = (2 - 2 * MARGIN) / ROWS

    # Start point (Green)
    glColor3f(0, 1, 0)

    start_x = -1 + MARGIN + (cell_width / 2)
    start_y = -1 + MARGIN + (cell_height / 2)

    glVertex2f(start_x, start_y)

    # End point (Blue)
    glColor3f(0, 0, 1)

    end_x = -1 + MARGIN + ((COLS - 1) * cell_width) + (cell_width / 2)
    end_y = -1 + MARGIN + ((ROWS - 1) * cell_height) + (cell_height / 2)

    glVertex2f(end_x, end_y)

    glEnd()

# -------------------------
# Run Maze Logic
# -------------------------
generate_maze()

path = solve_maze()
# Open maze entrance
northWall[0][0] = 0

# Open maze exit
northWall[ROWS - 1][COLS - 1] = 0
# -------------------------
# Main Loop
# -------------------------
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT)

    draw_walls()
    draw_path(path)
    draw_points()

    pygame.display.flip()

pygame.quit()