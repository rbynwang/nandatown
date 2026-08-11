#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_overall_attempts(path="overall_attempts.txt"):
    x_vals = []
    y_vals = []
    with Path(path).open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 4:
                continue  # skip malformed lines
            m_str, TA_str, TPC_str, f_str = parts
            x_vals.append(float(m_str))
            y_vals.append(float(f_str))
    return x_vals, y_vals

def main():
    x_data, y_data = load_overall_attempts("overall_attempts.txt")

    plt.figure(figsize=(6, 4))
    plt.scatter(x_data, y_data, color="blue", label="Simulation data")

    # Plot y = x(1 - x)
    x = np.linspace(0.0, 1.0, 400)
    y = x * (1 - x)
    plt.plot(x, y, color="red", label=r"$y = x(1 - x)$")

    plt.xlim(0.0, 1.0)
    plt.ylim(0.0, max(max(y_data), 0.3) * 1.1)

    plt.xlabel("message_drop m")
    plt.ylabel("Fraction of Perfect Crimes f")
    plt.title("Perfect Crimes vs. message_drop")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()