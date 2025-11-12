import pandas as pd
import numpy as np

def generate_synthetic_data(n=500):
    np.random.seed(42)
    data = {
        "hours_worked": np.random.uniform(2, 12, n),
        "sleep_hours": np.random.uniform(4, 10, n),
        "tasks_completed": np.random.randint(1, 15, n),
        "breaks_taken": np.random.randint(0, 8, n),
        "focus_level": np.random.uniform(0.2, 1.0, n)
    }

    df = pd.DataFrame(data)
    
    # Generate productivity labels
    score = (
        0.5 * df["hours_worked"] +
        0.3 * df["tasks_completed"] -
        0.2 * df["breaks_taken"] +
        0.4 * df["focus_level"] * 10
    )
    df["productivity"] = pd.cut(
        score, bins=[0, 25, 45, 100],
        labels=["Low", "Medium", "High"]
    )

    df.to_csv("synthetic_productivity.csv", index=False)
    print("✅ Synthetic data generated: synthetic_productivity.csv")

if __name__ == "__main__":
    generate_synthetic_data()
