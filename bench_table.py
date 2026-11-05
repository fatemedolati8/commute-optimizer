import json, random, time, statistics as st
from main import build_problem, SOLVER_REGISTRY

cfg = json.load(open("config.json"))
SEEDS = range(10)
CASES = [
    ("default (toy + rush_hour)", "data/maps/toy_graph.json", "data/scenarios/rush_hour.json"),
    ("crossover_showcase", "data/maps/metropolis_graph.json", "data/scenarios/crossover_showcase.json"),
    ("flat_plateau", "data/maps/downtown_grid.json", "data/scenarios/flat_plateau.json"),
    ("dual_peak_rush_hour",
    "data/maps/metropolis_graph.json",
    "data/scenarios/dual_peak_rush_hour.json"),

("cascading_gridlock",
 "data/maps/metropolis_graph.json",
 "data/scenarios/cascading_gridlock.json"),
]

for title, mp, sc in CASES:
    problem = build_problem(mp, sc, cfg["problem"])
    print(f"\n### {title}")
    print("| Algorithm | best f(x*) | mean f(x*) | t* | runtime (s) | steps to converge | path |")
    print("|---|---|---|---|---|---|---|")
    for key, (name, cls, ck) in SOLVER_REGISTRY.items():
        costs, times, steps, best = [], [], [], None
        for seed in SEEDS:
            random.seed(seed)
            solver = cls(problem, **cfg[ck])
            t0 = time.perf_counter()
            state, cost = solver.solve()
            times.append(time.perf_counter() - t0)
            costs.append(cost)
            h = solver.history
            steps.append(next(i for i, x in enumerate(h, 1) if x <= h[-1] + 1e-9))
            if best is None or cost < best[1]:
                best = (state, cost)
        print(f"| {name} | {min(costs):.2f} | {st.mean(costs):.2f} | {best[0].format_time()} | "
              f"{st.mean(times):.3f} | {st.mean(steps):.0f} | {' -> '.join(best[0].path)} |")