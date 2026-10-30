from django import forms
from .models import MenuItem
from django.forms import inlineformset_factory
from .models import Order, OrderItem
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name","category","price","description","available"]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "phone", "payment_method", "payment_status", "status"]

OrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=["name", "price", "qty"], extra=1, can_delete=True)