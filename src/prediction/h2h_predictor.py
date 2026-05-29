from __future__ import annotations
from ..data.models import Team, Match


class HeadToHeadPredictor:
    RECENCY_WEIGHTS = [0.35, 0.25, 0.20, 0.12, 0.08]

    def predict_match(self, team1: Team, team2: Team, h2h_matches: list[Match], bo_n: int = 1) -> float:
        if not h2h_matches:
            return 0.5

        weighted_wins = 0.0
        total_weight = 0.0

        for i, match in enumerate(h2h_matches):
            w_idx = min(i, len(self.RECENCY_WEIGHTS) - 1)
            weight = self.RECENCY_WEIGHTS[w_idx]
            total_weight += weight

            if match.winner and match.winner.name == team1.name:
                weighted_wins += weight
            elif match.is_completed and match.team1_score == match.team2_score:
                weighted_wins += weight * 0.5

        if total_weight == 0:
            return 0.5

        base_prob = weighted_wins / total_weight

        score_diff_factor = 0.0
        for match in h2h_matches[:3]:
            if match.team1.name == team1.name:
                score_diff_factor += (match.team1_score - match.team2_score) * 0.03
            else:
                score_diff_factor += (match.team2_score - match.team1_score) * 0.03

        prob = base_prob + score_diff_factor
        return max(0.05, min(0.95, prob))
