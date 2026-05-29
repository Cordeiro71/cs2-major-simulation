from __future__ import annotations
import json
from ..data.models import SimulationResult, MatchPrediction


def display_simulation_results(results: dict) -> str:
    lines = []
    lines.append("=" * 80)
    lines.append("CS2 MAJOR SIMULATION RESULTS")
    lines.append(f"Simulations: {results['num_simulations']:,} | Teams: {results['teams_analyzed']}")
    lines.append("=" * 80)

    for i, r in enumerate(results["results"], 1):
        ci = r.confidence_interval
        lines.append("")
        lines.append(f"#{i:2d} {r.team_name}")
        lines.append(f"    Championship Win Probability: {r.win_probability:.1%}")
        lines.append(f"    95% Confidence Interval:      [{ci[0]:.1%}, {ci[1]:.1%}]")

        if r.stage_reach_prob:
            lines.append("    Stage Advancement:")
            for stage, prob in r.stage_reach_prob.items():
                bar = _progress_bar(prob)
                lines.append(f"      {stage:12s}: {prob:.1%} {bar}")

    return "\n".join(lines)


def display_match_prediction(pred: MatchPrediction) -> str:
    lines = []
    lines.append("-" * 60)
    lines.append(f"  {pred.team1.name}  vs  {pred.team2.name}")
    lines.append("-" * 60)
    lines.append(f"  {pred.team1.name}: {pred.team1_win_prob:.1%}")
    lines.append(f"  {pred.team2.name}: {pred.team2_win_prob:.1%}")
    lines.append(f"  Predicted Score:  {pred.predicted_score[0]}-{pred.predicted_score[1]}")
    lines.append(f"  Confidence: {pred.confidence:.1%}")
    lines.append("")
    lines.append("  Prediction Factors:")
    for factor, val in pred.factors.items():
        bar = _progress_bar(val)
        lines.append(f"    {factor:15s}: {val:.3f} {bar}")
    lines.append("-" * 60)
    return "\n".join(lines)


