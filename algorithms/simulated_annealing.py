"""
algorithms/simulated_annealing.py
Stochastic optimization governed by a temperature schedule.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors
import math
import random

class SimulatedAnnealingSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.initial_temp: float = self.params.get("initial_temp", 100.0)
        self.cooling_rate: float = self.params.get("cooling_rate", 0.995)
        self.min_temp: float = self.params.get("min_temp", 1e-3)
        self.max_iterations: int = self.params.get("max_iterations", 2000)

    def solve(self) -> Tuple[State, float]:

        # TODO: Implement Simulated Annealing
        curr_state=self.problem.generate_initial_state()
        curr_cost=self.problem.evaluate(curr_state)
        best_state=curr_state
        best_cost=curr_cost

        T=self.initial_temp

        for i in range(self.max_iterations):
            if T<self.min_temp:
                break
            neighbors=get_neighbors(curr_state,self.problem)

            if len(neighbors)<=0:
                break

            next_state=random.choice(neighbors)
            delta_E=self.problem.evaluate(next_state)-curr_cost

            if delta_E<0 or random.random()<math.exp(-delta_E/T):
                curr_state=next_state
                curr_cost=curr_cost+delta_E

                if curr_cost<best_cost:
                    best_cost=curr_cost
                    best_state=curr_state
            self.history.append(best_cost)
            T *=self.cooling_rate
        return best_state,best_cost
