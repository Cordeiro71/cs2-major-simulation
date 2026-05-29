# CS2 Major Simulation Engine (CSDONDO)

A Python-based Monte Carlo simulation engine that predicts CS2 Major tournament outcomes using HLTV data (rankings, match history, player stats).

## Features

- **HLTV Data Integration**: Team rankings, Elo ratings, map pool strengths, player ratings, head-to-head records
- **Monte Carlo Simulations**: Run up to 50,000 simulations for statistically significant predictions
- **All Major Stages**: Swiss system (Challengers/Legends) + Single Elimination (Champions/Playoffs)
- **Correct Tournament Structure**: Top 8 seeds go directly to Legends; Challengers has seeds 9-24
- **Composite Prediction Model**: Weighted factors including Elo, ranking, form, map pool, H2H, player ratings
- **Matchup Predictions**: BO1/BO3/BO5 win probabilities with confidence intervals
- **Probability Tree**: Visual bracket showing most likely playoff matchups and champion
- **Stage Advancement Tree**: Probability of each team reaching each stage
- **Web UI**: Full-featured dark-themed web interface with simulation controls, bracket tree, matchup predictor, and team cards
- **Export**: JSON and CSV output for further analysis

## Project Structure

```
csdondo/
├── main.py                          # CLI entry point
├── web.py                           # Web UI server (opens browser)
├── src/
│   ├── data/
│   │   ├── models.py                # Team, Match, Player, SimulationResult dataclasses
│   │   └── scraper.py               # HLTV data ingestion (cached + live scraping)
│   ├── simulation/
│   │   ├── monte_carlo.py           # Monte Carlo simulation orchestrator
│   │   ├── bracket.py               # Full Major bracket simulation
│   │   ├── swiss_system.py          # Swiss system stage simulator
│   │   └── single_elimination.py    # Single elimination bracket simulator
│   ├── prediction/
│   │   ├── elo_predictor.py         # Elo-based win probability
│   │   ├── h2h_predictor.py         # Head-to-head history predictor
│   │   └── composite_predictor.py   # Weighted multi-factor predictor
│   ├── utils/
│   │   ├── display.py               # Terminal output + probability tree visualization
│   │   └── export.py                # JSON/CSV export
│   └── web/
│       ├── server.py                # Web API endpoints
│       └── html_template.py         # Full HTML/CSS/JS UI
└── output/                          # Generated simulation results
```

## Usage

### Web UI (Recommended)

```bash
python3 web.py
```

Opens a browser with the full UI featuring:
- **Simulacao**: Run simulations with adjustable count, view results table
- **Arvore de Probabilidades**: Visual playoff bracket tree with win probabilities
- **Avanco por Estagio**: Stacked bar chart of each team's stage-by-stage advancement
- **Preditor de Matchup**: Select any two teams, choose BO1/BO3/BO5, see prediction factors
- **Times**: Browse all teams with rankings, form, map pool strengths, player ratings

### CLI - Full Major Simulation

```bash
python3 main.py --sims 1000 --export
python3 main.py --quick              # Quick mode (100 sims)
python3 main.py --sims 5000          # High accuracy mode
```

### CLI - Specific Matchup Prediction

```bash
python3 main.py --matchup "Vitality" "Natus Vincere"
python3 main.py --matchup "Team Spirit" "MOUZ"
```

## Tournament Structure

The Major follows the correct CS2 format:

1. **Challengers Stage** (Opening): 16 teams (seeds 9-24), Swiss system, top 8 advance
2. **Legends Stage** (Elimination): 16 teams (8 direct seeds + 8 from Challengers), Swiss system, top 8 advance
3. **Champions Stage** (Playoffs): 8 teams, single elimination BO3 (Grand Final BO5)

## Prediction Model

The composite predictor uses weighted factors:

| Factor           | Weight | Source                    |
|------------------|--------|---------------------------|
| Elo Rating       | 40%    | Derived from HLTV points  |
| HLTV Ranking     | 15%    | Official world ranking    |
| Recent Form      | 15%    | Last 5 match results      |
| Head-to-Head     | 15%    | Historical matchup data   |
| Map Pool         | 10%    | Per-map win rates         |
| Player Ratings   | 5%     | Average HLTV player rating|

## Requirements

- Python 3.10+ (uses only stdlib, no external dependencies)

## Architecture

The simulation pipeline:
1. **Data Layer**: Load team data (HLTV rankings, Elo, map pools, form)
2. **Prediction Layer**: Calculate win probability for any team matchup
3. **Simulation Layer**: Run tournament brackets thousands of times
4. **Aggregation**: Statistical analysis with confidence intervals
5. **Visualization**: Probability tree, stage bars, and web UI
