"""
algorithms/hill_climbing.py
Hill Climbing search with sideways move limits and random restarts.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors


class HillClimbingSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.max_sideways: int = self.params.get("max_sideways", 100)
        self.max_restarts: int = self.params.get("max_restarts", 5)

    def solve(self) -> Tuple[State, float]:

        # TODO: Implement Hill Climbing with sideways moves and restarts
        best_state, best_cost = None, float("inf")
        for r in range(self.max_restarts + 1):
            cur = self.problem.generate_initial_state() if r == 0 else random_state(self.problem)
            cur_cost = self.problem.evaluate(cur)
            sideways = 0
            visited = {cur}
            while True:
                nbrs = get_neighbors(cur, self.problem)
                if not nbrs:
                    break
                scored = [(self.problem.evaluate(n), n) for n in nbrs]
                cost, cand = min(scored, key=lambda x: x[0])
                if cost < cur_cost - 1e-9:
                    cur, cur_cost, sideways = cand, cost, 0
                else:
                    flats = [n for c, n in scored
                             if abs(c - cur_cost) < 1e-9 and n not in visited]
                    if flats and sideways < self.max_sideways:
                        cur = flats[0]
                        sideways += 1
                    else:
                        break
                visited.add(cur)
                if cur_cost < best_cost:
                    best_state, best_cost = cur, cur_cost
                self.history.append(best_cost)
            if cur_cost < best_cost:
                best_state, best_cost = cur, cur_cost
        return best_state, best_cost
