from __future__ import annotations
from .elo_predictor import EloPredictor
from .h2h_predictor import HeadToHeadPredictor
from ..data.models import Team, Match, MatchPrediction


class CompositePredictor:
    def __init__(self):
        self.elo = EloPredictor()
        self.h2h = HeadToHeadPredictor()
        self.weights = {
            "elo": 0.40,
            "ranking": 0.15,
            "form": 0.15,
            "map_pool": 0.10,
            "h2h": 0.15,
            "player_rating": 0.05,
        }

    def predict_match(self, team1: Team, team2: Team, h2h_matches: list[Match] = None, bo_n: int = 1) -> MatchPrediction:
        h2h_matches = h2h_matches or []
        factors = {}

        factors["elo"] = self.elo.predict_match(team1, team2, bo_n=bo_n)

        rank_diff = team2.ranking - team1.ranking
        factors["ranking"] = 0.5 + rank_diff * 0.02
        factors["ranking"] = max(0.1, min(0.9, factors["ranking"]))

        factors["form"] = 0.5 + (team1.form_score - team2.form_score) * 0.5
        factors["form"] = max(0.1, min(0.9, factors["form"]))

        t1_map_avg = sum(team1.map_pool.values()) / len(team1.map_pool) if team1.map_pool else 0.5
        t2_map_avg = sum(team2.map_pool.values()) / len(team2.map_pool) if team2.map_pool else 0.5
        factors["map_pool"] = 0.5 + (t1_map_avg - t2_map_avg)
        factors["map_pool"] = max(0.1, min(0.9, factors["map_pool"]))

        if h2h_matches:
            factors["h2h"] = self.h2h.predict_match(team1, team2, h2h_matches, bo_n)
        else:
            factors["h2h"] = 0.5

        factors["player_rating"] = 0.5 + (team1.avg_player_rating - team2.avg_player_rating) * 0.5
        factors["player_rating"] = max(0.1, min(0.9, factors["player_rating"]))

        team1_prob = sum(
            self.weights[k] * factors[k]
            for k in self.weights
        )
        team1_prob = max(0.02, min(0.98, team1_prob))
        team2_prob = 1.0 - team1_prob

        if bo_n >= 3:
            wins_needed = (bo_n + 1) // 2
            team1_prob = self._series_prob(team1_prob, wins_needed, wins_needed)

        confidence = self._calc_confidence(factors, h2h_matches)

        pred_score = self._predict_score(team1_prob, bo_n)

        return MatchPrediction(
            team1=team1,
            team2=team2,
            team1_win_prob=round(team1_prob, 4),
            team2_win_prob=round(1 - team1_prob, 4),
            predicted_score=pred_score,
            confidence=round(confidence, 4),
            factors={k: round(v, 4) for k, v in factors.items()},
        )

    def _series_prob(self, p: float, rw: int, rl: int, memo: dict = None) -> float:
        if memo is None:
            memo = {}
        key = (rw, rl)
        if key in memo:
            return memo[key]
        if rw == 0:
            return 1.0
        if rl == 0:
            return 0.0
        result = p * self._series_prob(p, rw - 1, rl, memo) + \
                 (1 - p) * self._series_prob(p, rw, rl - 1, memo)
        memo[key] = result
        return result

    def _predict_score(self, team1_prob: float, bo_n: int) -> tuple[int, int]:
        wins_needed = (bo_n + 1) // 2 if bo_n > 1 else 1
        if team1_prob > 0.65:
            return (wins_needed, max(0, wins_needed - 2))
        elif team1_prob > 0.5:
            return (wins_needed, wins_needed - 1)
        elif team1_prob > 0.35:
            return (wins_needed - 1, wins_needed)
        else:
            return (max(0, wins_needed - 2), wins_needed)

    def _calc_confidence(self, factors: dict, h2h_matches: list) -> float:
        spread = max(factors.values()) - min(factors.values())
        base = min(0.5 + spread * 0.3, 0.85)
        if not h2h_matches:
            base *= 0.85
        return base
