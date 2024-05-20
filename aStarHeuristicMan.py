from collections import deque

def read_grid_from_file(filename):
    with open(filename, 'r') as file:
        grid = [list(line.strip()) for line in file]
    return grid

def create_graph(grid):
    graph = {}
    rows = len(grid)
    cols = len(grid[0])
    
    # Define the possible directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 'X':  # Consider only open spaces
                neighbors = []
                for dx, dy in directions:
                    x, y = i + dx, j + dy
                    if 0 <= x < rows and 0 <= y < cols and grid[x][y] != 'X':
                        neighbors.append((x, y))
                graph[(i, j)] = neighbors
    return graph

def calculate_heuristic(node, end):
    # Calculate Manhattan distance heuristic
    return abs(node[0] - end[0]) + abs(node[1] - end[1])

def a_star(graph, start, end):
    # Initialize the priority queue with the start node
    queue = deque([(0, start)])
    visited = set([start])
    # Keep track of the previous node in the shortest path
    prev = {}

    # Keep track of the cost from start to each node
    g_values = {start: 0}

    while queue:
        _, node = queue.popleft()
        if node == end:
            break  # Reached the end node

        for neighbor in graph[node]:
            new_g = g_values[node] + 1  # Assuming each move has a cost of 1

            if neighbor not in g_values or new_g < g_values[neighbor]:
                g_values[neighbor] = new_g
                f_value = new_g + calculate_heuristic(neighbor, end)
                prev[neighbor] = node
                visited.add(neighbor)
                queue.append((f_value, neighbor))
                # Re-sort the queue based on the updated f-values
                queue = deque(sorted(queue, key=lambda x: x[0]))
    
    # Reconstruct the shortest path
    path = []
    while end in prev:
        path.insert(0, end)
        end = prev[end]
    if path:
        path.insert(0, start)
    print(len(queue))
    print(len(visited))
    return path, visited

def mark_explored(grid, explored):
    for node in explored:
        x, y = node
        if grid[x][y] != 'S' and grid[x][y] != 'E':
            grid[x][y] = '.'
    return grid

def mark_path(grid, path):
    for node in path:
        x, y = node
        if grid[x][y] != 'S' and grid[x][y] != 'E':
            grid[x][y] = '*'
    return grid

def print_grid(grid):
    for row in grid:
        print(''.join(row))

# File containing the grid data
filename = "pathFindingMap.txt"

# Read the grid from the file
grid = read_grid_from_file(filename)

# Find the start and end positions
start = None
end = None
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == 'S':
            start = (i, j)
        elif grid[i][j] == 'E':
            end = (i, j)
        if start and end:
            break
    if start and end:
        break

# Create the graph from the grid
graph = create_graph(grid)

# Perform A* search to find the shortest path
path, visited = a_star(graph, start, end)

if path:
    # Mark the explored spots during the search
    explored = set(visited)
    # Mark explored spots
    grid = mark_explored(grid, explored)
    # Mark the path found with asterisks
    grid = mark_path(grid, path)
    # Print the updated grid
    print_grid(grid)
    print(len(path) - 1)  # Length of the path excluding the start node
else:
    print("No path found!")
