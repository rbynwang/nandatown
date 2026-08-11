#!/usr/bin/env python3
import sys
import json
import re
from collections import defaultdict

def analyze_trace(filename: str):
    attempts = 0  # malicious cheat attempts against honest agents
    cheats = {}   # corr_id -> info about that cheat attempt

    # For reports:
    # attack_key = (round_str, cheater_id, victim_id)
    reports_by_attack = defaultdict(list)    # attack_key -> [report_corr_ids]
    report_outcome = {}                      # report_corr_id -> "receive" or "dropped"

    malicious_re = re.compile(r"^malicious-\d+$")
    honest_re = re.compile(r"^honest-\d+$")

    with open(filename, "r") as f:
        for line in f:
            event = json.loads(line)
            kind = event.get("kind")
            agent = event.get("agent")
            msg = event.get("msg", "")
            corr = event.get("corr")

            # ------- CHEAT SENDS (Attempts) -------
            if (
                kind == "send"
                and malicious_re.match(agent or "")
                and msg.startswith("cheat:")
            ):
                # msg format: "cheat:ROUND:CHEATER_ID"
                parts = msg.split(":")
                if len(parts) >= 3:
                    _, round_str, cheater_id = parts[:3]
                else:
                    continue  # malformed, skip

                victim = event.get("to")
                if not honest_re.match(victim or ""):
                    # We only count Attempts where target is an honest agent
                    continue

                attempts += 1
                cheats[corr] = {
                    "round": round_str,
                    "cheater": cheater_id,
                    "victim": victim,
                    "delivered": False,  # will be set true if victim receives the cheat
                }

            # ------- CHEAT RECEIVE / DROPPED (success of cheat) -------
            if (
                kind in ("receive", "dropped")
                and msg.startswith("cheat:")
                and honest_re.match(event.get("agent", ""))   # victim is honest
                and malicious_re.match(event.get("from", "")) # sender is malicious
            ):
                info = cheats.get(corr)
                if info is not None:
                    # Cheat successful iff the victim actually "receive"s it.
                    if kind == "receive":
                        info["delivered"] = True

            # ------- REPORT SENDS (honest agents reporting) -------
            if (
                kind == "send"
                and honest_re.match(agent or "")
                and msg.startswith("report:")
            ):
                # msg format: "report:ROUND:CHEATER_ID:...”
                parts = msg.split(":")
                if len(parts) >= 3:
                    _, round_str, cheater_id = parts[:3]
                else:
                    continue  # malformed, skip

                victim = agent  # reporter is the victim in this model
                attack_key = (round_str, cheater_id, victim)
                reports_by_attack[attack_key].append(corr)

            # ------- REPORT RECEIVE / DROPPED (observer outcome) -------
            if (
                kind in ("receive", "dropped")
                and event.get("agent") == "observer-0"
                and msg.startswith("report:")
            ):
                report_outcome[corr] = kind  # "receive" or "dropped"

    # ------- Count Perfect Crimes -------
    perfect_crimes = 0

    for info in cheats.values():
        if not info["delivered"]:
            # Cheat never reached the victim → not a Perfect Crime
            continue

        attack_key = (info["round"], info["cheater"], info["victim"])
        report_corrs = reports_by_attack.get(attack_key, [])

        # A successful report exists iff any corresponding report is *received* by observer-0
        has_successful_report = any(
            report_outcome.get(rc) == "receive" for rc in report_corrs
        )

        if not has_successful_report:
            perfect_crimes += 1

    return attempts, perfect_crimes


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} TRACE_FILE.jsonl", file=sys.stderr)
        sys.exit(1)

    fname = sys.argv[1]
    attempts, perfect = analyze_trace(fname)
    print(f"Attempts: {attempts}")
    print(f"Perfect crimes: {perfect}")