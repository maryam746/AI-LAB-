import heapq

# ============================================================
# GREEDY BEST FIRST SEARCH
# ============================================================

# Graph with different edge costs
graph = {
    'A': {'B': 2, 'C': 1},
    'B': {'D': 4, 'E': 3},
    'C': {'F': 1, 'G': 5},
    'D': {'H': 2},
    'E': {},
    'F': {'I': 6},
    'G': {},
    'H': {},
    'I': {}
}

# Heuristic function (estimated cost to reach goal 'I')
heuristic = {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 7, 'F': 3, 'G': 6, 'H': 2, 'I': 0}

# Greedy Best-First Search Function (without heapq)
def greedy_bfs(graph, start, goal):
    frontier = [(start, heuristic[start])]          # list-based priority queue
    visited = set()                                 # visited nodes
    came_from = {start: None}                       # path reconstruction

    while frontier:
        # Sort frontier manually by heuristic value (ascending)
        frontier.sort(key=lambda x: x[1])
        current_node, _ = frontier.pop(0)           # node with best heuristic

        if current_node in visited:
            continue
        print(current_node, end=" ")
        visited.add(current_node)

        # Goal test
        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"\nGoal found with GBFS. Path: {path}")
            return

        # Expand neighbors
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                came_from[neighbor] = current_node
                frontier.append((neighbor, heuristic[neighbor]))

    print("\nGoal not found")

# Run Greedy Best-First Search
print("\nFollowing is the Greedy Best-First Search (GBFS):")
greedy_bfs(graph, 'A', 'I')


# ============================================================
# A* SEARCH
# ============================================================

# Graph for A* (nodes and edge costs)
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'D': 2, 'E': 5},
    'C': {'F': 1, 'G': 3},
    'D': {},
    'E': {'G': 2},
    'F': {'G': 2},
    'G': {}
}

# Heuristic (estimated cost from node to goal 'G')
heuristic = {
    'A': 7, 'B': 6, 'C': 2,
    'D': 5, 'E': 3, 'F': 1,
    'G': 0
}


def a_star(graph, start, goal):
    frontier = [(start, heuristic[start])]          # (node, f(n)) list, sorted manually
    visited = set()                                 # closed set
    g_costs = {start: 0}                            # cost from start to each node
    came_from = {start: None}                       # parent pointers

    while frontier:
        # Sort by f(n) = g(n) + h(n)
        frontier.sort(key=lambda x: x[1])
        current_node, current_f = frontier.pop(0)   # node with lowest f(n)

        if current_node in visited:
            continue
        print(current_node, end=" ")
        visited.add(current_node)

        # Goal reached → reconstruct path
        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"\nGoal found with A*. Path: {path}")
            return

        # Expand neighbors
        for neighbor, cost in graph[current_node].items():
            new_g = g_costs[current_node] + cost
            f_cost = new_g + heuristic[neighbor]

            if neighbor not in g_costs or new_g < g_costs[neighbor]:
                g_costs[neighbor] = new_g
                came_from[neighbor] = current_node
                frontier.append((neighbor, f_cost))

    print("\nGoal not found")

# Run A* Search
print("\nFollowing is the A* Search:")
a_star(graph, 'A', 'G')


# ============================================================
# BREADTH FIRST SEARCH
# ============================================================

# Graph Representation
graph = {
    0: [1, 3],
    1: [0, 3],
    2: [4, 5],
    3: [0, 1, 6, 4],
    4: [3, 2, 5],
    5: [4, 2, 6],
    6: [3, 5]
}


# BFS Function
def bfs(graph, start, goal):
    visited = []  # List for visited nodes
    queue = []    # Initialize a queue

    visited.append(start)
    queue.append(start)

    while queue:
        node = queue.pop(0)  # Dequeue
        print(node, end=" ")

        if node == goal:  # Stop if goal is found
            print("\nGoal found!")
            break

        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)

# Define Start and Goal Nodes
start_node = 0
goal_node = 5

# Run BFS
print("\nFollowing is the Breadth-First Search (BFS):")
bfs(graph, start_node, goal_node)


# ============================================================
# BEAM SEARCH
# ============================================================

graph = {
    'S': [('A', 3), ('B', 6), ('C', 5)],
    'A': [('D', 9), ('E', 8)],
    'B': [('F', 12), ('G', 14)],
    'C': [('H', 7)],
    'H': [('I', 5), ('J', 6)],
    'I': [('K', 1), ('L', 10), ('M', 2)],
    'D': [], 'E': [],
    'F': [], 'G': [],
    'J': [], 'K': [],
    'L': [], 'M': []
}

