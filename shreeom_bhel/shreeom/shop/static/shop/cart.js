const cart = {};
const $ = s => document.querySelector(s);
const token = () => document.querySelector('[name=csrfmiddlewaretoken]').value;
function updateTotal() {
  let t = 0;
  for (const id in cart) t += cart[id].price * cart[id].qty;
  $('#total').textContent = Number(t.toFixed(2));
}
function setPrice(id, v) {
  cart[id].price = Math.max(0, parseFloat(v) || 0);
  updateTotal();
}
function render() {
  const ids = Object.keys(cart);
  $('#cart-list').innerHTML = ids.length ? ids.map(id => {
    const c = cart[id];
    return `<div class="crow"><span class="cn">${c.name}</span>
      <span class="cq"><button onclick="chg(${id},-1)">−</button> ${c.qty} <button onclick="chg(${id},1)">+</button></span>
      <span class="cp">₹<input type="number" min="0" step="any" value="${c.price}" oninput="setPrice(${id},this.value)"></span></div>`;
  }).join('') : '<p class="muted">Cart empty</p>';
  updateTotal();
}
function chg(id, d) { cart[id].qty += d; if (cart[id].qty <= 0) delete cart[id]; render(); }
document.querySelectorAll('.add').forEach(b => b.onclick = () => {
  const id = b.dataset.id;
  cart[id] = cart[id] || { name: b.dataset.name, price: parseFloat(b.dataset.price), qty: 0 };
  cart[id].qty++; render();
});
$('#place-btn').onclick = async () => {
  const items = Object.keys(cart).map(id => ({ id: +id, qty: cart[id].qty, price: cart[id].price }));
  if (!items.length) { $('#err').textContent = 'Adhi items add kara'; return; }
  const r = await fetch(PLACE_URL, { method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token() },
    body: JSON.stringify({ items, name: $('#cname').value, phone: $('#cphone').value,
      payment: document.querySelector('input[name=pay]:checked').value }) });
  const d = await r.json();
  if (d.redirect) location = d.redirect; else $('#err').textContent = d.error || 'Error';
};