import json
from datetime import datetime, time, timedelta
from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required as staff
from django.db.models import Q, Sum, Count, F, DecimalField
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import MenuItemForm, OrderForm, OrderItemFormSet
from .models import MenuItem, Order, OrderItem

def menu(request):
    q = request.GET.get("q", "").strip(); cat = request.GET.get("cat", "")
    items = MenuItem.objects.filter(available=True)
    if q: items = items.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if cat: items = items.filter(category=cat)
    return render(request, "shop/menu.html", {"items": items, "q": q, "cat": cat, "cats": MenuItem.CATS})

@require_POST
def place_order(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Login required"}, status=403)
    d = json.loads(request.body); rows = []; total = Decimal(0)
    for it in d.get("items", []):
        m = MenuItem.objects.filter(id=it.get("id"), available=True).first()
        qty = int(it.get("qty", 0))
        try:
            price = Decimal(str(it.get("price", m.price if m else 0)))
        except Exception:
            price = m.price if m else Decimal(0)
        if price < 0: price = m.price
        if m and qty > 0: rows.append((m, qty, price)); total += price * qty
    if not rows: return JsonResponse({"error": "Cart is empty"}, status=400)
    pay = d.get("payment") if d.get("payment") in ("cash", "online") else "cash"
    o = Order.objects.create(customer_name=(d.get("name") or "Customer")[:100], phone=(d.get("phone") or "")[:15],
        payment_method=pay, total=total, source="counter")
    for m, qty, price in rows: OrderItem.objects.create(order=o, name=m.name, price=price, qty=qty)
    url = reverse("pay", args=[o.id]) if pay == "online" else reverse("done", args=[o.id])
    return JsonResponse({"redirect": url})

def pay(request, pk):
    o = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        # TODO: Razorpay/PhonePe verification yethe lava. Sadhya demo - "Pay" dabla ki paid hoto.
        o.payment_status = "paid"; o.save()
        return redirect("done", pk=o.id)
    return render(request, "shop/pay.html", {"o": o})

def done(request, pk):
    return render(request, "shop/done.html", {"o": get_object_or_404(Order, pk=pk)})

@staff
def counter(request):
    return render(request, "shop/counter.html", {"items": MenuItem.objects.filter(available=True)})

@staff
def manage(request):
    return render(request, "shop/manage.html", {"items": MenuItem.objects.all()})

@staff
def item_edit(request, pk=None):
    obj = get_object_or_404(MenuItem, pk=pk) if pk else None
    form = MenuItemForm(request.POST or None, instance=obj)
    if form.is_valid(): form.save(); return redirect("manage")
    return render(request, "shop/form.html", {"form": form, "obj": obj})

@staff
def item_delete(request, pk):
    obj = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST": obj.delete(); return redirect("manage")
    return render(request, "shop/confirm_delete.html", {"obj": obj})

@staff
def kitchen(request):
    return render(request, "shop/kitchen.html")

@staff
def kitchen_api(request):
    qs = Order.objects.exclude(status="done").filter(Q(payment_method="cash") | Q(payment_status="paid") | Q(source="counter")).prefetch_related("items")
    data = [{"id": o.id, "name": o.customer_name, "source": o.get_source_display(), "status": o.status,
             "pay": o.get_payment_method_display(), "paid": o.payment_status,
             "time": timezone.localtime(o.created).strftime("%I:%M %p"),
             "items": [f"{i.qty} x {i.name}" for i in o.items.all()]} for o in qs]
    return JsonResponse({"orders": data})

@staff
@require_POST
def order_status(request, pk, status):
    o = get_object_or_404(Order, pk=pk)
    if status in ("preparing", "ready", "done"):
        o.status = status
        if status == "done": o.payment_status = "paid"
        o.save()
    return JsonResponse({"ok": True})


@staff
def report(request):
    try:
        day = datetime.strptime(request.GET.get("date", ""), "%Y-%m-%d").date()
    except ValueError:
        day = timezone.localdate()
    valid = Q(payment_method="cash") | Q(payment_status="paid")

    def day_orders(d):
        start = timezone.make_aware(datetime.combine(d, time.min))
        return Order.objects.filter(created__gte=start, created__lt=start + timedelta(days=1))

    all_orders = day_orders(day)
    qs = all_orders.filter(valid)
    summary = qs.aggregate(count=Count("id"), total=Sum("total"))
    cash = qs.filter(payment_method="cash").aggregate(count=Count("id"), total=Sum("total"))
    online = qs.filter(payment_method="online").aggregate(count=Count("id"), total=Sum("total"))
    items = (OrderItem.objects.filter(order__in=qs).values("name")
             .annotate(total_qty=Sum("qty"),
                       amount=Sum(F("price") * F("qty"), output_field=DecimalField(max_digits=12, decimal_places=2)))
             .order_by("-total_qty"))
    week = []
    for n in range(7):
        d = day - timedelta(days=n)
        a = day_orders(d).filter(valid).aggregate(count=Count("id"), total=Sum("total"))
        week.append({"date": d, "count": a["count"], "total": a["total"] or 0})
    orders = all_orders.prefetch_related("items")
    return render(request, "shop/report.html", {"day": day, "summary": summary, "cash": cash,
                                                "online": online, "items": items, "week": week, "orders": orders})
@staff
def order_edit(request, pk):
    o = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=o)
    fs = OrderItemFormSet(request.POST or None, instance=o)
    if request.method == "POST" and form.is_valid() and fs.is_valid():
        form.save(); fs.save()
        o.total = sum(i.price * i.qty for i in o.items.all()); o.save()
        return redirect(f"{reverse('report')}?date={timezone.localtime(o.created).date()}")
    return render(request, "shop/order_edit.html", {"o": o, "form": form, "fs": fs})

@staff
@require_POST
def order_delete(request, pk):
    o = get_object_or_404(Order, pk=pk)
    d = timezone.localtime(o.created).date()
    o.delete()
    return redirect(f"{reverse('report')}?date={d}")
def bill(request, pk):
    return render(request, "shop/bill.html", {"o": get_object_or_404(Order, pk=pk)})