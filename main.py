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

# northWall[i][j] = 1 → wall exists
# eastWall[i][j] = 1 → wall exists
northWall = [[1 for _ in range(COLS)] for _ in range(ROWS)]
eastWall = [[1 for _ in range(COLS)] for _ in range(ROWS)]

# -------------------------
# Maze Generation Variables
# -------------------------
visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
stack = []

current = (0, 0)
visited[0][0] = True
generation_complete = False

# -------------------------
# Solver Variables
# -------------------------
solver_stack = []
solver_visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
dead_ends = []
solver_complete = False
current_solver = (0, 0)

# Random START (left edge) and END (right edge)
start = (random.randint(0, ROWS - 1), 0)
end = (random.randint(0, ROWS - 1), COLS - 1)

solver_stack.append(start)

# -------------------------
# Helper Function
# -------------------------
def get_cell_center(i, j):
    cell_width = (2 - 2 * MARGIN) / COLS
    cell_height = (2 - 2 * MARGIN) / ROWS

    x = -1 + MARGIN + (j * cell_width) + (cell_width / 2)
    y = -1 + MARGIN + (i * cell_height) + (cell_height / 2)

    return x, y

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

            if northWall[i][j] == 1:
                glVertex2f(x, y_next)
                glVertex2f(x_next, y_next)

            if eastWall[i][j] == 1:
                glVertex2f(x_next, y)
                glVertex2f(x_next, y_next)

    glEnd()

# -------------------------
# Maze Generation (DFS)
# -------------------------
def generate_maze_step():
    global current, generation_complete

    if generation_complete:
        return

    i, j = current
    neighbors = []

    if i > 0 and not visited[i - 1][j]:
        neighbors.append((i - 1, j, 'N'))
    if i < ROWS - 1 and not visited[i + 1][j]:
        neighbors.append((i + 1, j, 'S'))
    if j > 0 and not visited[i][j - 1]:
        neighbors.append((i, j - 1, 'W'))
    if j < COLS - 1 and not visited[i][j + 1]:
        neighbors.append((i, j + 1, 'E'))

    if neighbors:
        stack.append(current)

        ni, nj, direction = random.choice(neighbors)

        # remove wall
        if direction == 'N':
            northWall[i - 1][j] = 0
        elif direction == 'S':
            northWall[i][j] = 0
        elif direction == 'W':
            eastWall[i][j - 1] = 0
        elif direction == 'E':
            eastWall[i][j] = 0

        # BONUS: create cycles sometimes (1/20)
        if random.randint(1, 20) == 1:
            if direction == 'N' and i > 0:
                northWall[i - 1][j] = 0
            if direction == 'S' and i < ROWS - 1:
                northWall[i][j] = 0
            if direction == 'W' and j > 0:
                eastWall[i][j - 1] = 0
            if direction == 'E' and j < COLS - 1:
                eastWall[i][j] = 0

        current = (ni, nj)
        visited[ni][nj] = True

    elif stack:
        current = stack.pop()

    else:
        generation_complete = True

# -------------------------
# Maze Solver (Random DFS)
# -------------------------
def solve_maze_step():
    global solver_complete, current_solver

    if solver_complete:
        return

    if not solver_stack:
        solver_complete = True
        return

    i, j = solver_stack[-1]
    current_solver = (i, j)

    if (i, j) == end:
        solver_complete = True
        return

    solver_visited[i][j] = True

    moves = []

    if i > 0 and northWall[i - 1][j] == 0:
        moves.append((i - 1, j))
    if i < ROWS - 1 and northWall[i][j] == 0:
        moves.append((i + 1, j))
    if j > 0 and eastWall[i][j - 1] == 0:
        moves.append((i, j - 1))
    if j < COLS - 1 and eastWall[i][j] == 0:
        moves.append((i, j + 1))

    random.shuffle(moves)

    moved = False

    for ni, nj in moves:
        if not solver_visited[ni][nj]:
            solver_stack.append((ni, nj))
            moved = True
            break

    if not moved:
        dead_ends.append((i, j))
        solver_stack.pop()

# -------------------------
# Draw Helpers
# -------------------------
def draw_dead_ends():
    glPointSize(8)
    glBegin(GL_POINTS)
    glColor3f(0, 0, 1)

    for i, j in dead_ends:
        x, y = get_cell_center(i, j)
        glVertex2f(x, y)

    glEnd()

def draw_solver_path():
    glColor3f(1, 0, 0)
    glLineWidth(3)
    glBegin(GL_LINE_STRIP)

    for i, j in solver_stack:
        x, y = get_cell_center(i, j)
        glVertex2f(x, y)

    glEnd()

def draw_mouse():
    glPointSize(12)
    glBegin(GL_POINTS)
    glColor3f(1, 0, 0)

    x, y = get_cell_center(current_solver[0], current_solver[1])
    glVertex2f(x, y)

    glEnd()

def draw_points():
    glPointSize(14)
    glBegin(GL_POINTS)

    # start
    glColor3f(0, 1, 0)
    x, y = get_cell_center(start[0], start[1])
    glVertex2f(x, y)

    # end
    glColor3f(1, 1, 0)
    x, y = get_cell_center(end[0], end[1])
    glVertex2f(x, y)

    glEnd()

# -------------------------
# Main Loop
# -------------------------
running = True
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT)

    if not generation_complete:
        generate_maze_step()
    else:
        if not solver_complete:
            solve_maze_step()

    draw_walls()
    draw_dead_ends()
    draw_solver_path()
    draw_mouse()
    draw_points()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()