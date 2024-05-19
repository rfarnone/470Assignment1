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

def bfs(graph, start, end):
    queue = deque([(start, [start])])
    visited = set([start])
    
    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

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
filename = "breadthFirstPath.txt"

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

# Perform BFS to find the shortest path
path = bfs(graph, start, end)

if path:
    # Mark the explored spots during BFS
    explored = set()
    for _, nodes in graph.items():
        for node in nodes:
            if node not in path:
                explored.add(node)
    # Mark explored spots
    grid = mark_explored(grid, explored)
    # Mark the path found with asterisks
    grid = mark_path(grid, path)
    # Print the updated grid
    print_grid(grid)
else:
    print("No path found!")
