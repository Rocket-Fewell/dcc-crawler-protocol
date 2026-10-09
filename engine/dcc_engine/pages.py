"""Player eyes and the GM correction door. Speech still belongs to Discord."""

PLAYER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Shooting Gallery</title>
<style>
  :root { color-scheme: dark; }
  body { margin: 0; font: 16px/1.4 system-ui, sans-serif; background: #1a120c; color: #f3e6d0; }
  header, main { padding: 16px 20px; }
  header { background: #2a1c12; border-bottom: 1px solid #6b4a2a; }
  h1 { margin: 0 0 4px; font-size: 22px; }
  .muted { color: #c8b497; }
  .grid { display: grid; grid-template-columns: 320px 1fr; gap: 16px; }
  .sheet { max-height: 380px; overflow: auto; white-space: pre-wrap; font: 14px/1.35 ui-monospace, monospace; }
  .card { background: #2c2118; border: 1px solid #6b4a2a; border-radius: 8px; padding: 12px; margin-bottom: 12px; }
  .hp { height: 8px; background: #3a2a1c; border-radius: 4px; overflow: hidden; }
  .hp span { display: block; height: 100%; background: #c4542c; }
  .log { min-height: 180px; white-space: pre-wrap; }
  .you { color: #f3e6d0; }
  .system { color: #d7c4a3; }
  .gm { color: #f0d78c; }
  .roll { color: #9fd0c3; }
  form, .row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  input, button, select { font: inherit; padding: 8px 10px; border-radius: 6px; border: 1px solid #6b4a2a; background: #1a120c; color: inherit; }
  button { background: #c4542c; color: #1a120c; border: 0; cursor: pointer; }
  button.quiet { background: #3a2a1c; color: #f3e6d0; }
  @media (max-width: 800px) { .grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<header>
  <h1 id="room">Shooting Gallery</h1>
  <p class="muted" id="round"></p>
</header>
<main>
  <pre id="sheet" class="card sheet"></pre>
  <div class="grid">
    <section>
      <div class="card" id="self"></div>
      <div id="enemies"></div>
    </section>
    <section>
      <div class="card log" id="log" aria-live="polite"></div>
      <form id="line-form">
        <label for="line">What you do</label>
        <input id="line" name="line" size="50" autocomplete="off" placeholder="I get behind the sandbags, then I cast eldritch blast at the first mannequin">
        <button type="submit">Send</button>
      </form>
      <p class="row">
        <button type="button" class="quiet" data-line="I get behind the sandbags, then I cast eldritch blast at the first mannequin">Cover, then Eldritch Blast</button>
        <button type="button" class="quiet" data-line="I swing the mop at the first mannequin">Swing the mop</button>
        <button type="button" class="quiet" data-line="I cast witch bolt at the first mannequin">Witch Bolt</button>
        <button type="button" class="quiet" data-line="I pick up the body and swing it at the other mannequin">Swing the body</button>
        <button type="button" class="quiet" data-line="I end turn">End turn</button>
      </p>
      <form id="seat-form" class="card">
        <strong>Or seat a different Crawler</strong>
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
    </section>
  </div>
</main>
<script>
const logEl = document.getElementById("log");
function bar(current, max) {
  const pct = max ? Math.max(0, Math.min(100, current / max * 100)) : 0;
  const wrap = document.createElement("div");
  wrap.className = "hp";
  const span = document.createElement("span");
  span.style.width = pct + "%";
  wrap.appendChild(span);
  return wrap;
}
function card(title, lines, hp) {
  const el = document.createElement("div");
  el.className = "card";
  const h = document.createElement("strong");
  h.textContent = title;
  el.appendChild(h);
  if (hp) el.appendChild(bar(hp[0], hp[1]));
  for (const line of lines) {
    const p = document.createElement("div");
    p.textContent = line;
    el.appendChild(p);
  }
  return el;
}
function pip(on, label) { return (on ? "ready" : "spent") + " " + label; }
function render(data) {
  document.getElementById("room").textContent = data.room;
  document.getElementById("round").textContent = "Round " + data.round + (data.gallery_clear ? " · gallery clear" : "");
  const c = data.crawler;
  document.getElementById("sheet").textContent = (c.card_text || "").replaceAll("**", "");
  const self = document.getElementById("self");
  self.replaceChildren(card(c.name + " · " + c.class_name + " " + c.level, [
    "HP " + c.hp + "/" + c.hp_max + (c.temp_hp ? " +" + c.temp_hp + " temp" : "") + "  AC " + c.ac + (c.ac_bonus ? "+" + c.ac_bonus : "") + (c.cover ? "  cover " + c.cover : ""),
    pip(c.action, "action") + " · " + pip(c.bonus, "bonus") + " · " + pip(c.object, "object"),
    "Movement " + c.movement_left + " ft" + (c.hidden ? " · hidden" : ""),
    (c.attacks[0] ? c.attacks[0].name + " " + c.attacks[0].damage : "")
  ], [c.hp, c.hp_max]));
  const foes = document.getElementById("enemies");
  foes.replaceChildren();
  for (const enemy of data.enemies) {
    const attacks = (enemy.attacks || []).map((atk) => atk.name + ": +" + atk.to_hit + ", " + atk.damage + " " + atk.type + ", " + atk.kind);
    foes.appendChild(card(enemy.name, [
      enemy.spoken_name,
      enemy.system_line || "",
      "HP " + enemy.hp + "/" + enemy.hp_max + "  AC " + enemy.ac + (enemy.cover ? "  cover " + enemy.cover : ""),
      enemy.picture
    ].concat(attacks), [enemy.hp, enemy.hp_max]));
  }
  logEl.replaceChildren();
  for (const entry of data.log) {
    const p = document.createElement("div");
    p.className = (entry.voice || "").toLowerCase();
    p.textContent = entry.text;
    logEl.appendChild(p);
  }
  logEl.scrollTop = logEl.scrollHeight;
}
async function refresh() {
  const res = await fetch("/api/player");
  render(await res.json());
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
document.querySelectorAll("[data-line]").forEach((button) => {
  button.addEventListener("click", () => send(button.getAttribute("data-line")));
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
  if (res.ok) render(data.view);
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
  body { margin: 0; font: 16px/1.4 system-ui, sans-serif; background: #121418; color: #e6e1d6; }
  header, main { padding: 16px 20px; }
  header { background: #1c222b; border-bottom: 1px solid #3d4a5c; }
  h1 { margin: 0 0 4px; font-size: 22px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .card { background: #1c222b; border: 1px solid #3d4a5c; border-radius: 8px; padding: 12px; margin-bottom: 12px; }
  pre, #cards { white-space: pre-wrap; font: inherit; margin: 0; }
  form, .row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  input, button, select { font: inherit; padding: 8px 10px; border-radius: 6px; border: 1px solid #3d4a5c; background: #121418; color: inherit; }
  button { background: #d7c4a3; color: #121418; border: 0; cursor: pointer; }
  .note { color: #d7c4a3; }
  @media (max-width: 800px) { .grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<header>
  <h1>Table</h1>
  <p class="note">Every card and the raw line. Players do not get this page.</p>
</header>
<main>
  <div class="row">
    <button type="button" id="undo">Undo last resolution</button>
    <form id="fix">
      <label>Combatant <select id="who" name="who"></select></label>
      <label>HP <input id="hp" name="hp" type="number" min="0" value="0"></label>
      <button type="submit">Set hit points</button>
    </form>
    <span id="note"></span>
  </div>
  <div class="grid">
    <section class="card"><strong>Heard</strong><pre id="raw"></pre></section>
    <section class="card"><strong>Spoken back</strong><pre id="log"></pre></section>
  </div>
  <section class="card"><strong>GM note from the room stub</strong><pre id="secret"></pre></section>
  <section class="card" id="cards"></section>
</main>
<script>
function render(data) {
  document.getElementById("raw").textContent = data.raw.join("\\n");
  document.getElementById("log").textContent = data.log.map((entry) => entry.text).join("\\n");
  document.getElementById("secret").textContent = data.gm_note || "";
  const cards = document.getElementById("cards");
  const lines = [data.crawler.name + " " + data.crawler.hp + "/" + data.crawler.hp_max];
  const select = document.getElementById("who");
  const previous = select.value;
  select.replaceChildren();
  function add(id, name) {
    const option = document.createElement("option");
    option.value = id;
    option.textContent = name;
    select.appendChild(option);
  }
  add(data.crawler.id, data.crawler.name);
  for (const enemy of data.enemies) {
    lines.push(enemy.name + " " + enemy.hp + "/" + enemy.hp_max + " AC " + enemy.ac);
    add(enemy.id, enemy.name);
  }
  if (previous) select.value = previous;
  cards.textContent = lines.join("\\n");
}
async function refresh() {
  const res = await fetch("/api/gm");
  render(await res.json());
}
document.getElementById("undo").addEventListener("click", async () => {
  const res = await fetch("/api/undo", {method: "POST"});
  const data = await res.json();
  document.getElementById("note").textContent = res.ok ? "Undone." : (data.error || "nothing to undo");
  if (res.ok) render(data.view);
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
  if (res.ok) render(data.view);
});
refresh();
setInterval(refresh, 1000);
</script>
</body>
</html>
"""