# Beam Search function
def beam_search(start, goal, beam_width=2):
    # Initialize the beam with the start state
    beam = [(0, [start])]  # (cumulative cost, path)

    while beam:
        candidates = []
        # Expand each path in the beam
        for cost, path in beam:
            current_node = path[-1]
            if current_node == goal:
                return path, cost  # Return the path and cost if goal
            # Generate successors
            for neighbor, edge_cost in graph.get(current_node, []):
                new_cost = cost + edge_cost
                new_path = path + [neighbor]
                candidates.append((new_cost, new_path))

        # Select top-k paths based on the lowest cumulative cost
        beam = heapq.nsmallest(beam_width, candidates, key=lambda x: x[0])

    return None, float('inf')  # Return None if no path is found


# Run Beam Search
start_node = 'S'
goal_node = 'L'
beam_width = 3
path, cost = beam_search(start=start_node, goal=goal_node, beam_width=beam_width)

# Print results
if path:
    print(f"\nPath found: {' → '.join(path)} with total cost: {cost}")
else:
    print("No path found.")


# ============================================================
# UTILITY BASED AGENT
# ============================================================

class UtilityBasedAgent:
    def __init__(self):
        self.utility = {'Dirty': -10, 'Clean': 10}

    def calculate_utility(self, percept):
        return self.utility[percept]

    def select_action(self, percept):
        if percept == 'Dirty':
            return 'Clean the room'
        else:
            return 'No action needed'

    def act(self, percept):
        action = self.select_action(percept)
        return action


class UtilityEnvironment:
    def __init__(self, state='Dirty'):
        self.state = state

    def get_percept(self):
        return self.state

    def clean_room(self):
        self.state = 'Clean'


def run_utility_agent(agent, environment, steps):
    total_utility = 0
    for step in range(steps):
        percept = environment.get_percept()
        action = agent.act(percept)
        utility = agent.calculate_utility(percept)
        print(f"Step {step + 1}: Percept - {percept}, Action - {action}, Utility - {utility}")
        total_utility += utility
        if percept == 'Dirty':
            environment.clean_room()
    print("Total Utility:", total_utility)


# Create instances of agent and environment
print("\n--- Utility Based Agent ---")
agent = UtilityBasedAgent()
environment = UtilityEnvironment()

# Run the agent in the environment for 5 steps
run_utility_agent(agent, environment, 5)


# ============================================================
# SIMPLE REFLEX AGENT (Grid)
# ============================================================

class SimpleReflexAgent:
    def __init__(self):
        self.position = 0  # Start at position 0 (top-left corner)
        self.environment_model = ['Clean', 'Dirty', 'Clean',
                                  'Clean', 'Dirty', 'Dirty',
                                  'Clean', 'Clean', 'Clean']  # Initial model of the environment

    def act(self, percept):
        # If the current position is dirty, clean it
        if percept == 'Dirty':
            self.environment_model[self.position] = 'Clean'  # Clean the environment model
            return 'Clean the room'
        else:
            return 'Room is clean'

    def move(self):
        # Move to the next position in the grid
        if self.position < 8:
            self.position += 1
        return self.position

    def update_model(self, position, percept):
        # Update the agent's internal model with the percept
        self.environment_model[position] = percept

    def get_model(self):
        return self.environment_model


class GridEnvironment:
    def __init__(self):
        # Create the environment with a 3x3 grid, where 'b', 'e', and 'f' are dirty
        self.grid = ['Clean', 'Dirty', 'Clean',
                     'Clean', 'Dirty', 'Dirty',
                     'Clean', 'Clean', 'Clean']

    def get_percept(self, position):
        # Return the state of the current position
        return self.grid[position]

    def clean_room(self, position):
        # Clean the room at the given position
        self.grid[position] = 'Clean'

    def display_grid(self, agent_position):
        # Display the current state of the grid in a 3x3 format
        print("\nCurrent Grid State:")
        grid_with_agent = self.grid[:]  # Copy the grid
        grid_with_agent[agent_position] = "👽"  # Place the agent at the current position
        for i in range(0, 9, 3):
            print(" | ".join(grid_with_agent[i:i + 3]))
        print()  # Extra line for spacing


