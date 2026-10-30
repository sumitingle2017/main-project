from django.urls import path
from django.contrib.auth import views as auth
from . import views as v
urlpatterns = [
    path("", v.menu, name="menu"),
    path("place/", v.place_order, name="place"),
    path("pay/<int:pk>/", v.pay, name="pay"),
    path("done/<int:pk>/", v.done, name="done"),
    path("login/", auth.LoginView.as_view(template_name="shop/login.html"), name="login"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),
    path("counter/", v.counter, name="counter"),
    path("manage/", v.manage, name="manage"),
    path("manage/add/", v.item_edit, name="item_add"),
    path("manage/<int:pk>/edit/", v.item_edit, name="item_edit"),
    path("manage/<int:pk>/delete/", v.item_delete, name="item_delete"),
    path("kitchen/", v.kitchen, name="kitchen"),
    path("kitchen/api/", v.kitchen_api, name="kitchen_api"),
    path("order/<int:pk>/<str:status>/", v.order_status, name="order_status"),
    path("report/", v.report, name="report"),
    path("report/order/<int:pk>/edit/", v.order_edit, name="order_edit"),
    path("report/order/<int:pk>/delete/", v.order_delete, name="order_delete"),
    path("bill/<int:pk>/", v.bill, name="bill"),
]
