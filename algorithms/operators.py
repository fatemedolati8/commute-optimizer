"""
algorithms/operators.py
Defines candidate neighborhood generation and genetic recombination operators.
"""

from typing import List
from core.state import State
from core.problem import CommuteProblem


from collections import deque
from typing import List, Tuple

def _enumerate_replacements(
    problem,
    start: str,
    end: str,
    blocked_nodes: set,
    max_edges: int = 5,
    max_paths: int = 12
) -> List[Tuple[str, ...]]:

    network = problem.network

    if start == end:
        return []

    queue = deque([(start, (start,))])
    results = []

    while queue and len(results) < max_paths:

        current, path = queue.popleft()

        if len(path) - 1 >= max_edges:
            continue

        for neighbor in network.get_neighbors(current):

            if neighbor in path:
                continue

            if neighbor in blocked_nodes and neighbor != end:
                continue

            new_path = path + (neighbor,)

            if neighbor == end:
                results.append(new_path)
            else:
                queue.append((neighbor, new_path))

            if len(results) >= max_paths:
                break

    return results

def get_neighbors(state: State, problem: CommuteProblem) -> List[State]:

    # TODO: Implement neighborhood generation
    neighbors=[]
    visited={state}
    if not problem.is_valid_state(state):
        return neighbors
    valid_times = problem.get_valid_time_domain()

    current_index = min(
        range(len(valid_times)),
        key=lambda i: abs(valid_times[i] - state.departure_time)
    )
    for index in (current_index - 1, current_index + 1):

        if 0 <= index < len(valid_times):

            candidate = State(
                path=state.path,
                departure_time=valid_times[index]
            )

            if candidate not in visited and problem.is_valid_state(candidate):
                visited.add(candidate)
                neighbors.append(candidate)

    path = state.path
    path_length = len(path)

    for i in range(path_length - 1):
        for j in range(i + 1, path_length):

            start = path[i]
            end = path[j]
            blocked = set(path[:i]) | set(path[j + 1:])
            alternatives = _enumerate_replacements(
                problem,
                start,
                end,
                blocked,
                max_edges=5,
                max_paths=12
            )
            original_segment = path[i:j + 1]

            for replacement in alternatives:

                if replacement == original_segment:
                    continue

                new_path = (
                    path[:i] +
                    replacement +
                    path[j + 1:]
                )

                candidate = State(
                    path=new_path,
                    departure_time=state.departure_time
                )

                if candidate not in visited and problem.is_valid_state(candidate):
                    visited.add(candidate)
                    neighbors.append(candidate)
    return neighbors

import random
def crossover(parent1: State, parent2: State, problem: CommuteProblem) -> State:

    # TODO: Implement genetic crossover

    times = problem.get_valid_time_domain()

    p1, p2 = parent1.path, parent2.path
    avg = (parent1.departure_time + parent2.departure_time) / 2.0
    child_time = min(times, key=lambda t: abs(t - avg))

    shared = [n for n in p1[1:-1] if n in p2[1:-1]]
    random.shuffle(shared)
    for node in shared:
        i, j = p1.index(node), p2.index(node)
        child_path = p1[:i + 1] + p2[j + 1:]   
        child = State(child_path, child_time)
        if problem.is_valid_state(child):        
            return child

    base = State(random.choice([p1, p2]), child_time)
    nbrs = get_neighbors(base, problem)
    return random.choice(nbrs) if nbrs else base

def random_state(problem: CommuteProblem) -> State:
    net = problem.network

    def dfs(node, visited):
        if node == problem.destination:
            return [node]
        nbrs = [n for n in net.get_neighbors(node) if n not in visited]
        random.shuffle(nbrs)
        for n in nbrs:
            res = dfs(n, visited | {n})
            if res:
                return [node] + res
        return None

    path = dfs(problem.origin, {problem.origin})
    return State(tuple(path), random.choice(problem.get_valid_time_domain()))
