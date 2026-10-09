"""Player eyes and the GM correction door. Speech still belongs to Discord."""

_SHARED_JS = r"""
function signed(n) {
  const num = Number(n);
  if (!Number.isFinite(num)) return "";
  return (num >= 0 ? "+" : "") + num;
}
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null && text !== "") node.textContent = text;
  return node;
}
function rich(text) {
  const frag = document.createDocumentFragment();
  String(text || "").split("**").forEach((part, index) => {
    if (!part) return;
    if (index % 2 === 1) {
      const strong = document.createElement("strong");
      strong.textContent = part;
      frag.appendChild(strong);
    } else {
      frag.appendChild(document.createTextNode(part));
    }
  });
  return frag;
}
function fillRich(node, text) {
  node.replaceChildren(rich(text));
}
function bar(current, max) {
  const pct = max ? Math.max(0, Math.min(100, current / max * 100)) : 0;
  const wrap = el("div", "hp");
  const span = document.createElement("span");
  span.style.width = pct + "%";
  wrap.appendChild(span);
  return wrap;
}
function sectionBody(section) {
  const text = section.text || "";
  const lines = text.split("\n");
  const first = (lines[0] || "").replaceAll("*", "").trim();
  if (first === section.title) return lines.slice(1).join("\n");
  return text;
}
function sheetSections(crawler) {
  const wrap = document.createDocumentFragment();
  const sections = crawler.card_sections || [];
  if (!sections.length) {
    const pre = el("pre", "prose");
    fillRich(pre, crawler.card_text || (crawler.name + " " + crawler.class_name + " " + crawler.level));
    wrap.appendChild(pre);
    return wrap;
  }
  for (const section of sections) {
    const block = el("section", "block");
    block.appendChild(el("h2", "", section.title));
    const pre = el("pre", "prose");
    fillRich(pre, sectionBody(section));
    block.appendChild(pre);
    wrap.appendChild(block);
  }
  return wrap;
}
function namedList(parent, title, rows) {
  if (!rows || !rows.length) return;
  parent.appendChild(el("h3", "", title));
  for (const row of rows) {
    const p = el("p", "action");
    const name = el("strong", "", row.name);
    p.appendChild(name);
    if (row.text) {
      p.appendChild(document.createTextNode(". " + row.text));
    }
    parent.appendChild(p);
  }
}
function coverSentence(enemy) {
  if (enemy.cover === "half") return "Half cover from the counter. Attacks roll against AC " + (Number(enemy.ac) + 2) + ".";
  if (enemy.cover === "three-quarters") return "Three-quarters cover. Attacks roll against AC " + (Number(enemy.ac) + 5) + ".";
  if (enemy.cover) return "Cover: " + enemy.cover + ".";
  return "No cover. Attacks roll against the printed AC.";
}
function enemyCard(enemy) {
  const card = enemy.card || {};
  const article = el("article", "card foe" + (enemy.hp <= 0 ? " down" : ""));
  article.appendChild(el("h2", "", enemy.name));
  if (card.nameplate) article.appendChild(el("p", "plate", card.nameplate));
  article.appendChild(el("p", "spoken", enemy.spoken_name || ""));
  if (card.type_line) article.appendChild(el("p", "", card.type_line));
  if (card.picture || enemy.picture) article.appendChild(el("p", "picture", card.picture || enemy.picture));
  if (enemy.system_line || card.system_line) article.appendChild(el("p", "system", enemy.system_line || card.system_line));
  article.appendChild(bar(enemy.hp, enemy.hp_max));
  const formula = card.hp_formula ? " (" + card.hp_formula + ")" : "";
  article.appendChild(el("p", "vitals", "HP " + enemy.hp + "/" + enemy.hp_max + formula + "   AC " + enemy.ac));
  article.appendChild(el("p", "", coverSentence(enemy)));
  const speed = [];
  if (card.speed) speed.push("Speed " + card.speed);
  if (card.initiative != null && card.initiative !== "") speed.push("Initiative " + signed(card.initiative));
  if (speed.length) article.appendChild(el("p", "", speed.join("   ")));
  const grid = el("div", "abilities");
  for (const ability of card.abilities || []) {
    const cell = el("div", "");
    cell.appendChild(el("div", "ab-key", String(ability.key || "").toUpperCase()));
    cell.appendChild(el("div", "ab-score", String(ability.score)));
    cell.appendChild(el("div", "ab-mod", signed(ability.mod) + "  save " + signed(ability.save)));
    grid.appendChild(cell);
  }
  if ((card.abilities || []).length) article.appendChild(grid);
  for (const label of card.labels || []) {
    const p = el("p", label.name === "Vulnerabilities" ? "vuln" : "");
    p.appendChild(el("strong", "", label.name + " "));
    p.appendChild(document.createTextNode(label.text || ""));
    article.appendChild(p);
  }
  if (card.cr != null && card.cr !== "") {
    article.appendChild(el("p", "", "CR " + card.cr + " (XP " + card.xp + "; PB " + signed(card.pb) + ")"));
  }
  namedList(article, "Traits", card.traits);
  namedList(article, "Actions", card.actions);
  namedList(article, "Bonus actions", card.bonus_actions);
  namedList(article, "Reactions", card.reactions);
  const rolls = (enemy.attacks || []).map((atk) => atk.name + " +" + atk.to_hit + ", " + atk.damage + " " + atk.type + ", " + atk.kind);
  if (rolls.length) article.appendChild(el("p", "rolls", "Rolls this fight: " + rolls.join("; ")));
  if ((enemy.conditions || []).length) article.appendChild(el("p", "", "Conditions: " + enemy.conditions.join(", ")));
  if (card.tactics) article.appendChild(el("p", "", "Tactics: " + card.tactics));
  return article;
}
function roomPanel(card) {
  const box = el("section", "card room");
  if (!card) return box;
  box.appendChild(el("h2", "", card.name || "Room"));
  if (card.read_aloud) {
    const read = el("p", "read");
    fillRich(read, card.read_aloud);
    box.appendChild(read);
  }
  if (card.layout) box.appendChild(el("p", "", card.layout));
  if ((card.features || []).length) {
    box.appendChild(el("h3", "", "In the room"));
    for (const feature of card.features) box.appendChild(el("p", "", feature));
  }
  if ((card.exits || []).length) {
    box.appendChild(el("h3", "", "Exits"));
    for (const exit of card.exits) box.appendChild(el("p", "", exit));
  }
  return box;
}
function pip(on, label) {
  return (on ? "ready" : "spent") + " " + label;
}
function turnStrip(crawler) {
  const box = el("div", "");
  const ac = crawler.ac + (crawler.ac_bonus ? "+" + crawler.ac_bonus : "");
  const temp = crawler.temp_hp ? " +" + crawler.temp_hp + " temp" : "";
  box.appendChild(el("p", "vitals", crawler.name + "  HP " + crawler.hp + "/" + crawler.hp_max + temp + "  AC " + ac + (crawler.cover ? "  your cover " + crawler.cover : "")));
  box.appendChild(bar(crawler.hp, crawler.hp_max));
  box.appendChild(el("p", "", pip(crawler.action, "action") + "  ·  " + pip(crawler.bonus, "bonus") + "  ·  " + pip(crawler.reaction, "reaction") + "  ·  " + pip(crawler.object, "object")));
  let move = "Movement " + crawler.movement_left + " ft";
  if (crawler.hidden) move += "  ·  hidden";
  if (crawler.hp <= 0) move += "  ·  death saves " + crawler.death_success + " success, " + crawler.death_fail + " fail";
  box.appendChild(el("p", "", move));
  return box;
}
"""

