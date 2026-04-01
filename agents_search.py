import heapq

# ============================================================
#  SHARED GRAPH & HEURISTICS
# ============================================================

GRAPH = {
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

HEURISTIC = {
    'A': 7, 'B': 6, 'C': 5,
    'D': 4, 'E': 7, 'F': 3,
    'G': 6, 'H': 2, 'I': 0
}

START = 'A'
GOAL  = 'I'


# ============================================================
# HELPER – path reconstructor (shared by all agents)
# ============================================================

def reconstruct_path(came_from, goal):
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path


# ============================================================
# 1.  BFS  +  SIMPLE REFLEX AGENT
# ============================================================

class BFSEnvironment_SimpleReflex:
    """Environment that holds the graph and goal."""
    def __init__(self, graph, goal):
        self.graph    = graph
        self.goal     = goal
        self.percept  = None          # last percept seen by the agent

    def get_percept(self, node):
        """Percept: current node label."""
        self.percept = node
        return node

    def is_goal(self, node):
        return node == self.goal

    def neighbors(self, node):
        return list(self.graph[node].keys())


class BFSAgent_SimpleReflex:
    """
    Simple Reflex Agent that uses BFS.
    Rule: if current node == goal → stop; else expand BFS frontier.
    """
    def __init__(self, environment: BFSEnvironment_SimpleReflex, start):
        self.env       = environment
        self.start     = start
        self.visited   = []
        self.queue     = [start]
        self.came_from = {start: None}
        self.visited.append(start)

    def act(self, percept):
        """Reflex rule based on percept (current node)."""
        if self.env.is_goal(percept):
            return 'GOAL_REACHED'
        return 'EXPAND'

    def run(self):
        print("\n=== BFS – Simple Reflex Agent ===")
        while self.queue:
            node    = self.queue.pop(0)
            percept = self.env.get_percept(node)
            action  = self.act(percept)
            print(f"  Visiting: {node}  →  Action: {action}")

            if action == 'GOAL_REACHED':
                path = reconstruct_path(self.came_from, node)
                print(f"  Path found: {path}")
                return path

            for nb in self.env.neighbors(node):
                if nb not in self.visited:
                    self.visited.append(nb)
                    self.queue.append(nb)
                    self.came_from[nb] = node

        print("  Goal not found.")
        return None


# ============================================================
# 2.  BFS  +  UTILITY BASED AGENT
# ============================================================

class BFSEnvironment_Utility:
    def __init__(self, graph, goal):
        self.graph = graph
        self.goal  = goal

    def get_percept(self, node):
        return node

    def is_goal(self, node):
        return node == self.goal

    def neighbors(self, node):
        return list(self.graph[node].keys())


class BFSAgent_Utility:
    """
    Utility Based Agent using BFS.
    Utility: +100 for reaching goal, -1 per step taken.
    Agent always picks the action that maximises utility.
    """
    GOAL_UTILITY = 100
    STEP_COST    = -1

    def __init__(self, environment: BFSEnvironment_Utility, start):
        self.env           = environment
        self.start         = start
        self.visited       = []
        self.queue         = [start]
        self.came_from     = {start: None}
        self.visited.append(start)
        self.total_utility = 0
        self.steps         = 0

    def calculate_utility(self, node):
        if self.env.is_goal(node):
            return self.GOAL_UTILITY
        return self.STEP_COST

    def select_action(self, node):
        utility = self.calculate_utility(node)
        self.total_utility += utility
        if self.env.is_goal(node):
            return 'GOAL_REACHED', utility
        return 'EXPAND', utility

    def run(self):
        print("\n=== BFS – Utility Based Agent ===")
        while self.queue:
            node              = self.queue.pop(0)
            percept           = self.env.get_percept(node)
            action, utility   = self.select_action(percept)
            self.steps       += 1
            print(f"  Step {self.steps}: Node={node}  Utility={utility}  Action={action}  CumulativeUtility={self.total_utility}")

            if action == 'GOAL_REACHED':
                path = reconstruct_path(self.came_from, node)
                print(f"  Path found: {path}")
                print(f"  Total Utility: {self.total_utility}")
                return path

            for nb in self.env.neighbors(node):
                if nb not in self.visited:
                    self.visited.append(nb)
                    self.queue.append(nb)
                    self.came_from[nb] = node

        print("  Goal not found.")
        return None


# ============================================================
# 3.  GREEDY BEST FIRST SEARCH  +  SIMPLE REFLEX AGENT
# ============================================================

class GreedyEnvironment_SimpleReflex:
    def __init__(self, graph, heuristic, goal):
        self.graph     = graph
        self.heuristic = heuristic
        self.goal      = goal

    def get_percept(self, node):
        return node

    def is_goal(self, node):
        return node == self.goal

    def neighbors(self, node):
        return list(self.graph[node].keys())

    def h(self, node):
        return self.heuristic[node]


class GreedyAgent_SimpleReflex:
    """
    Simple Reflex Agent using Greedy Best-First Search.
    Rule: always expand the neighbour with the lowest heuristic value.
    """
    def __init__(self, environment: GreedyEnvironment_SimpleReflex, start):
        self.env       = environment
        self.frontier  = [(start, environment.h(start))]
        self.visited   = set()
        self.came_from = {start: None}

    def act(self, percept):
        if self.env.is_goal(percept):
            return 'GOAL_REACHED'
        return 'EXPAND'

    def run(self):
        print("\n=== Greedy Best-First Search – Simple Reflex Agent ===")
        while self.frontier:
            self.frontier.sort(key=lambda x: x[1])
            node, h_val = self.frontier.pop(0)

            if node in self.visited:
                continue

            percept = self.env.get_percept(node)
            action  = self.act(percept)
            self.visited.add(node)
            print(f"  Visiting: {node}  h={h_val}  →  Action: {action}")

            if action == 'GOAL_REACHED':
                path = reconstruct_path(self.came_from, node)
                print(f"  Path found: {path}")
                return path

            for nb in self.env.neighbors(node):
                if nb not in self.visited:
                    self.came_from[nb] = node
                    self.frontier.append((nb, self.env.h(nb)))

        print("  Goal not found.")
        return None


# ============================================================
# 4.  GREEDY BEST FIRST SEARCH  +  UTILITY BASED AGENT
# ============================================================

class GreedyEnvironment_Utility:
    def __init__(self, graph, heuristic, goal):
        self.graph     = graph
        self.heuristic = heuristic
        self.goal      = goal

    def get_percept(self, node):
        return node

    def is_goal(self, node):
        return node == self.goal

    def neighbors(self, node):
        return list(self.graph[node].keys())

    def h(self, node):
        return self.heuristic[node]


class GreedyAgent_Utility:
    """
    Utility Based Agent using Greedy Best-First Search.
    Utility = -h(node) so lower heuristic → higher utility.
    """
    def __init__(self, environment: GreedyEnvironment_Utility, start):
        self.env           = environment
        self.frontier      = [(start, environment.h(start))]
        self.visited       = set()
        self.came_from     = {start: None}
        self.total_utility = 0
        self.steps         = 0

    def calculate_utility(self, node):
        if self.env.is_goal(node):
            return 100
        return -self.env.h(node)       # higher when closer to goal

    def select_action(self, node):
        utility = self.calculate_utility(node)
        self.total_utility += utility
        if self.env.is_goal(node):
            return 'GOAL_REACHED', utility
        return 'EXPAND', utility

    def run(self):
        print("\n=== Greedy Best-First Search – Utility Based Agent ===")
        while self.frontier:
            self.frontier.sort(key=lambda x: x[1])
            node, h_val = self.frontier.pop(0)

            if node in self.visited:
                continue

            percept           = self.env.get_percept(node)
            action, utility   = self.select_action(percept)
            self.visited.add(node)
            self.steps       += 1
            print(f"  Step {self.steps}: Node={node}  h={h_val}  Utility={utility}  Action={action}  CumulativeUtility={self.total_utility}")

            if action == 'GOAL_REACHED':
                path = reconstruct_path(self.came_from, node)
                print(f"  Path found: {path}")
                print(f"  Total Utility: {self.total_utility}")
                return path

            for nb in self.env.neighbors(node):
                if nb not in self.visited:
                    self.came_from[nb] = node
                    self.frontier.append((nb, self.env.h(nb)))

        print("  Goal not found.")
        return None


# ============================================================
# 5.  A*  +  SIMPLE REFLEX AGENT
# ============================================================

class AStarEnvironment_SimpleReflex:
    def __init__(self, graph, heuristic, goal):
        self.graph     = graph
        self.heuristic = heuristic
        self.goal      = goal

    def get_percept(self, node):
        return node

    def is_goal(self, node):
        return node == self.goal

    def neighbors(self, node):
        return self.graph[node].items()   # (neighbor, cost) pairs

    def h(self, node):
        return self.heuristic[node]


class AStarAgent_SimpleReflex:
    """
    Simple Reflex Agent using A* Search.
    Rule: expand node with lowest f = g + h.
    """
    def __init__(self, environment: AStarEnvironment_SimpleReflex, start):
        self.env       = environment
        self.frontier  = [(start, environment.h(start))]
        self.visited   = set()
        self.g_costs   = {start: 0}
        self.came_from = {start: None}

    def act(self, percept):
        if self.env.is_goal(percept):
            return 'GOAL_REACHED'
        return 'EXPAND'

    def run(self):
        print("\n=== A* Search – Simple Reflex Agent ===")
        while self.frontier:
            self.frontier.sort(key=lambda x: x[1])
            node, f_val = self.frontier.pop(0)

            if node in self.visited:
                continue

            percept = self.env.get_percept(node)
            action  = self.act(percept)
            self.visited.add(node)
            g = self.g_costs[node]
            h = self.env.h(node)
            print(f"  Visiting: {node}  g={g}  h={h}  f={f_val}  →  Action: {action}")

            if action == 'GOAL_REACHED':
                path = reconstruct_path(self.came_from, node)
                print(f"  Path found: {path}  (total cost g={g})")
                return path

            for nb, cost in self.env.neighbors(node):
                new_g = self.g_costs[node] + cost
                if nb not in self.g_costs or new_g < self.g_costs[nb]:
                    self.g_costs[nb]   = new_g
                    self.came_from[nb] = node
                    self.frontier.append((nb, new_g + self.env.h(nb)))

        print("  Goal not found.")
        return None


# ============================================================
# 6.  A*  +  UTILITY BASED AGENT
# ============================================================

class AStarEnvironment_Utility:
    def __init__(self, graph, heuristic, goal):
        self.graph     = graph
        self.heuristic = heuristic
        self.goal      = goal

    def get_percept(self, node):
        return node

    def is_goal(self, node):
        return node == self.goal

    def neighbors(self, node):
        return self.graph[node].items()

    def h(self, node):
        return self.heuristic[node]


class AStarAgent_Utility:
    """
    Utility Based Agent using A* Search.
    Utility = 100 at goal, otherwise -(g + h) to prefer lower-cost paths.
    """
    def __init__(self, environment: AStarEnvironment_Utility, start):
        self.env           = environment
        self.frontier      = [(start, environment.h(start))]
        self.visited       = set()
        self.g_costs       = {start: 0}
        self.came_from     = {start: None}
        self.total_utility = 0
        self.steps         = 0

    def calculate_utility(self, node, f_val):
        if self.env.is_goal(node):
            return 100
        return -f_val      # prefer smaller f

    def select_action(self, node, f_val):
        utility = self.calculate_utility(node, f_val)
        self.total_utility += utility
        if self.env.is_goal(node):
            return 'GOAL_REACHED', utility
        return 'EXPAND', utility

    def run(self):
        print("\n=== A* Search – Utility Based Agent ===")
        while self.frontier:
            self.frontier.sort(key=lambda x: x[1])
            node, f_val = self.frontier.pop(0)

            if node in self.visited:
                continue

            percept           = self.env.get_percept(node)
            action, utility   = self.select_action(percept, f_val)
            self.visited.add(node)
            self.steps       += 1
            g = self.g_costs[node]
            h = self.env.h(node)
            print(f"  Step {self.steps}: Node={node}  g={g}  h={h}  f={f_val}  Utility={utility}  Action={action}  CumulativeUtility={self.total_utility}")

            if action == 'GOAL_REACHED':
                path = reconstruct_path(self.came_from, node)
                print(f"  Path found: {path}  (total cost g={g})")
                print(f"  Total Utility: {self.total_utility}")
                return path

            for nb, cost in self.env.neighbors(node):
                new_g = self.g_costs[node] + cost
                if nb not in self.g_costs or new_g < self.g_costs[nb]:
                    self.g_costs[nb]   = new_g
                    self.came_from[nb] = node
                    self.frontier.append((nb, new_g + self.env.h(nb)))

        print("  Goal not found.")
        return None


# ============================================================
# 7.  BEAM SEARCH  +  SIMPLE REFLEX AGENT
# ============================================================

class BeamEnvironment_SimpleReflex:
    def __init__(self, graph, heuristic, goal, beam_width=2):
        self.graph      = graph
        self.heuristic  = heuristic
        self.goal       = goal
        self.beam_width = beam_width

    def get_percept(self, node):
        return node

    def is_goal(self, node):
        return node == self.goal

    def neighbors(self, node):
        return list(self.graph[node].keys())

    def h(self, node):
        return self.heuristic[node]


class BeamAgent_SimpleReflex:
    """
    Simple Reflex Agent using Beam Search.
    Rule: keep only top beam_width nodes at each level; if current == goal → stop.
    """
    def __init__(self, environment: BeamEnvironment_SimpleReflex, start):
        self.env       = environment
        self.frontier  = [(start, environment.h(start))]
        self.visited   = set()
        self.came_from = {start: None}

    def act(self, percept):
        if self.env.is_goal(percept):
            return 'GOAL_REACHED'
        return 'EXPAND'

    def run(self):
        print(f"\n=== Beam Search (width={self.env.beam_width}) – Simple Reflex Agent ===")
        while self.frontier:
            # Prune to beam width
            self.frontier.sort(key=lambda x: x[1])
            self.frontier = self.frontier[:self.env.beam_width]
            next_frontier = []

            for node, h_val in self.frontier:
                if node in self.visited:
                    continue

                percept = self.env.get_percept(node)
                action  = self.act(percept)
                self.visited.add(node)
                print(f"  Visiting: {node}  h={h_val}  →  Action: {action}")

                if action == 'GOAL_REACHED':
                    path = reconstruct_path(self.came_from, node)
                    print(f"  Path found: {path}")
                    return path

                for nb in self.env.neighbors(node):
                    if nb not in self.visited:
                        self.came_from[nb] = node
                        next_frontier.append((nb, self.env.h(nb)))

            self.frontier = next_frontier

        print("  Goal not found.")
        return None


# ============================================================
# 8.  BEAM SEARCH  +  UTILITY BASED AGENT
# ============================================================

class BeamEnvironment_Utility:
    def __init__(self, graph, heuristic, goal, beam_width=2):
        self.graph      = graph
        self.heuristic  = heuristic
        self.goal       = goal
        self.beam_width = beam_width

    def get_percept(self, node):
        return node

    def is_goal(self, node):
        return node == self.goal

    def neighbors(self, node):
        return list(self.graph[node].keys())

    def h(self, node):
        return self.heuristic[node]


class BeamAgent_Utility:
    """
    Utility Based Agent using Beam Search.
    Utility = 100 at goal, -h(node) otherwise (lower h = higher utility).
    Only top beam_width candidates survive each round.
    """
    def __init__(self, environment: BeamEnvironment_Utility, start):
        self.env           = environment
        self.frontier      = [(start, environment.h(start))]
        self.visited       = set()
        self.came_from     = {start: None}
        self.total_utility = 0
        self.steps         = 0

    def calculate_utility(self, node):
        if self.env.is_goal(node):
            return 100
        return -self.env.h(node)

    def select_action(self, node):
        utility = self.calculate_utility(node)
        self.total_utility += utility
        if self.env.is_goal(node):
            return 'GOAL_REACHED', utility
        return 'EXPAND', utility

    def run(self):
        print(f"\n=== Beam Search (width={self.env.beam_width}) – Utility Based Agent ===")
        while self.frontier:
            self.frontier.sort(key=lambda x: x[1])
            self.frontier = self.frontier[:self.env.beam_width]
            next_frontier = []

            for node, h_val in self.frontier:
                if node in self.visited:
                    continue

                percept           = self.env.get_percept(node)
                action, utility   = self.select_action(percept)
                self.visited.add(node)
                self.steps       += 1
                print(f"  Step {self.steps}: Node={node}  h={h_val}  Utility={utility}  Action={action}  CumulativeUtility={self.total_utility}")

                if action == 'GOAL_REACHED':
                    path = reconstruct_path(self.came_from, node)
                    print(f"  Path found: {path}")
                    print(f"  Total Utility: {self.total_utility}")
                    return path

                for nb in self.env.neighbors(node):
                    if nb not in self.visited:
                        self.came_from[nb] = node
                        next_frontier.append((nb, self.env.h(nb)))

            self.frontier = next_frontier

        print("  Goal not found.")
        return None


# ============================================================
# MAIN – run all 8 combinations
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("  SEARCH ALGORITHMS + AGENTS  (Start=A  Goal=I)")
    print("=" * 60)

    # --- 1. BFS + Simple Reflex ---
    env1   = BFSEnvironment_SimpleReflex(GRAPH, GOAL)
    agent1 = BFSAgent_SimpleReflex(env1, START)
    agent1.run()

    # --- 2. BFS + Utility Based ---
    env2   = BFSEnvironment_Utility(GRAPH, GOAL)
    agent2 = BFSAgent_Utility(env2, START)
    agent2.run()

    # --- 3. Greedy BFS + Simple Reflex ---
    env3   = GreedyEnvironment_SimpleReflex(GRAPH, HEURISTIC, GOAL)
    agent3 = GreedyAgent_SimpleReflex(env3, START)
    agent3.run()

    # --- 4. Greedy BFS + Utility Based ---
    env4   = GreedyEnvironment_Utility(GRAPH, HEURISTIC, GOAL)
    agent4 = GreedyAgent_Utility(env4, START)
    agent4.run()

    # --- 5. A* + Simple Reflex ---
    env5   = AStarEnvironment_SimpleReflex(GRAPH, HEURISTIC, GOAL)
    agent5 = AStarAgent_SimpleReflex(env5, START)
    agent5.run()

    # --- 6. A* + Utility Based ---
    env6   = AStarEnvironment_Utility(GRAPH, HEURISTIC, GOAL)
    agent6 = AStarAgent_Utility(env6, START)
    agent6.run()

    # --- 7. Beam Search + Simple Reflex ---
    env7   = BeamEnvironment_SimpleReflex(GRAPH, HEURISTIC, GOAL, beam_width=2)
    agent7 = BeamAgent_SimpleReflex(env7, START)
    agent7.run()

    # --- 8. Beam Search + Utility Based ---
    env8   = BeamEnvironment_Utility(GRAPH, HEURISTIC, GOAL, beam_width=2)
    agent8 = BeamAgent_Utility(env8, START)
    agent8.run()
