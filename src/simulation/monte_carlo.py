from __future__ import annotations
import random
import math
from ..data.models import Team, SimulationResult, MatchPrediction
from ..prediction.composite_predictor import CompositePredictor
from ..simulation.bracket import BracketSimulator


class MonteCarloSimulator:
    def __init__(self, predictor: CompositePredictor = None):
        self.predictor = predictor or CompositePredictor()
        self.bracket = BracketSimulator(self.predictor)

    def run_simulations(
        self,
        teams: list[Team],
        num_sims: int = 10000,
        stages: list[str] = None,
    ) -> dict:
        stages = stages or ["challengers", "legends", "playoffs"]
        num_sims = min(num_sims, 50000)
        num_sims = max(num_sims, 100)

        all_names = [t.name for t in teams]
        champion_counts: dict[str, int] = {n: 0 for n in all_names}
        final_counts: dict[str, int] = {n: 0 for n in all_names}
        semi_counts: dict[str, int] = {n: 0 for n in all_names}
        legends_counts: dict[str, int] = {n: 0 for n in all_names}
        challenger_counts: dict[str, int] = {n: 0 for n in all_names}

        major_result = self.bracket.simulate_full_major(teams, num_sims=num_sims)

        for sr in major_result.get("challengers", {}).get("results", []):
            challenger_counts[sr.team_name] = int(sr.win_probability * num_sims)

        for sr in major_result.get("legends", {}).get("results", []):
            legends_counts[sr.team_name] = int(sr.win_probability * num_sims)

        for sr in major_result.get("playoffs", {}).get("results", []):
            champion_counts[sr.team_name] = int(sr.stage_reach_prob.get("winner", 0) * num_sims)
            final_counts[sr.team_name] = int(sr.stage_reach_prob.get("final", 0) * num_sims)
            semi_counts[sr.team_name] = int(sr.stage_reach_prob.get("semifinal", 0) * num_sims)

        total = num_sims
        results = []
        for team in teams:
            win_prob = min(1.0, max(0.0, champion_counts[team.name] / total))
            final_prob = min(1.0, max(0.0, final_counts[team.name] / total))
            semi_prob = min(1.0, max(0.0, semi_counts[team.name] / total))
            legend_prob = min(1.0, max(0.0, legends_counts[team.name] / total))

            variance = win_prob * (1 - win_prob) / max(total, 1)
            ci_low = max(0, win_prob - 1.96 * math.sqrt(max(0, variance)))
            ci_high = min(1, win_prob + 1.96 * math.sqrt(max(0, variance)))

            results.append(SimulationResult(
                team_name=team.name,
                win_probability=round(win_prob, 4),
                avg_placement=0,
                stage_reach_prob={
                    "champion": round(win_prob, 4),
                    "final": round(final_prob, 4),
                    "semifinal": round(semi_prob, 4),
                    "legends": round(legend_prob, 4),
                    "challengers": round(min(1.0, max(0.0, challenger_counts[team.name] / total)), 4),
                },
                confidence_interval=(round(ci_low, 4), round(ci_high, 4)),
            ))

        results.sort(key=lambda r: r.win_probability, reverse=True)
        for i, r in enumerate(results):
            r.avg_placement = round(i + 1, 1)

        return {
            "num_simulations": total,
            "teams_analyzed": len(teams),
            "results": results,
        }

    def predict_matchup(self, team1: Team, team2: Team, bo_n: int = 3) -> MatchPrediction:
        return self.predictor.predict_match(team1, team2, bo_n=bo_n)
