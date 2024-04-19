import math
import heapq

# Cell Class
class Cell:
    def __init__(self):
        self.parent_i = 0 #parent's row
        self.parent_j = 0 #parent's column
        #Cost from start of this cell
        self.g = float('inf')
        #Heuristic cost to goal
        self.h = float('inf')
        #Total cost (g+h)
        self.f = float('inf')

# Grid Definition
ROW = 10
COL = 10

# Check if the cell within the grid
def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if the cell is blocked or not
def is_unblocked(grid, row, col):
    return grid[row][col] == 1

# Check if the cell is the goal
def is_goal(row, col, goal):
    return row == goal[0] and col == goal[1]

# Calculate the heuristic cost
def calculate_heuristic(row, col, goal):
    return math.sqrt((row - goal[0]) ** 2 + (col - goal[1]) ** 2)

# Trace the path from start to goal
def trace_path(cell_details, goal):
    print("The path is:")
    path = []
    row = goal[0]
    col = goal[1]

    # Trace the path from the goal to the start using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append([row, col])
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col
    
    # Add the start cell
    path.append((row, col))
    # Reverse the path to get the start to goal path
    path.reverse()

    # Print the path
    for i in range(len(path)):
        print(path[i], end=' ')
    print()

# Implementing A* Algorithm
def a_star_algorithm(grid, src, goal):
    # Check if the start and goal are within the grid
    if not is_valid(src[0], src[1]):
        print("Start is invalid")
        return
    if not is_valid(goal[0], goal[1]):
        print("Goal is invalid")
        return
    
    # Check if the start and goal are unblocked
    if not is_unblocked(grid, src[0], src[1]):
        print("Start is blocked")
        return
    if not is_unblocked(grid, goal[0], goal[1]):
        print("Goal is blocked")
        return
    
    # Check if the start is the goal
    if is_goal(src[0], src[1], goal):
        print("Start is the goal")
        return

    # Closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Cell details
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell
    i = src[0]
    j = src[1]
    cell_details[i][j].g = 0.0
    cell_details[i][j].h = 0.0
    cell_details[i][j].f = 0.0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Add start cell to the open list
    open_list = []
    heapq.heappush(open_list, (0.0, (i, j)))

    # Flag to indicate goal found or not
    found_goal = False

    # Main Loop for searching
    while len(open_list) > 0:
        # Pop the smallest f value cell from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # Check each direction for the next cell
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # Check if the cell is valid
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # Check if the cell is the goal
                if is_goal(new_i, new_j, goal):
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    print("Goal found")
                    trace_path(cell_details, goal)
                    found_goal = True
                    return
                else:
                    # Calculate the g, h, and f values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_heuristic(new_i, new_j, goal)
                    f_new = g_new + h_new

                    # Check if the cell is already in the open list
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, (new_i, new_j)))

                        # Update the cell details
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    # Goal not found
    if not found_goal:
        print("Goal not found")

def main():
    # Grid (1 for unblocked, 0 for blocked)
    grid = [
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1]
    ]

    # Start and Goal
    src = (0, 1)
    dest = (9, 9)

    # Run the A* Algorithm
    a_star_algorithm(grid, src, dest)

if __name__ == "__main__":
    main()