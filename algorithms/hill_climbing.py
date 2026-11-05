"""
algorithms/hill_climbing.py
Hill Climbing search with sideways move limits and random restarts.
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
class HillClimbingSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.max_sideways: int = self.params.get("max_sideways", 100)
        self.max_restarts: int = self.params.get("max_restarts", 5)

    def solve(self) -> Tuple[State, float]:

        # TODO: Implement Hill Climbing with sideways moves and restarts
        best_state=None
        best_cost=float("inf")

        for r in range(self.max_restarts+1):
            if r==0:
                curr_state=self.problem.generate_initial_state()
            else:
                curr_state=random_state(self.problem)
            curr_cost=self.problem.evaluate(curr_state)
            sideways=0
            visited={curr_state}
            while True:
                neighbors=get_neighbors(curr_state,self.problem)
                if len(neighbors)<=0:
                    break

                costs_nbrs={}
                min_cost=float("inf")
                min_state=None
                cost_nbr={}
                for n in neighbors:
                    cost_nbr=self.problem.evaluate(n)
                    if cost_nbr<min_cost:
                        min_cost=cost_nbr
                        min_state=n
                    costs_nbrs[n]=cost_nbr

                if min_cost<curr_cost- 1e-9:
                    curr_cost=min_cost
                    curr_state=min_state
                    sideways=0
                else:
                    equal_costs={}
                    for cn in costs_nbrs:
                        if abs(costs_nbrs[cn]-curr_cost)<1e-9 and cn not in visited:
                            equal_costs[cn]=costs_nbrs[cn]

                    if len(equal_costs)>0 and sideways< self.max_sideways:
                        curr_state = next(iter(equal_costs))
                        curr_cost = costs_nbrs[curr_state]
                        sideways+=1
                    else:
                        break
                visited.add(curr_state)
                if curr_cost<best_cost:
                    best_cost=curr_cost
                    best_state=curr_state
                self.history.append(best_cost)
            if curr_cost<best_cost:
                best_cost=curr_cost
                best_state=curr_state
        return best_state,best_cost

