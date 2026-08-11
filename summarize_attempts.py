#!/usr/bin/env python3
import sys
from pathlib import Path
from count_crime import analyze_trace  # re-use the function we wrote earlier

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} M_VALUE", file=sys.stderr)
        sys.exit(1)

    m = sys.argv[1]  # e.g. "0.2", "0.05", etc.
    base_dir = Path(".")
    traces_dir = base_dir / "traces"

    out_path = base_dir / f"attempts_{m}.txt"

    with out_path.open("w") as out_f:
        for n in range(1, 401):
            trace_file = traces_dir / f"drop_{m}_seed_{n}_reputation.jsonl"
            if not trace_file.exists():
                # If file is missing, write "0, 0" (or you can choose to skip/raise)
                out_f.write("0, 0\n")
                continue

            attempts, perfect_crimes = analyze_trace(str(trace_file))
            out_f.write(f"{attempts}, {perfect_crimes}\n")

    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()