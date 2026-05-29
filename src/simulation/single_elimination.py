from __future__ import annotations
import random
import math
from ..data.models import Team, Match, MatchPrediction, SimulationResult
from ..prediction.composite_predictor import CompositePredictor


class SingleEliminationSimulator:
    def __init__(self, predictor: CompositePredictor, bo_n: int = 3, grand_final_bo: int = 5):
        self.predictor = predictor
        self.bo_n = bo_n
        self.grand_final_bo = grand_final_bo

    def simulate_bracket(self, teams: list[Team], num_sims: int = 1000) -> list[SimulationResult]:
        if len(teams) not in (2, 4, 8, 16):
            teams = teams[:8]

        win_counts: dict[str, int] = {t.name: 0 for t in teams}
        final_counts: dict[str, int] = {t.name: 0 for t in teams}
        semifinal_counts: dict[str, int] = {t.name: 0 for t in teams}
        placement_sums: dict[str, float] = {t.name: 0.0 for t in teams}

        for _ in range(num_sims):
            placements = self._simulate_single_bracket(teams)
            for place, team_name in enumerate(placements):
                placement_sums[team_name] += (place + 1)
                if place == 0:
                    win_counts[team_name] += 1
                if place <= 1:
                    final_counts[team_name] += 1
                if place <= 3:
                    semifinal_counts[team_name] += 1

        sim_results = []
        for team in teams:
            prob = win_counts[team.name] / num_sims
            avg_place = placement_sums[team.name] / num_sims
            ci_low = max(0, prob - 1.96 * math.sqrt(prob * (1 - prob) / num_sims))
            ci_high = min(1, prob + 1.96 * math.sqrt(prob * (1 - prob) / num_sims))

            sim_results.append(SimulationResult(
                team_name=team.name,
                win_probability=round(prob, 4),
                avg_placement=round(avg_place, 2),
                stage_reach_prob={
                    "winner": round(win_counts[team.name] / num_sims, 4),
                    "final": round(final_counts[team.name] / num_sims, 4),
                    "semifinal": round(semifinal_counts[team.name] / num_sims, 4),
                },
                confidence_interval=(round(ci_low, 4), round(ci_high, 4)),
            ))

        sim_results.sort(key=lambda r: r.win_probability, reverse=True)
        return sim_results

    def _simulate_single_bracket(self, teams: list[Team]) -> list[str]:
        round_teams = [t.name for t in teams]
        team_lookup = {t.name: t for t in teams}
        placement: list[str] = []
        round_num = 0

        while len(round_teams) > 1:
            next_round = []
            losers = []
            is_final = len(round_teams) == 2
            bo = self.grand_final_bo if is_final else self.bo_n

            for i in range(0, len(round_teams), 2):
                if i + 1 >= len(round_teams):
                    next_round.append(round_teams[i])
                    continue

                t1 = team_lookup[round_teams[i]]
                t2 = team_lookup[round_teams[i + 1]]

                pred = self.predictor.predict_match(t1, t2, bo_n=bo)
                winner = round_teams[i] if random.random() < pred.team1_win_prob else round_teams[i + 1]

                next_round.append(winner)
                loser = round_teams[i] if winner != round_teams[i] else round_teams[i + 1]
                losers.append(loser)

            if len(round_teams) > 2:
                losers.sort(key=lambda n: -team_lookup[n].elo)
                placement.extend(losers)

            round_teams = next_round
            round_num += 1

        placement.insert(0, round_teams[0])
        return placement