def display_bracket(teams: list, predictions: list[MatchPrediction]) -> str:
    lines = []
    lines.append("")
    lines.append("QUARTERFINALS")
    lines.append("-" * 50)
    for i in range(0, min(8, len(teams)), 2):
        if i < len(predictions):
            pred = predictions[i // 2] if i // 2 < len(predictions) else None
            if pred:
                lines.append(f"  {pred.team1.name:20s} ({pred.team1_win_prob:.0%})  vs  {pred.team2.name:20s} ({pred.team2_win_prob:.0%})")
    return "\n".join(lines)


def display_probability_tree(results: dict) -> str:
    lines = []
    lines.append("")
    lines.append("=" * 80)
    lines.append("  PROBABILITY TREE - MOST LIKELY TOURNAMENT PATHS")
    lines.append("=" * 80)

    sorted_results = sorted(results["results"], key=lambda r: r.win_probability, reverse=True)
    top_teams = sorted_results[:8]

    if not top_teams:
        return "\n".join(lines)

    lines.append("")
    lines.append("  PLAYOFF BRACKET (Most Likely Matchups)")
    lines.append("  " + "-" * 70)

    if len(top_teams) >= 8:
        matchups_qf = [
            (top_teams[0], top_teams[7]),
            (top_teams[1], top_teams[6]),
            (top_teams[2], top_teams[5]),
            (top_teams[3], top_teams[4]),
        ]

        lines.append("  QUARTERFINALS:")
        semi_teams = []
        for i, (t1, t2) in enumerate(matchups_qf):
            t1_champ = t1.stage_reach_prob.get("champion", t1.win_probability)
            t2_champ = t2.stage_reach_prob.get("champion", t2.win_probability)
            total = t1_champ + t2_champ
            t1_pct = t1_champ / total if total > 0 else 0.5
            t2_pct = t2_champ / total if total > 0 else 0.5
            winner = t1 if t1_pct > t2_pct else t2
            semi_teams.append(winner)
            lines.append(f"    QF{i+1}: {t1.team_name:20s} ({t1_pct:5.1%})  vs  {t2.team_name:20s} ({t2_pct:5.1%})")
            lines.append(f"          -> {winner.team_name} advances")

        lines.append("")
        lines.append("  SEMIFINALS:")
        sf_matchups = [
            (semi_teams[0], semi_teams[3]),
            (semi_teams[1], semi_teams[2]),
        ]
        final_teams = []
        for i, (t1, t2) in enumerate(sf_matchups):
            t1_champ = t1.stage_reach_prob.get("champion", t1.win_probability)
            t2_champ = t2.stage_reach_prob.get("champion", t2.win_probability)
            total = t1_champ + t2_champ
            t1_pct = t1_champ / total if total > 0 else 0.5
            t2_pct = t2_champ / total if total > 0 else 0.5
            winner = t1 if t1_pct > t2_pct else t2
            final_teams.append(winner)
            lines.append(f"    SF{i+1}: {t1.team_name:20s} ({t1_pct:5.1%})  vs  {t2.team_name:20s} ({t2_pct:5.1%})")
            lines.append(f"          -> {winner.team_name} advances")

        lines.append("")
        lines.append("  GRAND FINAL:")
        if len(final_teams) >= 2:
            t1, t2 = final_teams[0], final_teams[1]
            t1_champ = t1.stage_reach_prob.get("champion", t1.win_probability)
            t2_champ = t2.stage_reach_prob.get("champion", t2.win_probability)
            total = t1_champ + t2_champ
            t1_pct = t1_champ / total if total > 0 else 0.5
            t2_pct = t2_champ / total if total > 0 else 0.5
            lines.append(f"    GF:  {t1.team_name:20s} ({t1_pct:5.1%})  vs  {t2.team_name:20s} ({t2_pct:5.1%})")
            champion = t1 if t1_pct > t2_pct else t2
            lines.append(f"          -> {champion.team_name} WINS THE MAJOR!")

    lines.append("")
    lines.append("  TOP 10 MOST LIKELY CHAMPIONS:")
    lines.append("  " + "-" * 50)
    for i, r in enumerate(sorted_results[:10], 1):
        champ_prob = r.stage_reach_prob.get("champion", r.win_probability)
        final_prob = r.stage_reach_prob.get("final", 0)
        semi_prob = r.stage_reach_prob.get("semifinal", 0)
        bar = _progress_bar(champ_prob, width=30)
        lines.append(f"  {i:2d}. {r.team_name:25s} Champ: {champ_prob:6.2%} {bar}")
        lines.append(f"      {'':25s} Final: {final_prob:6.2%} | Semi: {semi_prob:6.2%}")

    return "\n".join(lines)


def display_stage_tree(results: dict) -> str:
    lines = []
    lines.append("")
    lines.append("=" * 80)
    lines.append("  STAGE-BY-STAGE ADVANCEMENT TREE")
    lines.append("=" * 80)

    sorted_results = sorted(results["results"], key=lambda r: r.win_probability, reverse=True)

    stages = ["challengers", "legends", "semifinal", "final", "champion"]
    stage_labels = {
        "challengers": "Challengers",
        "legends": "Legends",
        "semifinal": "Semifinals",
        "final": "Grand Final",
        "champion": "CHAMPION",
    }

    for stage in stages:
        label = stage_labels.get(stage, stage)
        lines.append(f"")
        lines.append(f"  {label}")
        lines.append(f"  {'-' * 70}")

        stage_teams = []
        for r in sorted_results:
            prob = r.stage_reach_prob.get(stage, 0)
            if prob > 0:
                stage_teams.append((r, prob))

        stage_teams.sort(key=lambda x: x[1], reverse=True)

        for r, prob in stage_teams[:16]:
            bar = _progress_bar(prob, width=25)
            lines.append(f"    {r.team_name:25s} {prob:6.1%} {bar}")

        if not stage_teams:
            lines.append("    (no teams)")

    return "\n".join(lines)


def _progress_bar(value: float, width: int = 20) -> str:
    filled = int(value * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"
