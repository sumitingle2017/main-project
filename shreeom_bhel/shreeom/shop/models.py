from django.db import models

class MenuItem(models.Model):
    CATS = [("bhel","Bhel"),("puri","Puri"),("namkeen","Namkeen"),("chivda","Chivda"),("snacks","Snacks"),("drinks","Drinks")]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATS, default="bhel")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    available = models.BooleanField(default=True)
    class Meta: ordering = ["category","name"]
    def __str__(self): return self.name

class Order(models.Model):
    STATUS = [("new","New"),("preparing","Preparing"),("ready","Ready"),("done","Done")]
    SOURCE = [("online","Online"),("counter","Counter")]
    PAY = [("cash","Cash"),("online","Online")]
    PSTATUS = [("pending","Pending"),("paid","Paid")]
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    source = models.CharField(max_length=10, choices=SOURCE, default="online")
    payment_method = models.CharField(max_length=10, choices=PAY, default="cash")
    payment_status = models.CharField(max_length=10, choices=PSTATUS, default="pending")
    status = models.CharField(max_length=10, choices=STATUS, default="new")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-id"]

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    qty = models.PositiveIntegerField()

    @property
    def amount(self):
        return self.price * self.qty
