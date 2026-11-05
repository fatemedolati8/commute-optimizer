"""
algorithms/genetic_algorithm.py
Population-based optimization using selection, recombination, and mutation.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors, crossover
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


class GeneticAlgorithmSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.population_size: int = self.params.get("population_size", 30)
        self.generations: int = self.params.get("generations", 100)
        self.crossover_rate: float = self.params.get("crossover_rate", 0.8)
        self.mutation_rate: float = self.params.get("mutation_rate", 0.2)
        self.elitism: int = self.params.get("elitism", 2)
        self.tournament_size = self.params.get("tournament_size", 3)

    def solve(self) -> Tuple[State, float]:

        # TODO: Implement Genetic Algorithm
        population=[]
        population.append(self.problem.generate_initial_state())
        for i in range(self.population_size-1):
            population.append(random_state(self.problem))

        best_state=None
        best_cost=float("inf")
        for p in population:
            cost=self.problem.evaluate(p)
            if cost<best_cost:
                best_cost=cost
                best_state=p

        def tournament(pop, tournament_size):
            samples=random.sample(pop,tournament_size)
            min_cost=float("inf")
            min_state=None
            for s in samples:
                cost=self.problem.evaluate(s)
                if cost <min_cost:
                    min_cost=cost
                    min_state=s
            return min_state


        for i in range(self.generations):
            sorted_pop=sorted(population,key=self.problem.evaluate)

            new_pop=sorted_pop[:self.elitism]
            while( len(new_pop)<self.population_size ):
                parent1=tournament(population,self.tournament_size)
                parent2=tournament(population,self.tournament_size)

                if random.random() <self.crossover_rate:
                    child=crossover(parent1,parent2,self.problem)

                else:
                    child=parent1

                if random.random() < self.mutation_rate:
                    nbrs=get_neighbors(child,self.problem)
                    if len(nbrs)>0:
                        child=random.choice(nbrs)

                new_pop.append(child)
            population=new_pop

            min_cost=float("inf")
            min_state=None
            for p in population:
                cost=self.problem.evaluate(p)
                if cost<min_cost:
                    min_cost=cost
                    min_state=p

            if min_cost<best_cost:
                best_cost=min_cost
                best_state=min_state
            self.history.append(best_cost)

        return best_state,best_cost


            




