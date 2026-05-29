from __future__ import annotations
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from ..data.scraper import HLTVScraper
from ..simulation.monte_carlo import MonteCarloSimulator
from ..prediction.composite_predictor import CompositePredictor
from ..simulation.bracket import BracketSimulator

_scraper: HLTVScraper = None
_predictor: CompositePredictor = None


def get_scraper():
    global _scraper
    if _scraper is None:
        _scraper = HLTVScraper(use_cached=True)
    return _scraper


def get_predictor():
    global _predictor
    if _predictor is None:
        _predictor = CompositePredictor()
    return _predictor


def run_simulation(num_sims: int = 1000) -> dict:
    scraper = get_scraper()
    predictor = get_predictor()
    data = scraper.get_sample_data()
    teams = data["teams"]

    simulator = MonteCarloSimulator(predictor)
    results = simulator.run_simulations(teams, num_sims=num_sims)

    bracket = BracketSimulator(predictor)
    bracket_result = bracket.simulate_full_major(teams, num_sims=min(num_sims, 1000))

    return {
        "simulation": _serialize_results(results),
        "bracket": _serialize_bracket(bracket_result),
        "teams": _serialize_teams(teams),
        "num_sims": num_sims,
    }


def predict_matchup(team1_name: str, team2_name: str, bo_n: int = 3) -> dict:
    scraper = get_scraper()
    predictor = get_predictor()
    data = scraper.get_sample_data()
    teams = data["teams"]

    team1 = next((t for t in teams if t.name.lower() == team1_name.lower()), None)
    team2 = next((t for t in teams if t.name.lower() == team2_name.lower()), None)

    if not team1 or not team2:
        return {"error": f"Team not found: {team1_name if not team1 else team2_name}"}

    h2h = scraper.get_historical_matches(team1, team2)
    pred = predictor.predict_match(team1, team2, h2h_matches=h2h, bo_n=bo_n)

    return {
        "team1": {"name": team1.name, "ranking": team1.ranking, "elo": team1.elo},
        "team2": {"name": team2.name, "ranking": team2.ranking, "elo": team2.elo},
        "team1_win_prob": pred.team1_win_prob,
        "team2_win_prob": pred.team2_win_prob,
        "predicted_score": list(pred.predicted_score),
        "confidence": pred.confidence,
        "factors": pred.factors,
        "bo_n": bo_n,
    }


def get_teams() -> list[dict]:
    scraper = get_scraper()
    data = scraper.get_sample_data()
    return _serialize_teams(data["teams"])


def _serialize_teams(teams) -> list[dict]:
    result = []
    for t in teams:
        result.append({
            "name": t.name,
            "ranking": t.ranking,
            "points": t.points,
            "elo": t.elo,
            "form_score": t.form_score,
            "avg_player_rating": t.avg_player_rating,
            "recent_form": t.recent_form,
            "map_pool": t.map_pool,
            "players": [{"nickname": p.nickname, "rating": p.rating, "adr": p.adr} for p in t.players],
        })
    return result


def _serialize_results(results: dict) -> dict:
    return {
        "num_simulations": results["num_simulations"],
        "teams_analyzed": results["teams_analyzed"],
        "results": [
            {
                "team_name": r.team_name,
                "win_probability": r.win_probability,
                "avg_placement": r.avg_placement,
                "stage_reach_prob": r.stage_reach_prob,
                "confidence_interval": list(r.confidence_interval),
            }
            for r in results["results"]
        ],
    }


def _serialize_bracket(bracket: dict) -> dict:
    output = {}
    for stage_key in ("challengers", "legends", "playoffs"):
        stage = bracket.get(stage_key, {})
        output[stage_key] = {
            "stage": stage.get("stage", ""),
            "format": stage.get("format", ""),
            "teams_in": stage.get("teams_in", 0),
            "teams_advancing": stage.get("teams_advancing", 0),
            "results": [
                {
                    "team_name": r.team_name,
                    "win_probability": r.win_probability,
                    "stage_reach_prob": r.stage_reach_prob,
                }
                for r in stage.get("results", [])
            ],
        }
    return output
