# ==============================================================
#  Food Delivery Dispatch System Simulation (3 Visualization Version)
#  Author: ChatGPT Simulation Template
#  Description:
#     Simulates a food delivery system under multiple configurations.
#     Automatically generates performance visualizations for analysis.
# ==============================================================

import simpy
import random
import statistics
import matplotlib.pyplot as plt
import pandas as pd

# -----------------------------
# Simulation Model
# -----------------------------

def food_delivery(env, num_drivers, arrival_rate, service_time_mean, results):
    """Simulate food delivery orders handled by available drivers."""
    driver_resource = simpy.Resource(env, capacity=num_drivers)
    order_id = 0

    while True:
        # Order arrivals follow an exponential (Poisson) process
        interarrival = random.expovariate(arrival_rate)
        yield env.timeout(interarrival)
        order_id += 1
        env.process(handle_order(env, order_id, driver_resource, service_time_mean, results))

def handle_order(env, order_id, driver_resource, service_time_mean, results):
    """Handle an individual food order."""
    arrival_time = env.now
    with driver_resource.request() as req:
        yield req
        wait_time = env.now - arrival_time
        service_time = random.expovariate(1.0 / service_time_mean)
        yield env.timeout(service_time)
        system_time = env.now - arrival_time

        results["wait_times"].append(wait_time)
        results["system_times"].append(system_time)
        results["completed_orders"].append(order_id)

# -----------------------------
# Simulation Runner
# -----------------------------

def run_simulation(num_drivers, arrival_rate, service_mean, sim_duration=8*60):
    """Run one simulation and return metrics."""
    env = simpy.Environment()
    results = {"wait_times": [], "system_times": [], "completed_orders": []}
    env.process(food_delivery(env, num_drivers, arrival_rate, service_mean, results))
    env.run(until=sim_duration)

    avg_wait = statistics.mean(results["wait_times"]) if results["wait_times"] else 0
    avg_system = statistics.mean(results["system_times"]) if results["system_times"] else 0
    throughput = len(results["completed_orders"]) / (sim_duration / 60.0)

    return avg_wait, avg_system, throughput, results

# -----------------------------
# Visualization and Analysis
# -----------------------------

def visualize_summary(df, scenario_results):
    """Generate 3 key performance visualizations."""
    
    # --- 1️⃣ Bar Chart: Average Wait Time ---
    plt.figure(figsize=(8, 5))
    plt.bar(df["scenario"], df["avg_wait_min"], color="skyblue")
    plt.title("Average Customer Wait Time per Scenario")
    plt.xlabel("Scenario")
    plt.ylabel("Wait Time (minutes)")
    plt.xticks(rotation=20, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("1_avg_wait_comparison.png")

    # --- 2️⃣ Bar Chart: Throughput ---
    plt.figure(figsize=(8, 5))
    plt.bar(df["scenario"], df["throughput_per_hr"], color="orange")
    plt.title("Throughput (Orders per Hour) per Scenario")
    plt.xlabel("Scenario")
    plt.ylabel("Orders per hour")
    plt.xticks(rotation=20, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("2_throughput_comparison.png")

    # --- 3️⃣ Histogram: System Time Distribution (for Baseline scenario) ---
    baseline_results = scenario_results["Baseline (5 drivers)"]
    plt.figure(figsize=(8, 5))
    plt.hist(baseline_results["system_times"], bins=30, color="lightgreen", edgecolor="black")
    plt.title("System Time Distribution (Baseline Scenario)")
    plt.xlabel("System time (minutes)")
    plt.ylabel("Number of orders")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("3_system_time_distribution.png")

    print("\n Charts saved as:")
    print(" - 1_avg_wait_comparison.png")
    print(" - 2_throughput_comparison.png")
    print(" - 3_system_time_distribution.png")

# -----------------------------
# Main Simulation Logic
# -----------------------------

def main():
    print("===============================================")
    print("   FOOD DELIVERY DISPATCH SYSTEM SIMULATION    ")
    print("===============================================")

    # --- Define Simulation Scenarios ---
    scenarios = {
        "Baseline (5 drivers)": {"num_drivers": 5, "arrival_rate": 0.1, "service_mean": 30.0},
        "More drivers (8 drivers)": {"num_drivers": 8, "arrival_rate": 0.1, "service_mean": 30.0},
        "Higher demand (5 drivers, 50% more orders)": {"num_drivers": 5, "arrival_rate": 0.15, "service_mean": 30.0},
        "Faster deliveries (5 drivers, faster service)": {"num_drivers": 5, "arrival_rate": 0.1, "service_mean": 20.0}
    }

    results_list = []
    scenario_results = {}

    for scenario, params in scenarios.items():
        print(f"\nRunning scenario: {scenario}")
        avg_wait, avg_system, throughput, results = run_simulation(
            params["num_drivers"], params["arrival_rate"], params["service_mean"]
        )
        scenario_results[scenario] = results
        results_list.append({
            "scenario": scenario,
            "num_drivers": params["num_drivers"],
            "arrival_rate_per_min": params["arrival_rate"],
            "service_mean_min": params["service_mean"],
            "avg_wait_min": round(avg_wait, 3),
            "avg_system_min": round(avg_system, 3),
            "throughput_per_hr": round(throughput, 2)
        })

    # --- Results Table ---
    df = pd.DataFrame(results_list)
    print("\n===== Summary Results =====")
    print(df.to_string(index=False))

    # --- Save and Visualize ---
    df.to_csv("simulation_summary.csv", index=False)
    print("\n Results saved to 'simulation_summary.csv'")

    visualize_summary(df, scenario_results)

if __name__ == "__main__":
    main()


# this is change 01
# this is change 02