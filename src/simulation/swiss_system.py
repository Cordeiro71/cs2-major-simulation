from __future__ import annotations
import random
import math
from typing import Optional
from ..data.models import Team, Match, MatchPrediction, SimulationResult
from ..prediction.composite_predictor import CompositePredictor


class SwissSystemSimulator:
    def __init__(self, predictor: CompositePredictor, bo_first: int = 1, bo_elim_adv: int = 3):
        self.predictor = predictor
        self.bo_first = bo_first
        self.bo_elim_adv = bo_elim_adv

    def simulate_stage(self, teams: list[Team], advancing: int, num_sims: int = 1000) -> list[SimulationResult]:
        advancement_counts: dict[str, int] = {t.name: 0 for t in teams}
        placement_sums: dict[str, float] = {t.name: 0.0 for t in teams}

        for _ in range(num_sims):
            results = self._simulate_single_swiss(teams, advancing)
            for i, team in enumerate(results):
                advancement_counts[team.name] += 1 if i < advancing else 0
                placement_sums[team.name] += (i + 1)

        sim_results = []
        for team in teams:
            prob = min(1.0, max(0.0, advancement_counts[team.name] / num_sims))
            avg_place = placement_sums[team.name] / num_sims
            variance = prob * (1 - prob) / max(num_sims, 1)
            ci_low = max(0, prob - 1.96 * math.sqrt(max(0, variance)))
            ci_high = min(1, prob + 1.96 * math.sqrt(max(0, variance)))

            sim_results.append(SimulationResult(
                team_name=team.name,
                win_probability=round(prob, 4),
                avg_placement=round(avg_place, 2),
                confidence_interval=(round(ci_low, 4), round(ci_high, 4)),
            ))

        sim_results.sort(key=lambda r: r.win_probability, reverse=True)
        return sim_results

    def _simulate_single_swiss(self, teams: list[Team], advancing: int) -> list[Team]:
        records: dict[str, tuple[int, int]] = {t.name: (0, 0) for t in teams}
        team_lookup = {t.name: t for t in teams}
        advanced: set[str] = set()
        eliminated: set[str] = set()

        for rnd in range(5):
            if len(advanced) >= advancing or len(advanced) + len(eliminated) >= len(teams):
                break

            active = [t.name for t in teams if t.name not in advanced and t.name not in eliminated]
            pools: dict[tuple[int, int], list[str]] = {}
            for name in active:
                rec = records[name]
                pools.setdefault(rec, []).append(name)

            matched = set()
            for pool_key in sorted(pools.keys()):
                pool_teams = [n for n in pools[pool_key] if n not in matched]
                random.shuffle(pool_teams)

                while len(pool_teams) >= 2:
                    t1_name = pool_teams.pop(0)
                    t2_name = pool_teams.pop(0)
                    matched.add(t1_name)
                    matched.add(t2_name)

                    t1 = team_lookup[t1_name]
                    t2 = team_lookup[t2_name]

                    w, l = records[t1_name]
                    is_elim_or_adv = w >= 2 or l >= 2
                    bo_n = self.bo_elim_adv if is_elim_or_adv else self.bo_first

                    pred = self.predictor.predict_match(t1, t2, bo_n=bo_n)
                    winner = t1_name if random.random() < pred.team1_win_prob else t2_name

                    w1, l1 = records[t1_name]
                    w2, l2 = records[t2_name]
                    if winner == t1_name:
                        records[t1_name] = (w1 + 1, l1)
                        records[t2_name] = (w2, l2 + 1)
                    else:
                        records[t1_name] = (w1, l1 + 1)
                        records[t2_name] = (w2 + 1, l2)

                    if records[t1_name][0] >= 3:
                        advanced.add(t1_name)
                    if records[t1_name][1] >= 3:
                        eliminated.add(t1_name)
                    if records[t2_name][0] >= 3:
                        advanced.add(t2_name)
                    if records[t2_name][1] >= 3:
                        eliminated.add(t2_name)

            if len(advanced) >= advancing:
                break

        sorted_teams = sorted(
            teams,
            key=lambda t: (
                t.name in advanced,
                records[t.name][0],
                -records[t.name][1],
                -t.elo,
            ),
            reverse=True,
        )
        return sorted_teams
