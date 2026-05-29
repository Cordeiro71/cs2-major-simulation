from __future__ import annotations
import urllib.request
import urllib.parse
import json
import re
import time
import logging
from html.parser import HTMLParser
from .models import Team, Match, Player, MapScore, Tournament

logger = logging.getLogger(__name__)

HLTV_BASE = "https://www.hltv.org"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

MAJOR_TEAMS_2025 = [
    {"name": "Team Spirit", "ranking": 1, "points": 950, "elo": 1850},
    {"name": "Vitality", "ranking": 2, "points": 880, "elo": 1820},
    {"name": "MOUZ", "ranking": 3, "points": 820, "elo": 1790},
    {"name": "Natus Vincere", "ranking": 4, "points": 780, "elo": 1770},
    {"name": "FaZe Clan", "ranking": 5, "points": 740, "elo": 1750},
    {"name": "G2 Esports", "ranking": 6, "points": 700, "elo": 1730},
    {"name": "Astralis", "ranking": 7, "points": 660, "elo": 1710},
    {"name": "Heroic", "ranking": 8, "points": 620, "elo": 1690},
    {"name": "Complexity", "ranking": 9, "points": 580, "elo": 1670},
    {"name": "Liquid", "ranking": 10, "points": 550, "elo": 1655},
    {"name": "FURIA", "ranking": 11, "points": 520, "elo": 1640},
    {"name": " paiN Gaming", "ranking": 12, "points": 490, "elo": 1625},
    {"name": "Cloud9", "ranking": 13, "points": 460, "elo": 1610},
    {"name": "Eternal Fire", "ranking": 14, "points": 430, "elo": 1595},
    {"name": "The MongolZ", "ranking": 15, "points": 400, "elo": 1580},
    {"name": "Wildcard", "ranking": 16, "points": 370, "elo": 1565},
    {"name": "Imperial", "ranking": 17, "points": 340, "elo": 1550},
    {"name": "MIBR", "ranking": 18, "points": 310, "elo": 1535},
    {"name": "BIG", "ranking": 19, "points": 280, "elo": 1520},
    {"name": "Monte", "ranking": 20, "points": 250, "elo": 1505},
    {"name": "Ninjas in Pyjamas", "ranking": 21, "points": 230, "elo": 1495},
    {"name": "3DMAX", "ranking": 22, "points": 210, "elo": 1480},
    {"name": "SAW", "ranking": 23, "points": 190, "elo": 1465},
    {"name": "Virtus.pro", "ranking": 24, "points": 170, "elo": 1450},
]

MAP_POOL = ["Mirage", "Inferno", "Nuke", "Overpass", "Anubis", "Dust2", "Ancient"]

DEFAULT_MAP_STRENGTHS = {
    "Mirage": 0.55, "Inferno": 0.52, "Nuke": 0.48,
    "Overpass": 0.50, "Anubis": 0.53, "Dust2": 0.54, "Ancient": 0.49,
}


class HLTVScraper:
    def __init__(self, use_cached: bool = True, cache_dir: str = ""):
        self.use_cached = use_cached
        self.cache_dir = cache_dir
        self._teams: list[Team] = []
        self._matches: list[Match] = []
        self._h2h_data: dict[tuple[str, str], list[dict]] = {}

    def _fetch_page(self, url: str) -> str:
        if self.use_cached:
            raise RuntimeError("Live scraping disabled; use cached/sample data")
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")

    def get_major_teams(self) -> list[Team]:
        if self._teams:
            return self._teams

        for td in MAJOR_TEAMS_2025:
            team = Team(
                name=td["name"].strip(),
                ranking=td["ranking"],
                points=td["points"],
                elo=td["elo"],
                recent_form=self._generate_form(td["ranking"]),
                map_pool={m: round(DEFAULT_MAP_STRENGTHS[m] + (20 - td["ranking"]) * 0.008 + 0.02 * (hash(td["name"] + m) % 10 - 5) / 10, 3) for m in MAP_POOL},
                players=self._generate_players(td["name"]),
            )
            self._teams.append(team)
        return self._teams

    def _generate_form(self, ranking: int) -> list[str]:
        base_win_rate = max(0.3, 0.85 - (ranking - 1) * 0.025)
        import random
        rng = random.Random(hash(str(ranking)) + 42)
        form = []
        for _ in range(5):
            form.append("W" if rng.random() < base_win_rate else "L")
        return form

    def _generate_players(self, team_name: str) -> list[Player]:
        import random
        rng = random.Random(hash(team_name))
        players = []
        for i in range(5):
            rating = round(0.85 + rng.random() * 0.45, 2)
            players.append(Player(
                name=f"Player {i+1}",
                nickname=f"{team_name[:3].upper()}{i+1}",
                rating=rating,
                kills_per_round=round(0.55 + rng.random() * 0.25, 2),
                deaths_per_round=round(0.55 + rng.random() * 0.15, 2),
                adr=round(65 + rng.random() * 35, 1),
                impact=round(0.8 + rng.random() * 0.5, 2),
                maps_played=50 + rng.randint(0, 200),
            ))
        return players

    def get_historical_matches(self, team1: Team, team2: Team) -> list[Match]:
        key = tuple(sorted([team1.name, team2.name]))
        if key in self._h2h_data:
            return self._h2h_data[key]

        import random
        rng = random.Random(hash(key[0] + key[1]))
        matches = []
        num_matches = rng.randint(1, 8)

        for _ in range(num_matches):
            t1_stronger = team1.elo > team2.elo
            if t1_stronger:
                t1_wins = rng.random() < 0.55
            else:
                t1_wins = rng.random() < 0.45

            if t1_wins:
                score = (2, 1) if rng.random() < 0.6 else (2, 0)
            else:
                score = (1, 2) if rng.random() < 0.6 else (0, 2)

            match = Match(
                team1=team1, team2=team2,
                team1_score=score[0], team2_score=score[1],
                date=f"2025-{rng.randint(1,5):02d}-{rng.randint(1,28):02d}",
                event="CS2 Tournament",
                is_completed=True,
            )
            matches.append(match)

        self._h2h_data[key] = matches
        return matches

    def get_major_structure(self) -> dict:
        return {
            "name": "CS2 Major Copenhagen 2025",
            "stages": [
                {
                    "name": "Opening Stage (Challengers)",
                    "format": "swiss",
                    "teams": 16,
                    "advancing": 8,
                    "type": "bo1_bo3",
                },
                {
                    "name": "Elimination Stage (Legends)",
                    "format": "swiss",
                    "teams": 16,
                    "advancing": 8,
                    "type": "bo1_bo3",
                },
                {
                    "name": "Playoffs (Champions)",
                    "format": "single_elimination",
                    "teams": 8,
                    "advancing": 1,
                    "type": "bo3_bo5",
                },
            ],
        }

    def get_sample_data(self) -> dict:
        teams = self.get_major_teams()
        return {
            "teams": teams,
            "major": self.get_major_structure(),
        }
