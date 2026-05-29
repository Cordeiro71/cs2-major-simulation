from __future__ import annotations
import math
from ..data.models import Team, Match


class EloPredictor:
    K_FACTOR = 32
    HOME_ADVANTAGE = 0

    def predict_match(self, team1: Team, team2: Team, bo_n: int = 1) -> float:
        elo_diff = team1.elo - team2.elo + self.HOME_ADVANTAGE
        prob = 1.0 / (1.0 + 10 ** (-elo_diff / 400.0))
        if bo_n > 1:
            prob = self._bo_adjust(prob, bo_n)
        return prob

    def _bo_adjust(self, p: float, bo_n: int) -> float:
        wins_needed = (bo_n + 1) // 2
        return self._series_prob(p, wins_needed, wins_needed)

    def _series_prob(self, p: float, remaining_wins: int, remaining_losses: int, memo: dict = None) -> float:
        if memo is None:
            memo = {}
        key = (remaining_wins, remaining_losses)
        if key in memo:
            return memo[key]
        if remaining_wins == 0:
            return 1.0
        if remaining_losses == 0:
            return 0.0
        result = p * self._series_prob(p, remaining_wins - 1, remaining_losses, memo) + \
                 (1 - p) * self._series_prob(p, remaining_wins, remaining_losses - 1, memo)
        memo[key] = result
        return result

    def update_elo(self, winner: Team, loser: Team, k: float = None) -> tuple[float, float]:
        k = k or self.K_FACTOR
        expected_w = 1.0 / (1.0 + 10 ** ((loser.elo - winner.elo) / 400.0))
        expected_l = 1.0 - expected_w

        new_winner_elo = winner.elo + k * (1.0 - expected_w)
        new_loser_elo = loser.elo + k * (0.0 - expected_l)
        return new_winner_elo, new_loser_elo
