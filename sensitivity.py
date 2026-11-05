import json, random, statistics as st
from main import build_problem, SOLVER_REGISTRY

cfg = json.load(open("config.json"))
problem = build_problem("data/maps/metropolis_graph.json",
                        "data/scenarios/crossover_showcase.json", cfg["problem"])
SA = SOLVER_REGISTRY["sa"][1]

print("### Simulated Annealing: effect of cooling_rate (alpha) and initial_temp (T0)")
print("| alpha | T0 | mean f | min f | max f |")
print("|---|---|---|---|---|")
for alpha in (0.5, 0.992, 0.999):
    for T0 in (0.5, 120, 5000):
        costs = []
        for seed in range(15):
            random.seed(seed)
            s = SA(problem, initial_temp=T0, cooling_rate=alpha,
                   min_temp=0.001, max_iterations=3000)
            costs.append(s.solve()[1])
        print(f"| {alpha} | {T0} | {st.mean(costs):.2f} | {min(costs):.2f} | {max(costs):.2f} |")

fp = build_problem("data/maps/downtown_grid.json",
                   "data/scenarios/flat_plateau.json", cfg["problem"])
HC = SOLVER_REGISTRY["hc"][1]
print("\n### Hill Climbing: effect of max_sideways (flat_plateau)")
print("| max_sideways | mean f | max f |")
print("|---|---|---|")
for ms in (0, 5, 100):
    costs = []
    for seed in range(15):
        random.seed(seed)
        costs.append(HC(fp, max_sideways=ms, max_restarts=0).solve()[1])
    print(f"| {ms} | {st.mean(costs):.2f} | {max(costs):.2f} |")