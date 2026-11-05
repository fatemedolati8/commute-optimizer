"""Runs all 4 solvers on one scenario and saves route plots + convergence plot in a folder.
Usage: python run_scenario.py <map.json> <scenario.json> <output_folder>
"""
import os, sys, json, random
from main import build_problem, SOLVER_REGISTRY
from visualization.plot_routes import plot_commute_route
from visualization.plot_metrics import plot_convergence

map_path, scenario_path, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out_dir, exist_ok=True)
cfg = json.load(open("config.json"))
problem = build_problem(map_path, scenario_path, cfg["problem"])

histories = {}
for key, (name, cls, ck) in SOLVER_REGISTRY.items():
    random.seed(42)
    solver = cls(problem, **cfg[ck])
    state, cost = solver.solve()
    histories[name] = solver.history
    print(f"{name:22s} {cost:6.2f} min | {state.format_time()} | {' -> '.join(state.path)}")
    plot_commute_route(problem, state, title=f"{name} Best Route",
                       save_path=os.path.join(out_dir, f"route_{key}.png"))
print("\n### Convergence Statistics")

for name, history in histories.items():
    if not history:
        print(f"\n{name}: Empty history")
        continue

    final_cost = history[-1]

    convergence_step = next(
        (i + 1 for i, cost in enumerate(history)
         if cost <= final_cost + 1e-9),
        None
    )
    improvements = sum(
        1 for i in range(1, len(history))
        if history[i] < history[i - 1] - 1e-9
    )

    print(f"\n{name}")
    print(f"  First recorded cost: {history[0]:.2f}")
    print(f"  Final best cost:     {final_cost:.2f}")
    print(f"  History length:      {len(history)}")
    print(f"  Convergence step:    {convergence_step}")
    print(f"  Improvements:        {improvements}")
plot_convergence(histories, save_path=os.path.join(out_dir, "convergence_comparison.png"), show=False)
print("Saved to", out_dir)