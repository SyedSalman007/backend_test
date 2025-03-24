from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('add/', views.add_user, name='add_user'),
  path('login/', views.LoginInterfaceView.as_view(), name='login_user'),
  path('logout/', views.LogoutInterfaceView.as_view(), name='logout_user'),
  path('create/', views.create_order, name='create'),
  path('orders/', views.OrderListView.as_view(), name='order_list'),
  path("orders/update/<int:pk>/", views.OrderUpdateView.as_view(), name="order_update"),
  path("orders/delete/<int:pk>/", views.OrderDeleteView.as_view(), name="order_delete"),
  path("users/emails/", views.UserEmailListView.as_view(), name="user-email-list"),
  path("orders/by-emails/", views.UserOrdersView.as_view(), name="user-orders"),
]