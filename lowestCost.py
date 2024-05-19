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
                        # For Dijkstra's algorithm, assign a cost of 1 for each step
                        neighbors.append(((x, y), 1))
                graph[(i, j)] = neighbors
    return graph

def dijkstra(graph, start, end):
    # Initialize the distance dictionary with infinity for all nodes
    distance = {node: float('inf') for node in graph}
    distance[start] = 0  # Distance to the start node is 0
    # Initialize the priority queue with the start node
    queue = [(0, start)]
    visited = set([start])
    # Keep track of the previous node in the shortest path
    prev = {}

    while queue:
        dist, node = queue.pop(0)
        if node == end:
            break  # Reached the end node
        if dist > distance[node]:
            continue  # Skip if we've found a shorter path already
        for neighbor, weight in graph[node]:
            alt = distance[node] + weight
            if alt < distance[neighbor]:
                distance[neighbor] = alt
                prev[neighbor] = node
                visited.add(neighbor)
                queue.append((alt, neighbor))
                # Re-sort the queue based on the updated distances
                queue.sort()
    
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

# Perform Dijkstra's algorithm to find the shortest path
path = dijkstra(graph, start, end)

if path:
    # Mark the explored spots during Dijkstra's algorithm
    explored = set(path[1])
    # Mark explored spots
    grid = mark_explored(grid, explored)
    # Mark the path found with asterisks
    grid = mark_path(grid, path[0])
    # Print the updated grid
    print_grid(grid)
    print(len(path[0]) - 1)  # Length of the path excluding the start node
else:
    print("No path found!")