def run_grid_agent(agent, environment, steps):
    for step in range(steps):
        percept = environment.get_percept(agent.position)
        action = agent.act(percept)
        print(f"Step {step + 1}: Position {agent.position} -> Percept - {percept}, Action - {action}")

        # Update agent's internal model based on percept
        agent.update_model(agent.position, percept)

        # Display the grid state with agent's position
        environment.display_grid(agent.position)

        if percept == 'Dirty':
            environment.clean_room(agent.position)

        agent.move()


# Create instances of agent and environment
print("\n--- Simple Reflex Agent (Grid) ---")
agent = SimpleReflexAgent()
environment = GridEnvironment()

# Run the agent in the environment for 9 steps (to cover the 3x3 grid)
run_grid_agent(agent, environment, 9)


# ============================================================
# SIMPLE REFLEX AGENT (Heat Sensor)
# ============================================================

class HeatEnvironment:
    def __init__(self, heat_level='High'):
        self.heat_level = heat_level

    def get_percept(self):
        """Return the heat level of the object as the percept."""
        return 'Hot' if self.heat_level == 'High' else 'Cool'


class HeatReflexAgent:
    def __init__(self):
        pass

    def act(self, percept):
        """Determine action based on the percept (heat level)."""
        if percept == 'Hot':
            return 'Pull hand away, you touched the hot object'
        else:
            return 'You have not touched any hot object, No need to pull away'


def run_heat_agent(agent, environment):
    # The agent reacts to the heat stimulus only once
    percept = environment.get_percept()
    action = agent.act(percept)
    print(f"Percept: {percept}, Action: {action}")


# Create instances of agent and environment
print("\n--- Simple Reflex Agent (Heat Sensor) ---")
agent = HeatReflexAgent()
environment = HeatEnvironment(heat_level='Low')  # Start with a cool object

# Run the agent in the environment (only once)
run_heat_agent(agent, environment)


# ============================================================
# BEAM SEARCH VS BEST FIRST SEARCH (using frontier)
# ============================================================

graph = {
    'S': {'A': 3, 'B': 6, 'C': 5},
    'A': {'D': 9, 'E': 8},
    'B': {'F': 12, 'G': 14},
    'C': {'H': 7},
    'H': {'I': 5, 'J': 6},
    'I': {'K': 1, 'L': 10, 'M': 2},
    'D': {}, 'E': {},
    'F': {}, 'G': {},
    'J': {}, 'K': {},
    'L': {}, 'M': {}
}

heuristic = {
    'S': 10, 'A': 8, 'B': 7, 'C': 6,
    'D': 5,  'E': 4, 'F': 6, 'G': 9,
    'H': 3,  'I': 2, 'J': 5, 'K': 4,
    'L': 0,  'M': 3
}


def beam_search_frontier(graph, start, goal, beam_width=2):
    frontier = [(start, heuristic[start])]
    visited = set()
    came_from = {start: None}
    all_frontiers = []  # Store all frontiers

    while frontier:
        frontier.sort(key=lambda x: x[1])
        frontier = frontier[:beam_width]  # Keep only top beam_width nodes
        all_frontiers.append(list(frontier))  # Store current frontier
        next_frontier = []

        for current_node, _ in frontier:
            if current_node in visited:
                continue

            visited.add(current_node)

            if current_node == goal:
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = came_from[current_node]
                path.reverse()
                print(f"Goal found with Beam Search. Path: {path}")
                return path, all_frontiers

            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    next_frontier.append((neighbor, heuristic[neighbor]))
                    came_from[neighbor] = current_node

        frontier = next_frontier

    print("Goal not found")
    return None, all_frontiers


def best_first_search(graph, start, goal):
    frontier = [(start, heuristic[start])]
    visited = set()
    came_from = {start: None}
    all_frontiers = []  # Store all frontiers

    while frontier:
        frontier.sort(key=lambda x: x[1])
        all_frontiers.append(list(frontier))  # Store current frontier
        current_node, _ = frontier.pop(0)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"Goal found with Best First Search. Path: {path}")
            return path, all_frontiers

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                frontier.append((neighbor, heuristic[neighbor]))
                came_from[neighbor] = current_node

    print("Goal not found")
    return None, all_frontiers


print("\n--- Beam Search vs Best First Search ---")
print("Beam Search:")
beam_search_frontier(graph, 'S', 'L', beam_width=2)

print("\nBest First Search:")
best_first_search(graph, 'S', 'L')
