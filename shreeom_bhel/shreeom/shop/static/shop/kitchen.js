let lastMax = 0, first = true, soundOn = false, ctx;
const token = () => document.querySelector('[name=csrfmiddlewaretoken]').value;
document.getElementById('sound').onclick = e => {
  ctx = new (window.AudioContext || window.webkitAudioContext)(); soundOn = true;
  e.target.textContent = '🔔 Sound ON'; beep();
};
function beep() {
  if (!soundOn) return;
  [0, 0.3, 0.6].forEach(t => { const o = ctx.createOscillator(), g = ctx.createGain();
    o.frequency.value = 880; o.connect(g); g.connect(ctx.destination);
    o.start(ctx.currentTime + t); o.stop(ctx.currentTime + t + 0.2); });
}
const NEXT = { new: ['preparing', 'Start Making'], preparing: ['ready', 'Mark Ready'], ready: ['done', 'Handed Over'] };
async function setStatus(id, s) {
  await fetch(ST + id + '/' + s + '/', { method: 'POST', headers: { 'X-CSRFToken': token() } }); load();
}
async function load() {
  const r = await fetch(API);
  if (r.redirected || !r.ok) {
    document.getElementById('orders').innerHTML = '<p class="err">Login nahi ahe. /login/ madhe login kara.</p>';
    return;
  }
  const d = await r.json();
  const max = Math.max(0, ...d.orders.map(o => o.id));
  if (!first && max > lastMax) { beep(); if (navigator.vibrate) navigator.vibrate(300); }
  lastMax = Math.max(lastMax, max); first = false;
  document.getElementById('orders').innerHTML = d.orders.map(o => `
    <div class="card st-${o.status}"><div class="row"><h3>#${o.id} ${o.name}</h3><small>${o.time}</small></div>
    <p class="muted">${o.source} • ${o.pay} (${o.paid})</p>
    <ul>${o.items.map(i => `<li>${i}</li>`).join('')}</ul>
    <button class="btn" onclick="setStatus(${o.id},'${NEXT[o.status][0]}')">${NEXT[o.status][1]}</button></div>`).join('')
    || '<p class="muted">Navin order nahi.</p>';
}
load(); setInterval(load, 4000);
