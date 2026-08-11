#!/usr/bin/env python3
from pathlib import Path

def main():
    base_dir = Path(".")
    out_path = base_dir / "overall_attempts.txt"

    m_values = [round(0.05 * i, 2) for i in range(0, 20)]  # 0.0, 0.05, ..., 0.95

    with out_path.open("w") as out_f:
        for m in m_values:
            m_str = f"{m:.2f}".rstrip("0").rstrip(".") if m != 0 else "0"
            attempts_file = base_dir / f"attempts_{m_str}.txt"

            TA = 0  # total Attempts
            TPC = 0 # total Perfect Crimes

            with attempts_file.open() as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # each line: "A, PC"
                    parts = [x.strip() for x in line.split(",")]
                    if len(parts) != 2:
                        continue
                    A = int(parts[0])
                    PC = int(parts[1])
                    TA += A
                    TPC += PC

            if TA == 0:
                frac = 0.0
            else:
                frac = TPC / TA

            f_str = f"{frac:.3f}"
            out_f.write(f"{m_str}, {TA}, {TPC}, {f_str}\n")

    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()