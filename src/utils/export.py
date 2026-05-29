from __future__ import annotations
import json
import csv
import os
from ..data.models import SimulationResult


def export_results_json(results: dict, filepath: str) -> str:
    data = {
        "num_simulations": results["num_simulations"],
        "teams_analyzed": results["teams_analyzed"],
        "results": [
            {
                "rank": i + 1,
                "team": r.team_name,
                "championship_probability": r.win_probability,
                "confidence_interval": list(r.confidence_interval),
                "stage_probabilities": r.stage_reach_prob,
                "avg_placement": r.avg_placement,
            }
            for i, r in enumerate(results["results"])
        ],
    }
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath


def export_results_csv(results: dict, filepath: str) -> str:
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Rank", "Team", "Championship_Prob",
            "CI_Low", "CI_High",
            "Avg_Placement",
            "Champion_Prob", "Final_Prob", "Semifinal_Prob", "Legends_Prob",
        ])
        for i, r in enumerate(results["results"], 1):
            row = [
                i, r.team_name, r.win_probability,
                r.confidence_interval[0], r.confidence_interval[1],
                r.avg_placement,
            ]
            for stage in ["champion", "final", "semifinal", "legends"]:
                row.append(r.stage_reach_prob.get(stage, 0))
            writer.writerow(row)
    return filepath
