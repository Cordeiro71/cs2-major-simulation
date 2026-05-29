#!/usr/bin/env python3
"""
CS2 Major Simulation Engine
Uses HLTV data and Monte Carlo simulations to predict CS2 Major tournament outcomes.
"""

import sys
import os
import argparse
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data.scraper import HLTVScraper
from src.simulation.monte_carlo import MonteCarloSimulator
from src.simulation.bracket import BracketSimulator
from src.prediction.composite_predictor import CompositePredictor
from src.utils.display import (
    display_simulation_results,
    display_match_prediction,
    display_bracket,
    display_probability_tree,
    display_stage_tree,
)
from src.utils.export import export_results_json, export_results_csv


def main():
    parser = argparse.ArgumentParser(description="CS2 Major Simulation Engine")
    parser.add_argument("--sims", type=int, default=1000, help="Number of Monte Carlo simulations")
    parser.add_argument("--output-dir", type=str, default="/tmp/csdondo/output", help="Output directory")
    parser.add_argument("--matchup", nargs=2, metavar=("TEAM1", "TEAM2"), help="Predict specific matchup")
    parser.add_argument("--export", action="store_true", help="Export results to files")
    parser.add_argument("--quick", action="store_true", help="Quick mode (fewer simulations)")
    args = parser.parse_args()

    num_sims = 100 if args.quick else args.sims

    print("=" * 80)
    print("  CS2 MAJOR SIMULATION ENGINE")
    print("  Powered by HLTV Data & Monte Carlo Methods")
    print("=" * 80)
    print()

    print("[1/4] Loading HLTV team data...")
    scraper = HLTVScraper(use_cached=True)
    data = scraper.get_sample_data()
    teams = data["teams"]
    major = data["major"]
    print(f"       Loaded {len(teams)} teams")
    print()

    print("[2/4] Major Tournament Structure:")
    for stage in major["stages"]:
        print(f"       - {stage['name']}: {stage['format']} ({stage['teams']} teams, {stage['advancing']} advance)")
    print()

    predictor = CompositePredictor()

    if args.matchup:
        team1_name, team2_name = args.matchup
        team1 = next((t for t in teams if t.name.lower() == team1_name.lower()), None)
        team2 = next((t for t in teams if t.name.lower() == team2_name.lower()), None)

        if not team1 or not team2:
            print(f"Error: Team not found. Available teams:")
            for t in teams:
                print(f"  - {t.name}")
            sys.exit(1)

        print(f"[3/4] Predicting matchup: {team1.name} vs {team2.name}")
        h2h = scraper.get_historical_matches(team1, team2)
        pred = predictor.predict_match(team1, team2, h2h_matches=h2h, bo_n=3)
        print(display_match_prediction(pred))
        print()

        pred_bo1 = predictor.predict_match(team1, team2, h2h_matches=h2h, bo_n=1)
        pred_bo5 = predictor.predict_match(team1, team2, h2h_matches=h2h, bo_n=5)
        print(f"  BO1: {team1.name} {pred_bo1.team1_win_prob:.1%} - {team2.name} {pred_bo1.team2_win_prob:.1%}")
        print(f"  BO3: {team1.name} {pred.team1_win_prob:.1%} - {team2.name} {pred.team2_win_prob:.1%}")
        print(f"  BO5: {team1.name} {pred_bo5.team1_win_prob:.1%} - {team2.name} {pred_bo5.team2_win_prob:.1%}")

    else:
        print(f"[3/4] Running {num_sims:,} Monte Carlo simulations...")
        start = time.time()

        simulator = MonteCarloSimulator(predictor)
        results = simulator.run_simulations(teams, num_sims=num_sims)

        elapsed = time.time() - start
        print(f"       Completed in {elapsed:.1f}s ({num_sims / max(elapsed, 0.01):.0f} sims/sec)")
        print()

        print("[4/4] Results:")
        output = display_simulation_results(results)
        print(output)
        print()

        print(display_probability_tree(results))
        print()
        print(display_stage_tree(results))
        print()

        if args.export:
            os.makedirs(args.output_dir, exist_ok=True)
            json_path = export_results_json(results, os.path.join(args.output_dir, "simulation_results.json"))
            csv_path = export_results_csv(results, os.path.join(args.output_dir, "simulation_results.csv"))
            print(f"Exported results to:")
            print(f"  JSON: {json_path}")
            print(f"  CSV:  {csv_path}")

        print()
        print("=" * 80)
        print("  TOP PREDICTIONS SUMMARY")
        print("=" * 80)
        for i, r in enumerate(results["results"][:5], 1):
            champion_prob = r.stage_reach_prob.get("champion", r.win_probability)
            print(f"  #{i} {r.team_name:25s} - Champion: {champion_prob:.1%}")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
