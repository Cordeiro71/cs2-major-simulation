from __future__ import annotations


def get_html() -> str:
    return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CSDONDO - CS2 Major Simulator</title>
<style>
:root {
  --bg: #0a0a0f;
  --bg2: #12121a;
  --bg3: #1a1a2e;
  --bg4: #22223a;
  --accent: #6c5ce7;
  --accent2: #a29bfe;
  --green: #00b894;
  --yellow: #fdcb6e;
  --red: #e17055;
  --blue: #0984e3;
  --text: #e8e8f0;
  --text2: #a0a0b8;
  --border: #2a2a44;
  --radius: 8px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  min-height: 100vh;
}
.header {
  background: linear-gradient(135deg, var(--bg3), var(--accent));
  padding: 20px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2px solid var(--accent);
}
.header h1 {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.5px;
}
.header h1 span { color: var(--yellow); }
.header .subtitle { color: var(--text2); font-size: 14px; }
.tabs {
  display: flex;
  background: var(--bg2);
  border-bottom: 2px solid var(--border);
  padding: 0 20px;
  overflow-x: auto;
}
.tab {
  padding: 12px 24px;
  cursor: pointer;
  color: var(--text2);
  font-weight: 600;
  font-size: 14px;
  border-bottom: 3px solid transparent;
  transition: all 0.2s;
  white-space: nowrap;
}
.tab:hover { color: var(--text); background: var(--bg3); }
.tab.active { color: var(--accent2); border-bottom-color: var(--accent); }
.content { padding: 20px 30px; max-width: 1400px; margin: 0 auto; }
.page { display: none; }
.page.active { display: block; }
.controls {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 20px;
  margin-bottom: 20px;
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
.controls label { font-size: 13px; color: var(--text2); font-weight: 600; }
.controls select, .controls input {
  background: var(--bg3);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 14px;
}
.controls select:focus, .controls input:focus { outline: none; border-color: var(--accent); }
.btn {
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}
.btn:hover { background: var(--accent2); transform: translateY(-1px); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
.btn-outline {
  background: transparent;
  border: 2px solid var(--accent);
  color: var(--accent2);
}
.btn-danger { background: var(--red); }
.loading {
  text-align: center;
  padding: 60px;
  color: var(--text2);
  font-size: 18px;
}
.loading .spinner {
  display: inline-block;
  width: 40px; height: 40px;
  border: 4px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Teams Grid */
.teams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}
.team-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px;
  transition: all 0.2s;
}
.team-card:hover { border-color: var(--accent); transform: translateY(-2px); }
.team-card .rank {
  display: inline-block;
  background: var(--accent);
  color: white;
  border-radius: 50%;
  width: 32px; height: 32px;
  text-align: center;
  line-height: 32px;
  font-weight: 800;
  font-size: 14px;
  margin-right: 10px;
}
.team-card .team-name { font-size: 18px; font-weight: 700; }
.team-card .team-stats { margin-top: 10px; }
.team-card .stat { display: flex; justify-content: space-between; padding: 2px 0; font-size: 13px; }
.team-card .stat-val { color: var(--accent2); font-weight: 600; }
.form-badge {
  display: inline-block;
  width: 22px; height: 22px;
  border-radius: 4px;
  text-align: center;
  line-height: 22px;
  font-size: 11px;
  font-weight: 800;
  margin-right: 3px;
}
.form-W { background: var(--green); color: white; }
.form-L { background: var(--red); color: white; }

/* Results Table */
.results-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--bg2);
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--border);
}
.results-table th {
  background: var(--bg3);
  padding: 12px 16px;
  text-align: left;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text2);
  border-bottom: 2px solid var(--border);
}
.results-table td {
  padding: 10px 16px;
  font-size: 14px;
  border-bottom: 1px solid var(--border);
}
.results-table tr:hover td { background: var(--bg3); }
.prob-bar {
  height: 8px;
  background: var(--bg);
  border-radius: 4px;
  overflow: hidden;
  min-width: 80px;
}
.prob-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}
.prob-bar-fill.high { background: linear-gradient(90deg, var(--green), #00d2a0); }
.prob-bar-fill.mid { background: linear-gradient(90deg, var(--yellow), #ffeaa7); }
.prob-bar-fill.low { background: linear-gradient(90deg, var(--red), #fab1a0); }

/* Bracket Tree */
.bracket-container {
  overflow-x: auto;
  padding: 20px 0;
}
.bracket {
  display: flex;
  gap: 40px;
  align-items: stretch;
  min-width: fit-content;
}
.bracket-round {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  min-width: 200px;
}
.bracket-round-title {
  text-align: center;
  font-weight: 700;
  color: var(--accent2);
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
  padding: 6px;
  background: var(--bg3);
  border-radius: 4px;
}
.bracket-match {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 6px;
  margin: 4px 0;
  overflow: hidden;
}
.bracket-team {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  font-size: 13px;
  cursor: default;
}
.bracket-team:first-child { border-bottom: 1px solid var(--border); }
.bracket-team.winner { background: rgba(108, 92, 231, 0.15); }
.bracket-team .name { font-weight: 600; }
.bracket-team .prob {
  font-weight: 700;
  color: var(--accent2);
  font-size: 12px;
}

/* Matchup Predictor */
.matchup-panel {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 20px;
  align-items: start;
  margin-top: 20px;
}
.matchup-team-panel {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  text-align: center;
}
.matchup-vs {
  font-size: 32px;
  font-weight: 900;
  color: var(--accent);
  padding-top: 40px;
}
.matchup-team-panel h3 { font-size: 20px; margin-bottom: 8px; }
.matchup-prob {
  font-size: 36px;
  font-weight: 800;
  margin: 8px 0;
}
.prob-high { color: var(--green); }
.prob-mid { color: var(--yellow); }
.prob-low { color: var(--red); }
.factors-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 16px;
}
.factor-card {
  background: var(--bg3);
  border-radius: 6px;
  padding: 12px;
  text-align: center;
}
.factor-card .factor-name { font-size: 12px; color: var(--text2); margin-bottom: 4px; }
.factor-card .factor-val { font-size: 18px; font-weight: 700; }

/* Stage bars */
.stage-container { margin-top: 20px; }
.stage-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
}
.stage-row .team-label { min-width: 160px; font-weight: 600; font-size: 14px; }
.stage-row .stage-bar {
  flex: 1;
  height: 24px;
  background: var(--bg);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}
.stage-row .stage-bar-fill {
  height: 100%;
  border-radius: 4px;
  display: flex;
  align-items: center;
  padding-left: 8px;
  font-size: 11px;
  font-weight: 700;
  transition: width 0.5s ease;
}
.stage-legend {
  display: flex;
  gap: 20px;
  margin: 16px 0;
  font-size: 13px;
}
.stage-legend span { display: flex; align-items: center; gap: 6px; }
.legend-dot { width: 12px; height: 12px; border-radius: 3px; display: inline-block; }

/* Error */
.error-box {
  background: rgba(225, 112, 85, 0.15);
  border: 1px solid var(--red);
  border-radius: var(--radius);
  padding: 16px;
  color: var(--red);
  margin: 16px 0;
}
.section-title {
  font-size: 18px;
  font-weight: 700;
  margin: 20px 0 12px;
  color: var(--accent2);
}
@media (max-width: 768px) {
  .content { padding: 12px; }
  .matchup-panel { grid-template-columns: 1fr; }
  .factors-grid { grid-template-columns: repeat(2, 1fr); }
  .teams-grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>CSDON<span>DO</span></h1>
    <div class="subtitle">CS2 Major Simulation Engine</div>
  </div>
  <div id="statusBar" style="font-size:13px;color:var(--text2)"></div>
</div>

<div class="tabs">
  <div class="tab active" data-page="simulate">Simulacao</div>
  <div class="tab" data-page="bracket">Arvore de Probabilidades</div>
  <div class="tab" data-page="stages">Avanco por Estagio</div>
  <div class="tab" data-page="matchup">Preditor de Matchup</div>
  <div class="tab" data-page="teams">Times</div>
</div>

<div class="content">

<!-- SIMULATE PAGE -->
<div id="page-simulate" class="page active">
  <div class="controls">
    <label>Simulacoes:</label>
    <select id="simCount">
      <option value="100">100 (rapido)</option>
      <option value="500">500</option>
      <option value="1000" selected>1,000</option>
      <option value="5000">5,000</option>
      <option value="10000">10,000</option>
      <option value="50000">50,000 (max)</option>
    </select>
    <button class="btn" id="btnSimulate" onclick="runSimulation()">Simular Major</button>
    <button class="btn btn-outline" onclick="exportResults()">Exportar JSON</button>
  </div>
  <div id="simResults"></div>
</div>

<!-- BRACKET TREE PAGE -->
<div id="page-bracket" class="page">
  <div class="section-title">Arvore de Probabilidades do Playoff</div>
  <div id="bracketTree" class="bracket-container">
    <div class="loading">Execute uma simulacao primeiro na aba "Simulacao"</div>
  </div>
</div>

<!-- STAGES PAGE -->
<div id="page-stages" class="page">
  <div class="section-title">Probabilidade de Avanco por Estagio</div>
  <div class="stage-legend">
    <span><span class="legend-dot" style="background:var(--green)"></span> Champion</span>
    <span><span class="legend-dot" style="background:var(--accent)"></span> Final</span>
    <span><span class="legend-dot" style="background:var(--yellow)"></span> Semifinal</span>
    <span><span class="legend-dot" style="background:var(--blue)"></span> Legends</span>
    <span><span class="legend-dot" style="background:var(--text2)"></span> Challengers</span>
  </div>
  <div id="stageBars">
    <div class="loading">Execute uma simulacao primeiro na aba "Simulacao"</div>
  </div>
</div>

<!-- MATCHUP PAGE -->
<div id="page-matchup" class="page">
  <div class="controls">
    <label>Time 1:</label>
    <select id="team1Select"></select>
    <label>Time 2:</label>
    <select id="team2Select"></select>
    <label>Formato:</label>
    <select id="boFormat">
      <option value="1">BO1</option>
      <option value="3" selected>BO3</option>
      <option value="5">BO5</option>
    </select>
    <button class="btn" onclick="predictMatchup()">Prever Matchup</button>
  </div>
  <div id="matchupResults"></div>
</div>

<!-- TEAMS PAGE -->
<div id="page-teams" class="page">
  <div class="controls">
    <label>Filtrar:</label>
    <input type="text" id="teamFilter" placeholder="Buscar time..." oninput="filterTeams()">
    <label>Ordenar:</label>
    <select id="teamSort" onchange="sortTeams()">
      <option value="ranking">Ranking</option>
      <option value="name">Nome</option>
      <option value="elo">Elo</option>
    </select>
  </div>
  <div id="teamsList" class="teams-grid"></div>
</div>

</div>

<script>
let simData = null;
let teamsData = null;

document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('page-' + tab.dataset.page).classList.add('active');
  });
});

async function runSimulation() {
  const btn = document.getElementById('btnSimulate');
  const sims = parseInt(document.getElementById('simCount').value);
  btn.disabled = true;
  document.getElementById('simResults').innerHTML = '<div class="loading"><div class="spinner"></div><br>Simulando ' + sims.toLocaleString() + ' torneios...</div>';
  document.getElementById('statusBar').textContent = 'Simulando...';

  try {
    const res = await fetch('/api/simulate?sims=' + sims);
    simData = await res.json();
    if (simData.error) throw new Error(simData.error);
    renderResults();
    renderBracketTree();
    renderStageBars();
    document.getElementById('statusBar').textContent = sims.toLocaleString() + ' simulacoes completas';
  } catch(e) {
    document.getElementById('simResults').innerHTML = '<div class="error-box">Erro: ' + e.message + '</div>';
    document.getElementById('statusBar').textContent = 'Erro';
  }
  btn.disabled = false;
}

function renderResults() {
  if (!simData) return;
  const results = simData.simulation.results;
  let html = '<table class="results-table"><thead><tr>';
  html += '<th>#</th><th>Time</th><th>Champion</th><th>Final</th><th>Semi</th><th>Legends</th><th>CI 95%</th>';
  html += '</tr></thead><tbody>';

  results.forEach((r, i) => {
    const prob = r.stage_reach_prob;
    const ci = r.confidence_interval;
    const champPct = (r.win_probability * 100);
    const cls = champPct > 15 ? 'high' : champPct > 5 ? 'mid' : 'low';
    html += '<tr>';
    html += '<td>' + (i+1) + '</td>';
    html += '<td style="font-weight:700">' + r.team_name + '</td>';
    html += '<td><div style="display:flex;align-items:center;gap:8px"><span style="font-weight:700;min-width:50px">' + champPct.toFixed(1) + '%</span><div class="prob-bar"><div class="prob-bar-fill ' + cls + '" style="width:' + Math.min(champPct * 3, 100) + '%"></div></div></div></td>';
    html += '<td>' + ((prob.final||0)*100).toFixed(1) + '%</td>';
    html += '<td>' + ((prob.semifinal||0)*100).toFixed(1) + '%</td>';
    html += '<td>' + ((prob.legends||0)*100).toFixed(1) + '%</td>';
    html += '<td style="font-size:12px;color:var(--text2)">[' + (ci[0]*100).toFixed(1) + '%, ' + (ci[1]*100).toFixed(1) + '%]</td>';
    html += '</tr>';
  });

  html += '</tbody></table>';
  html += '<p style="margin-top:12px;color:var(--text2);font-size:13px">Total: ' + simData.simulation.num_simulations.toLocaleString() + ' simulacoes | ' + simData.simulation.teams_analyzed + ' times</p>';
  document.getElementById('simResults').innerHTML = html;
}

function renderBracketTree() {
  if (!simData) return;
  const results = simData.simulation.results;
  const top8 = results.slice(0, 8);

  if (top8.length < 8) {
    document.getElementById('bracketTree').innerHTML = '<div class="error-box">Dados insuficientes</div>';
    return;
  }

  const qf = [
    [top8[0], top8[7]],
    [top8[1], top8[6]],
    [top8[2], top8[5]],
    [top8[3], top8[4]],
  ];

  function winProb(a, b) {
    const pA = a.win_probability;
    const pB = b.win_probability;
    const total = pA + pB;
    return total > 0 ? pA / total : 0.5;
  }

  function matchupHTML(t1, t2) {
    const p = winProb(t1, t2);
    const winner = p >= 0.5 ? t1 : t2;
    const loser = p >= 0.5 ? t2 : t1;
    const winnerP = Math.max(p, 1-p);
    const loserP = Math.min(p, 1-p);
    return '<div class="bracket-match">' +
      '<div class="bracket-team winner"><span class="name">' + winner.team_name + '</span><span class="prob">' + (winnerP*100).toFixed(1) + '%</span></div>' +
      '<div class="bracket-team"><span class="name">' + loser.team_name + '</span><span class="prob">' + (loserP*100).toFixed(1) + '%</span></div>' +
      '</div>';
  }

  const sfTeams = qf.map(m => winProb(m[0], m[1]) >= 0.5 ? m[0] : m[1]);
  const sf = [[sfTeams[0], sfTeams[3]], [sfTeams[1], sfTeams[2]]];
  const fTeams = sf.map(m => winProb(m[0], m[1]) >= 0.5 ? m[0] : m[1]);
  const champion = winProb(fTeams[0], fTeams[1]) >= 0.5 ? fTeams[0] : fTeams[1];

  let html = '<div class="bracket">';
  html += '<div class="bracket-round"><div class="bracket-round-title">Quartas de Final</div>';
  qf.forEach(m => { html += matchupHTML(m[0], m[1]); });
  html += '</div>';

  html += '<div class="bracket-round"><div class="bracket-round-title">Semifinais</div>';
  sf.forEach(m => { html += matchupHTML(m[0], m[1]); });
  html += '</div>';

  html += '<div class="bracket-round"><div class="bracket-round-title">Final</div>';
  html += matchupHTML(fTeams[0], fTeams[1]);
  html += '</div>';

  html += '<div class="bracket-round"><div class="bracket-round-title">Campeao</div>';
  html += '<div style="background:linear-gradient(135deg,var(--accent),var(--green));border-radius:var(--radius);padding:20px;text-align:center;font-weight:800;font-size:18px;">' + champion.team_name + '<br><span style="font-size:24px;color:var(--yellow)">&#127942;</span></div>';
  html += '</div>';

  html += '</div>';
  document.getElementById('bracketTree').innerHTML = html;
}

function renderStageBars() {
  if (!simData) return;
  const results = simData.simulation.results;
  const stages = [
    {key: 'champion', label: 'Champion', color: 'var(--green)'},
    {key: 'final', label: 'Final', color: 'var(--accent)'},
    {key: 'semifinal', label: 'Semifinal', color: 'var(--yellow)'},
    {key: 'legends', label: 'Legends', color: 'var(--blue)'},
    {key: 'challengers', label: 'Challengers', color: 'var(--text2)'},
  ];

  let html = '<div class="stage-container">';
  results.forEach(r => {
    html += '<div class="stage-row">';
    html += '<div class="team-label">' + r.team_name + '</div>';
    html += '<div class="stage-bar">';
    let offset = 0;
    stages.forEach(s => {
      const prob = r.stage_reach_prob[s.key] || 0;
      const width = prob * 100;
      if (width > 0) {
        html += '<div class="stage-bar-fill" style="position:absolute;left:' + offset + '%;width:' + width + '%;background:' + s.color + ';opacity:0.8"></div>';
        offset = offset + width;
      }
    });
    html += '</div>';
    const champ = (r.stage_reach_prob.champion || 0) * 100;
    html += '<div style="min-width:60px;text-align:right;font-weight:700;font-size:13px;color:' + (champ > 10 ? 'var(--green)' : 'var(--text2)') + '">' + champ.toFixed(1) + '%</div>';
    html += '</div>';
  });
  html += '</div>';
  document.getElementById('stageBars').innerHTML = html;
}

async function predictMatchup() {
  const t1 = document.getElementById('team1Select').value;
  const t2 = document.getElementById('team2Select').value;
  const bo = document.getElementById('boFormat').value;
  if (!t1 || !t2) return;

  document.getElementById('matchupResults').innerHTML = '<div class="loading"><div class="spinner"></div></div>';

  try {
    const res = await fetch('/api/predict?team1=' + encodeURIComponent(t1) + '&team2=' + encodeURIComponent(t2) + '&bo=' + bo);
    const data = await res.json();
    if (data.error) throw new Error(data.error);
    renderMatchup(data);
  } catch(e) {
    document.getElementById('matchupResults').innerHTML = '<div class="error-box">' + e.message + '</div>';
  }
}

function renderMatchup(data) {
  const t1p = data.team1_win_prob;
  const t2p = data.team2_win_prob;
  const t1cls = t1p > 0.6 ? 'prob-high' : t1p > 0.4 ? 'prob-mid' : 'prob-low';
  const t2cls = t2p > 0.6 ? 'prob-high' : t2p > 0.4 ? 'prob-mid' : 'prob-low';

  let html = '<div class="matchup-panel">';
  html += '<div class="matchup-team-panel">';
  html += '<h3>' + data.team1.name + '</h3>';
  html += '<div style="color:var(--text2);font-size:13px">Rank #' + data.team1.ranking + ' | Elo ' + data.team1.elo + '</div>';
  html += '<div class="matchup-prob ' + t1cls + '">' + (t1p*100).toFixed(1) + '%</div>';
  html += '<div style="color:var(--text2);font-size:13px">BO' + data.bo_n + '</div>';
  html += '</div>';

  html += '<div class="matchup-vs">VS</div>';

  html += '<div class="matchup-team-panel">';
  html += '<h3>' + data.team2.name + '</h3>';
  html += '<div style="color:var(--text2);font-size:13px">Rank #' + data.team2.ranking + ' | Elo ' + data.team2.elo + '</div>';
  html += '<div class="matchup-prob ' + t2cls + '">' + (t2p*100).toFixed(1) + '%</div>';
  html += '<div style="color:var(--text2);font-size:13px">BO' + data.bo_n + '</div>';
  html += '</div>';
  html += '</div>';

  html += '<div style="margin-top:16px;text-align:center;color:var(--text2)">Placar previsto: <strong style="color:var(--text)">' + data.predicted_score[0] + ' - ' + data.predicted_score[1] + '</strong> | Confianca: <strong style="color:var(--text)">' + (data.confidence*100).toFixed(0) + '%</strong></div>';

  html += '<div class="section-title">Fatores de Predicao</div>';
  html += '<div class="factors-grid">';
  const factors = data.factors || {};
  const fLabels = {elo:'Elo Rating', ranking:'Ranking HLTV', form:'Forma Recente', map_pool:'Map Pool', h2h:'Head-to-Head', player_rating:'Rating Jogadores'};
  for (const [k, v] of Object.entries(factors)) {
    html += '<div class="factor-card"><div class="factor-name">' + (fLabels[k]||k) + '</div><div class="factor-val">' + (v*100).toFixed(1) + '%</div><div class="prob-bar" style="margin-top:6px"><div class="prob-bar-fill ' + (v>0.55?'high':v>0.45?'mid':'low') + '" style="width:' + (v*100) + '%"></div></div></div>';
  }
  html += '</div>';

  document.getElementById('matchupResults').innerHTML = html;
}

async function loadTeams() {
  try {
    const res = await fetch('/api/teams');
    teamsData = await res.json();
    populateTeamSelects();
    renderTeams();
  } catch(e) {
    console.error(e);
  }
}

function populateTeamSelects() {
  if (!teamsData) return;
  const s1 = document.getElementById('team1Select');
  const s2 = document.getElementById('team2Select');
  teamsData.forEach((t, i) => {
    const o1 = document.createElement('option');
    o1.value = t.name; o1.textContent = '#' + t.ranking + ' ' + t.name;
    s1.appendChild(o1);
    const o2 = document.createElement('option');
    o2.value = t.name; o2.textContent = '#' + t.ranking + ' ' + t.name;
    if (i === 1) o2.selected = true;
    s2.appendChild(o2);
  });
}

function renderTeams(filtered) {
  const teams = filtered || teamsData;
  if (!teams) return;
  let html = '';
  teams.forEach(t => {
    const formHTML = t.recent_form.map(f => '<span class="form-badge form-' + f + '">' + f + '</span>').join('');
    html += '<div class="team-card">';
    html += '<div style="display:flex;align-items:center"><span class="rank">' + t.ranking + '</span><span class="team-name">' + t.name + '</span></div>';
    html += '<div class="team-stats">';
    html += '<div class="stat"><span>Elo</span><span class="stat-val">' + t.elo + '</span></div>';
    html += '<div class="stat"><span>Pontos HLTV</span><span class="stat-val">' + t.points + '</span></div>';
    html += '<div class="stat"><span>Forma</span><span>' + formHTML + '</span></div>';
    html += '<div class="stat"><span>Rating Medio</span><span class="stat-val">' + t.avg_player_rating.toFixed(2) + '</span></div>';
    html += '<div class="stat"><span>Forma Score</span><span class="stat-val">' + (t.form_score*100).toFixed(0) + '%</span></div>';
    html += '</div>';

    if (t.map_pool && Object.keys(t.map_pool).length) {
      html += '<div style="margin-top:8px;font-size:12px;color:var(--text2)">Map Pool:</div>';
      Object.entries(t.map_pool).forEach(([map, str]) => {
        const w = Math.max(str * 100, 5);
        html += '<div style="display:flex;align-items:center;gap:6px;font-size:11px;margin:2px 0"><span style="min-width:70px;color:var(--text2)">' + map + '</span><div class="prob-bar" style="flex:1;height:6px"><div class="prob-bar-fill ' + (str>0.55?'high':str>0.45?'mid':'low') + '" style="width:' + w + '%"></div></div><span>' + (str*100).toFixed(0) + '%</span></div>';
      });
    }

    if (t.players && t.players.length) {
      html += '<div style="margin-top:8px;font-size:12px;color:var(--text2)">Jogadores:</div>';
      t.players.forEach(p => {
        html += '<div style="font-size:11px;display:flex;justify-content:space-between;padding:1px 0"><span>' + p.nickname + '</span><span style="color:var(--accent2)">Rating ' + p.rating.toFixed(2) + ' | ADR ' + p.adr.toFixed(0) + '</span></div>';
      });
    }

    html += '</div>';
  });
  document.getElementById('teamsList').innerHTML = html;
}

function filterTeams() {
  if (!teamsData) return;
  const q = document.getElementById('teamFilter').value.toLowerCase();
  const filtered = teamsData.filter(t => t.name.toLowerCase().includes(q));
  renderTeams(filtered);
}

function sortTeams() {
  if (!teamsData) return;
  const key = document.getElementById('teamSort').value;
  const sorted = [...teamsData].sort((a, b) => {
    if (key === 'name') return a.name.localeCompare(b.name);
    if (key === 'elo') return b.elo - a.elo;
    return a.ranking - b.ranking;
  });
  renderTeams(sorted);
}

function exportResults() {
  if (!simData) { alert('Execute uma simulacao primeiro'); return; }
  const blob = new Blob([JSON.stringify(simData, null, 2)], {type: 'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'csdondo_simulation.json'; a.click();
  URL.revokeObjectURL(url);
}

loadTeams();
</script>
</body>
</html>'''
