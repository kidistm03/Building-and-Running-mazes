# Maze Generator and Solver 
## Project Overview

This project is a procedural maze generator and solver built using Python, Pygame, and OpenGL.
It visually demonstrates how a maze can be generated using a Depth-First Search (DFS) backtracking algorithm and then solved using a stack-based pathfinding method.

## The program dynamically shows:

Maze generation (“mouse eating walls”)
Maze solving (red path traversal)
Dead ends (blue markers)
Start and end points

## Objective

The goal of this project is to:

Generate a proper rectangular maze of size ROWS x COLS
Ensure every cell is connected by a unique path (perfect maze)
Find and display a path from:
Start (left edge) → End (right edge)
Visualize both generation and solving processes in real-time

## Maze Representation

The maze is represented using two 2D arrays:

northWall[i][j] → top wall of cell (i, j)
eastWall[i][j]  → right wall of cell (i, j)
Wall Rules:
1 → wall exists
0 → wall removed
Special Structure:
Bottom boundary is handled using northWall of last row
Left boundary is implicitly handled using eastWall[i][0]

## Maze Generation Algorithm

The maze is generated using a randomized Depth-First Search (DFS) approach:

Steps:
Start from a random cell
Mark it as visited
Randomly choose an unvisited neighbor
Remove the wall between current and neighbor
Push current cell to stack
Move to neighbor
If stuck → backtrack using stack
Repeat until all cells are visited

## Key Idea:

This creates a perfect maze (spanning tree) where:

Every cell is reachable
There is exactly one path between any two cells

## Maze Solver Algorithm

The solver uses a stack-based DFS backtracking algorithm:

Steps:
Start from the random start cell (left edge)
Try moving in available directions (no wall + not visited)
Choose a valid move randomly
Push current position to stack
Move forward
If stuck:
Mark as dead end (blue point)
Backtrack using stack
Continue until reaching the end cell

## Bonus Feature (Cycle Creation)

To make the maze more interesting, the generator occasionally:

Removes an extra wall with probability 1/20
This creates cycles in the maze
Prevents purely tree-like structure
Makes solving less predictable
### 🎮 Visualization Features
### 🟩 Green dot → Start position
### 🟨 Yellow dot → End position
### 🔴 Red dot → Current solver position
### 🔵 Blue dots → Dead ends
### White lines → Maze walls

## Technologies Used
Python
Pygame
PyOpenGL
Random module (for maze randomness)

## Project Structure
```
Maze Project/
│── main.py
│── README.md
```
## Key Concepts Used
Depth-First Search (DFS)
Backtracking algorithm
Stack data structure
Graph traversal
Randomized algorithms
Grid-based representation

## Learning Outcome

This project demonstrates:

How recursive backtracking works in real applications
How mazes can be modeled as graphs
Practical use of stacks in algorithm design
Real-time visualization of algorithms
