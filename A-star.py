# Import libraries

import pygame
import math
from queue import PriorityQueue

# Set window dimesions
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

# window caption
pygame.display.set_caption("A* Pathfinding")

# color presets
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Spot class


class Spot:
    def __init__(self, row, col, width, total_rows) -> None:
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # get position
    def getPos(self):
        return self.row, self.col

    # Get state color
    def isClosed(self):
        return self.color == RED

    def isOpen(self):
        return self.color == GREEN

    def isBarrier(self):
        return self.color == BLACK

    def isStart(self):
        return self.color == ORANGE

    def isEnd(self):
        return self.color == TURQUOISE

    def isPath(self):
        return self.color == PURPLE

    def reset(self):
         self.color = WHITE

    # set state color

    def setClosed(self):
        self.color = RED

    def setOpen(self):
        self.color = GREEN

    def setBarrier(self):
        self.color = BLACK

    def setStart(self):
        self.color = ORANGE

    def setEnd(self):
        self.color = TURQUOISE

    def setPath(self):
        self.color = PURPLE

    # draw function
    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbors(self, grid):
        self.neighbors = []

        # down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isBarrier() : 
            self.neighbors.append(grid[self.row + 1][self.col])
        
        # up
        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier() : 
            self.neighbors.append(grid[self.row - 1][self.col])
        
        # right
        if self.col < self.total_rows - 1 and not grid[self.row ][self.col + 1].isBarrier() : 
            self.neighbors.append(grid[self.row ][self.col + 1])
        
        # left
        if self.col > 0 and not grid[self.row ][self.col  - 1].isBarrier() :
            self.neighbors.append(grid[self.row ][self.col -1])

        # DIAGONALS 

        # top left
        if self.row  > 0 and self.col > 0 and not grid[self.row -1 ][self.col  - 1].isBarrier() :
            self.neighbors.append(grid[self.row -1 ][self.col -1])
        
        # top right
        if self.row  > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1 ][self.col  + 1].isBarrier() :
            self.neighbors.append(grid[self.row -1 ][self.col + 1])

        # bottom left
        if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row  + 1 ][self.col  - 1].isBarrier() :
            self.neighbors.append(grid[self.row + 1 ][self.col -1])
        
        # bottom right
        if self.row < self.total_rows - 1  and self.col < self.total_rows - 1 and not grid[self.row + 1 ][self.col  + 1].isBarrier() :
            self.neighbors.append(grid[self.row + 1 ][self.col +1])

        

    def __lt__(slef, other):
        return False

# Hueristic function
def h(p1, p2):

    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)

# draw path
def reconstructPath(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.setPath()
        draw()

# A* Algorithm
def a_star(Draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))  
    came_from = {}
    g_score = {spot : float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot : float('inf') for row in grid for spot in row}
    f_score[start] = h(start.getPos(), end.getPos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end :
            reconstructPath(came_from, end, Draw)
            end.setEnd()
            start.setStart()
            return True
    
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.getPos(), end.getPos())

                if neighbor not in open_set_hash :

                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.setOpen()
        
        Draw()

        if current != start:
            current.setClosed()

    return False

# grid data structure
def makeGrid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

# draw grid lines
def drawGridLines(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# draw function
def Draw(win, grid, rows, width):

    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    drawGridLines(win, rows, width)
    pygame.display.update()

# Get spot clicked
def getClickedPosition(pos, rows, width):

    gap = width // rows

    i, j = pos

    row = i // gap
    col = j // gap

    return row, col


# Main function
def main(win, width):

    ROWS = 50
    grid = makeGrid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:

        Draw(win,grid, ROWS, width )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPosition(pos, ROWS, width)
                spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.setStart()
                elif not end and spot != start:
                    end = spot
                    end.setEnd()
                elif spot != end and spot != start  :
                    spot.setBarrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPosition(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()

                if spot == start :
                    start = None
                elif spot == end :
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                   
                    for row in grid :
                        for spot in row :
                            spot.updateNeighbors(grid)
                    
                    a_star(lambda: Draw(win, grid, ROWS, width), grid, start , end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = makeGrid(ROWS, width)
          
    pygame.quit()


main(WIN, WIDTH)
