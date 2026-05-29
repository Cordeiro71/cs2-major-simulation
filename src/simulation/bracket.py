from __future__ import annotations
import random
from ..simulation.swiss_system import SwissSystemSimulator
from ..simulation.single_elimination import SingleEliminationSimulator
from ..prediction.composite_predictor import CompositePredictor
from ..data.models import Team, SimulationResult, MatchPrediction


class BracketSimulator:
    def __init__(self, predictor: CompositePredictor = None):
        self.predictor = predictor or CompositePredictor()
        self.swiss = SwissSystemSimulator(self.predictor)
        self.playoffs = SingleEliminationSimulator(self.predictor)

    def simulate_full_major(
        self,
        teams: list[Team],
        num_sims: int = 1000,
    ) -> dict:
        all_teams = list(teams)
        challenger_teams = all_teams[8:24]
        legends_seed = all_teams[:8]

        challenger_results = self.swiss.simulate_stage(challenger_teams, advancing=8, num_sims=num_sims)

        advancing_names = set()
        if challenger_results:
            for r in challenger_results[:8]:
                advancing_names.add(r.team_name)

        advancing_from_challengers = [t for t in challenger_teams if t.name in advancing_names]
        legend_pool = list(legends_seed) + advancing_from_challengers[:8]
        if len(legend_pool) > 16:
            legend_pool = legend_pool[:16]
        random.shuffle(legend_pool)

        legends_results = self.swiss.simulate_stage(legend_pool, advancing=8, num_sims=num_sims)

        playoff_names = set()
        if legends_results:
            for r in legends_results[:8]:
                playoff_names.add(r.team_name)

        playoff_teams = [t for t in legend_pool if t.name in playoff_names][:8]
        while len(playoff_teams) < 8:
            remaining = [t for t in all_teams if t not in playoff_teams]
            if remaining:
                playoff_teams.append(remaining[0])
            else:
                break

        random.shuffle(playoff_teams)
        playoff_results = self.playoffs.simulate_bracket(playoff_teams, num_sims=num_sims)

        return {
            "challengers": {
                "stage": "Opening Stage (Challengers)",
                "format": "Swiss System",
                "teams_in": 16,
                "teams_advancing": 8,
                "results": challenger_results,
            },
            "legends": {
                "stage": "Elimination Stage (Legends)",
                "format": "Swiss System",
                "teams_in": 16,
                "teams_advancing": 8,
                "results": legends_results,
            },
            "playoffs": {
                "stage": "Playoffs (Champions Stage)",
                "format": "Single Elimination",
                "teams_in": 8,
                "teams_advancing": 1,
                "results": playoff_results,
            },
        }