PLAYER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Shooting Gallery</title>
<style>
  :root { color-scheme: dark; }
  body { margin: 0; font: 16px/1.45 system-ui, sans-serif; background: #1a120c; color: #f3e6d0; }
  header { position: sticky; top: 0; z-index: 2; padding: 12px 20px; background: #2a1c12; border-bottom: 1px solid #6b4a2a; }
  main { padding: 16px 20px 48px; }
  h1 { margin: 0 0 4px; font-size: 22px; }
  h2 { margin: 0 0 6px; font-size: 16px; letter-spacing: 0.03em; }
  h3 { margin: 12px 0 4px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.06em; color: #f0d78c; }
  .muted, header p { color: #c8b497; margin: 0; }
  .grid { display: grid; grid-template-columns: minmax(280px, 1fr) minmax(280px, 1fr); gap: 16px; align-items: start; }
  .foes { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; margin: 12px 0; }
  .card { background: #2c2118; border: 1px solid #6b4a2a; border-radius: 8px; padding: 12px 14px; margin-bottom: 12px; }
  .foe.down { opacity: 0.55; }
  .plate { color: #f0d78c; }
  .picture, .read { color: #e7d7bd; }
  .system { color: #d7c4a3; }
  .vuln { color: #f0b429; }
  .rolls { color: #9fd0c3; }
  .prose { white-space: pre-wrap; font: 14px/1.4 ui-monospace, monospace; margin: 0; }
  .block { margin-top: 14px; }
  .abilities { display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; margin: 8px 0; }
  .abilities div { background: #1a120c; border-radius: 4px; padding: 4px; text-align: center; }
  .ab-key { font-size: 11px; letter-spacing: 0.04em; color: #c8b497; }
  .ab-score { font-size: 18px; }
  .ab-mod { font-size: 11px; color: #c8b497; }
  .hp { height: 8px; background: #3a2a1c; border-radius: 4px; overflow: hidden; margin: 6px 0; }
  .hp span { display: block; height: 100%; background: #c4542c; }
  .log { min-height: 180px; max-height: 360px; overflow: auto; }
  .you { color: #f3e6d0; }
  .gm { color: #f0d78c; }
  .roll { color: #9fd0c3; }
  form, .row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  input, button, select { font: inherit; padding: 8px 10px; border-radius: 6px; border: 1px solid #6b4a2a; background: #1a120c; color: inherit; }
  button { background: #c4542c; color: #1a120c; border: 0; cursor: pointer; }
  button.quiet { background: #3a2a1c; color: #f3e6d0; }
  .action { margin: 4px 0; }
  @media (max-width: 800px) {
    .grid, .abilities { grid-template-columns: repeat(3, 1fr); }
    .grid { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>
<header>
  <h1 id="room">Shooting Gallery</h1>
  <p id="round"></p>
</header>
<main>
  <div id="room-card"></div>
  <div id="enemies" class="foes"></div>
  <div class="grid">
    <article class="card" id="sheet"></article>
    <section>
      <div class="card" id="turn"></div>
      <div class="card log" id="log" aria-live="polite"></div>
      <form id="line-form">
        <label for="line">What you do</label>
        <input id="line" name="line" size="50" autocomplete="off" placeholder="I get behind the sandbags, then I cast eldritch blast at the first mannequin">
        <button type="submit">Send</button>
      </form>
      <p class="row" id="actions"></p>
    </section>
  </div>
  <form id="seat-form" class="card">
    <strong>Or seat a different Crawler</strong>
    <p class="muted">This replaces the copy of Raithen for a fresh fight. It does not write the live sheet.</p>
    <label>Name <input name="name" required maxlength="40"></label>
    <label>Class <input name="class_name" value="Rogue"></label>
    <label>Level <input name="level" type="number" min="1" max="20" value="1"></label>
    <label>HP <input name="hp" type="number" min="1" max="999" value="11"></label>
    <label>AC <input name="ac" type="number" min="1" max="30" value="14"></label>
    <label>Attack <input name="attack_name" value="Shortbow"></label>
    <label>To hit <input name="to_hit" type="number" min="-5" max="20" value="5"></label>
    <label>Damage <input name="damage" value="1d6+3"></label>
    <label>Type
      <select name="type">
        <option>piercing</option>
        <option>bludgeoning</option>
        <option>slashing</option>
      </select>
    </label>
    <button type="submit">Seat</button>
    <span id="seat-note" class="muted"></span>
  </form>
</main>
<script>
""" + _SHARED_JS + """
const logEl = document.getElementById("log");
let last = "";
function render(data) {
  document.getElementById("room").textContent = data.room;
  document.getElementById("round").textContent = "Round " + data.round + (data.gallery_clear ? " · gallery clear" : "");
  document.getElementById("room-card").replaceChildren(roomPanel(data.room_card));
  const foes = document.getElementById("enemies");
  foes.replaceChildren();
  for (const enemy of data.enemies) foes.appendChild(enemyCard(enemy));
  document.getElementById("sheet").replaceChildren(sheetSections(data.crawler));
  document.getElementById("turn").replaceChildren(turnStrip(data.crawler));
  logEl.replaceChildren();
  for (const entry of data.log) {
    const p = document.createElement("div");
    p.className = (entry.voice || "").toLowerCase();
    p.textContent = entry.text;
    logEl.appendChild(p);
  }
  logEl.scrollTop = logEl.scrollHeight;
  const row = document.getElementById("actions");
  row.replaceChildren();
  const attacks = data.crawler.attacks || [];
  const shot = attacks.find((atk) => /eldritch blast/i.test(atk.name)) || attacks[0];
  function add(label, line) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "quiet";
    button.textContent = label;
    button.addEventListener("click", () => send(line));
    row.appendChild(button);
  }
  if (shot) add("Cover, then " + shot.name, "I get behind the sandbags, then I use " + shot.name + " at the first mannequin");
  for (const atk of attacks) add(atk.name, "I use " + atk.name + " at the first mannequin");
  for (const spell of data.crawler.spells || []) {
    const cost = spell.cost ? " (" + spell.cost + ")" : "";
    add(spell.name + cost, "I cast " + spell.name);
  }
  add("Swing the body", "I pick up the body and swing it at the other mannequin");
  add("End turn", "I end turn");
}
async function refresh() {
  const res = await fetch("/api/player");
  const data = await res.json();
  const key = JSON.stringify(data);
  if (key === last) return;
  last = key;
  render(data);
}
async function send(text) {
  const res = await fetch("/api/line", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text})
  });
  const data = await res.json();
  if (!res.ok) {
    document.getElementById("seat-note").textContent = data.error || "line refused";
    return;
  }
  last = JSON.stringify(data.view);
  render(data.view);
}
document.getElementById("line-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const input = document.getElementById("line");
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  send(text);
});
document.getElementById("seat-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.target;
  const body = {
    name: form.name.value,
    class_name: form.class_name.value,
    level: Number(form.level.value),
    hp: Number(form.hp.value),
    hp_max: Number(form.hp.value),
    ac: Number(form.ac.value),
    attack: {
      name: form.attack_name.value,
      to_hit: Number(form.to_hit.value),
      damage: form.damage.value,
      type: form.type.value
    },
    skills: ["stealth"],
    dex_mod: 3,
    str_mod: 0,
    pb: 2
  };
  const res = await fetch("/api/seat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });
  const data = await res.json();
  document.getElementById("seat-note").textContent = res.ok ? "Seated." : (data.error || "refused");
  if (res.ok) {
    last = JSON.stringify(data.view);
    render(data.view);
  }
});
refresh();
setInterval(refresh, 1000);
</script>
</body>
</html>
"""

GM_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Table</title>
<style>
  :root { color-scheme: dark; }
  body { margin: 0; font: 16px/1.45 system-ui, sans-serif; background: #121418; color: #e6e1d6; }
  header { position: sticky; top: 0; z-index: 2; padding: 12px 20px; background: #1c222b; border-bottom: 1px solid #3d4a5c; }
  main { padding: 16px 20px 48px; }
  h1 { margin: 0 0 4px; font-size: 22px; }
  h2 { margin: 0 0 6px; font-size: 16px; }
  h3 { margin: 12px 0 4px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.06em; color: #d7c4a3; }
  .note, header p { color: #d7c4a3; margin: 0; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-items: start; }
  .foes { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; }
  .card { background: #1c222b; border: 1px solid #3d4a5c; border-radius: 8px; padding: 12px 14px; margin-bottom: 12px; }
  .foe.down { opacity: 0.55; }
  .secret { margin-top: 10px; padding-top: 8px; border-top: 1px dashed #d7c4a3; color: #f0d78c; }
  .prose, pre { white-space: pre-wrap; font: 14px/1.4 ui-monospace, monospace; margin: 0; }
  .block { margin-top: 14px; }
  .abilities { display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; margin: 8px 0; }
  .abilities div { background: #121418; border-radius: 4px; padding: 4px; text-align: center; }
  .ab-key, .ab-mod { font-size: 11px; color: #d7c4a3; }
  .ab-score { font-size: 18px; }
  .hp { height: 8px; background: #121418; border-radius: 4px; overflow: hidden; margin: 6px 0; }
  .hp span { display: block; height: 100%; background: #d7c4a3; }
  .vuln { color: #f0b429; }
  .picture, .read { color: #e6e1d6; }
  form, .row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  input, button, select { font: inherit; padding: 8px 10px; border-radius: 6px; border: 1px solid #3d4a5c; background: #121418; color: inherit; }
  button { background: #d7c4a3; color: #121418; border: 0; cursor: pointer; }
  .action { margin: 4px 0; }
  @media (max-width: 800px) {
    .grid { grid-template-columns: 1fr; }
    .abilities { grid-template-columns: repeat(3, 1fr); }
  }
</style>
</head>
<body>
<header>
  <h1>Table</h1>
  <p>Every card, the cheese notes, and the raw line. Players do not get this page.</p>
</header>
<main>
  <div class="row card">
    <button type="button" id="undo">Undo last resolution</button>
    <form id="fix">
      <label>Combatant <select id="who" name="who"></select></label>
      <label>HP <input id="hp" name="hp" type="number" min="0" value="0"></label>
      <button type="submit">Set hit points</button>
    </form>
    <span id="note"></span>
  </div>
  <div id="room-card"></div>
  <section class="card"><strong>GM note from the room stub</strong><pre id="secret"></pre></section>
  <section class="card" id="pacing"></section>
  <div id="enemies" class="foes"></div>
  <article class="card" id="sheet"></article>
  <div class="grid">
    <section class="card"><strong>Heard</strong><pre id="raw"></pre></section>
    <section class="card"><strong>Spoken back</strong><pre id="log"></pre></section>
  </div>
</main>
<script>
""" + _SHARED_JS + """
let last = "";
function withSecret(article, enemy) {
  const secret = el("div", "secret");
  secret.appendChild(el("h3", "", "Table only"));
  if (enemy.gm_line) secret.appendChild(el("p", "", "GM: " + enemy.gm_line));
  if (enemy.how_to_cheese) secret.appendChild(el("p", "", "Cheese: " + enemy.how_to_cheese));
  if (enemy.what_it_wants) secret.appendChild(el("p", "", "Wants: " + enemy.what_it_wants));
  article.appendChild(secret);
  return article;
}
function pacing(block) {
  const box = el("div", "");
  box.appendChild(el("h2", "", "Pacing guide"));
  if (!block || !Object.keys(block).length) {
    box.appendChild(el("p", "", "None on this room card."));
    return box;
  }
  for (const key of ["tag", "setup", "decision", "on_success", "on_failure", "cut_short", "minutes"]) {
    if (block[key] == null || block[key] === "") continue;
    const p = el("p", "");
    p.appendChild(el("strong", "", key.replaceAll("_", " ") + ": "));
    p.appendChild(document.createTextNode(String(block[key])));
    box.appendChild(p);
  }
  return box;
}
function render(data) {
  document.getElementById("room-card").replaceChildren(roomPanel(data.room_card));
  document.getElementById("secret").textContent = data.gm_note || "";
  document.getElementById("pacing").replaceChildren(pacing(data.room_gm));
  const foes = document.getElementById("enemies");
  foes.replaceChildren();
  const select = document.getElementById("who");
  const previous = select.value;
  select.replaceChildren();
  function add(id, name) {
    const option = document.createElement("option");
    option.value = id;
    option.textContent = name;
    select.appendChild(option);
  }
  add(data.crawler.id, data.crawler.name + " " + data.crawler.hp + "/" + data.crawler.hp_max);
  for (const enemy of data.enemies) {
    foes.appendChild(withSecret(enemyCard(enemy), enemy));
    add(enemy.id, enemy.name + " " + enemy.hp + "/" + enemy.hp_max);
  }
  if (previous) select.value = previous;
  const sheet = document.getElementById("sheet");
  sheet.replaceChildren(el("h2", "", "Crawler card"));
  sheet.appendChild(turnStrip(data.crawler));
  sheet.appendChild(sheetSections(data.crawler));
  document.getElementById("raw").textContent = (data.raw || []).join("\\n");
  document.getElementById("log").textContent = (data.log || []).map((entry) => entry.text).join("\\n");
}
async function refresh() {
  const res = await fetch("/api/gm");
  const data = await res.json();
  const key = JSON.stringify(data);
  if (key === last) return;
  last = key;
  render(data);
}
document.getElementById("undo").addEventListener("click", async () => {
  const res = await fetch("/api/undo", {method: "POST"});
  const data = await res.json();
  document.getElementById("note").textContent = res.ok ? "Undone." : (data.error || "nothing to undo");
  if (res.ok) {
    last = JSON.stringify(data.view);
    render(data.view);
  }
});
document.getElementById("fix").addEventListener("submit", async (event) => {
  event.preventDefault();
  const res = await fetch("/api/correct", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({id: document.getElementById("who").value, hp: Number(document.getElementById("hp").value)})
  });
  const data = await res.json();
  document.getElementById("note").textContent = res.ok ? "Corrected." : (data.error || "refused");
  if (res.ok) {
    last = JSON.stringify(data.view);
    render(data.view);
  }
});
refresh();
setInterval(refresh, 1000);
</script>
</body>
</html>
"""
