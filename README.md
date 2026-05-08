# Building and Running Mazes

## Project Description

This project generates and solves a rectangular maze using Python, OpenGL, and Pygame.

The maze is represented using two arrays:

```python
northWall[R][C]
eastWall[R][C]
```

- `northWall[i][j] = 1` means the upper wall of the cell exists.
- `eastWall[i][j] = 1` means the right wall of the cell exists.

The maze is generated dynamically using a stack-based Depth First Search (DFS) algorithm.

An invisible “mouse” moves through the maze and removes walls between randomly selected unvisited neighboring cells. The remaining candidate cells are stored on a stack for backtracking when the mouse reaches a dead end.

The maze generation process is animated in real time to visualize the wall-eating process.

After the maze is generated, a maze-solving algorithm uses backtracking and stack traversal to find a valid path from the entrance to the exit.

The final solution path is displayed graphically.



## Features

- Random maze generation
- Proper maze structure
- Stack-based DFS generation
- Animated maze construction
- OpenGL graphical rendering
- Automatic maze solving
- Entrance and exit visualization
- Red solution path visualization

---

## Technologies Used

- Python
- Pygame
- PyOpenGL

---

## How the Maze Generator Works

1. All walls are initially intact.
2. A virtual mouse starts in a random cell.
3. The mouse checks neighboring cells.
4. One unvisited neighbor is chosen randomly.
5. The wall between the cells is removed.
6. Previous cells are stored on a stack.
7. When the mouse reaches a dead end, it backtracks using the stack.
8. The process continues until all cells are visited.

This guarantees a proper maze where every cell is connected by exactly one path.

---

## Maze Solving Algorithm

The maze is solved using a stack-based backtracking algorithm.

The solver:
- moves through open paths,
- stores visited cells on a stack,
- backtracks when trapped,
- and continues until the exit is reached.

The final path is displayed visually.

---

## Running the Project

Install dependencies:

```bash
pip install pygame PyOpenGL PyOpenGL_accelerate
```

Run the program:

```bash
py main.py
```

---

## File Structure

```text
project/
│
├── main.py
├── README.md
```

---

## Author

Computer Graphics Maze Project