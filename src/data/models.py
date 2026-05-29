from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MapScore:
    team1_rounds: int
    team2_rounds: int
    map_name: str


@dataclass
class Player:
    name: str
    nickname: str
    rating: float = 1.0
    kills_per_round: float = 0.0
    deaths_per_round: float = 0.0
    adr: float = 0.0
    impact: float = 0.0
    maps_played: int = 0


@dataclass
class Team:
    name: str
    hltv_id: int = 0
    ranking: int = 0
    points: float = 0.0
    players: list[Player] = field(default_factory=list)
    win_streak: int = 0
    recent_form: list[str] = field(default_factory=list)
    map_pool: dict[str, float] = field(default_factory=dict)
    elo: float = 1500.0

    @property
    def form_score(self) -> float:
        if not self.recent_form:
            return 0.5
        wins = sum(1 for r in self.recent_form if r == "W")
        return wins / len(self.recent_form)

    @property
    def avg_player_rating(self) -> float:
        if not self.players:
            return 1.0
        return sum(p.rating for p in self.players) / len(self.players)


@dataclass
class Match:
    team1: Team
    team2: Team
    team1_score: int = 0
    team2_score: int = 0
    maps: list[MapScore] = field(default_factory=list)
    date: str = ""
    event: str = ""
    stage: str = ""
    is_completed: bool = False

    @property
    def winner(self) -> Optional[Team]:
        if not self.is_completed:
            return None
        if self.team1_score > self.team2_score:
            return self.team1
        elif self.team2_score > self.team1_score:
            return self.team2
        return None

    @property
    def is_bo1(self) -> bool:
        return self.team1_score + self.team2_score <= 1

    @property
    def is_bo3(self) -> bool:
        return self.team1_score + self.team2_score <= 3

    @property
    def is_bo5(self) -> bool:
        return True


@dataclass
class Tournament:
    name: str
    hltv_id: int = 0
    date: str = ""
    prize_pool: str = ""
    teams: list[Team] = field(default_factory=list)
    stages: list[str] = field(default_factory=list)
    matches: list[Match] = field(default_factory=list)


@dataclass
class SimulationResult:
    team_name: str
    win_probability: float
    avg_placement: float
    stage_reach_prob: dict[str, float] = field(default_factory=dict)
    confidence_interval: tuple[float, float] = (0.0, 0.0)


@dataclass
class MatchPrediction:
    team1: Team
    team2: Team
    team1_win_prob: float
    team2_win_prob: float
    predicted_score: tuple[int, int] = (0, 0)
    confidence: float = 0.0
    factors: dict[str, float] = field(default_factory=dict)
