"""
algorithms/beam_search.py
Local Beam Search maintaining K parallel candidate states.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors
import random

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

class LocalBeamSearchSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.beam_width: int = self.params.get("beam_width", 5)
        self.max_iterations: int = self.params.get("max_iterations", 150)

    def solve(self) -> Tuple[State, float]:

        # TODO: Implement Local Beam Search
        beam=set()
        beam.add(self.problem.generate_initial_state())
        attempts = 0
        while len(beam) < self.beam_width and attempts < 100 * self.beam_width:
            beam.add(random_state(self.problem))
            attempts += 1
        beam = list(beam)

        best_state=None
        best_cost=float("inf")
        for b in beam:
            cost=self.problem.evaluate(b)
            if cost<best_cost:
                best_cost=cost
                best_state=b
        stall=0

        for i in range(self.max_iterations):
            pool=set(beam)
            for b in beam:
                pool.update(get_neighbors(b,self.problem))

            pool = sorted(pool, key=self.problem.evaluate)
            beam=pool[:self.beam_width]

            best_cost_this_iteration = self.problem.evaluate(beam[0])

            if best_cost_this_iteration<best_cost - 1e-9:
                best_cost=best_cost_this_iteration
                best_state=beam[0]
                stall=0
            else:
                stall+=1

            self.history.append(best_cost)
            if stall>=10:
                break
        return best_state,best_cost

       
