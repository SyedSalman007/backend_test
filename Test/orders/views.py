from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .models import Orders
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework import status

# Create your views here.

def home(request):
  return render(request, 'order/home.html', {})

def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "User created successfully!")
            return redirect("add_user")

    return render(request, "order/add_user.html")

class LoginInterfaceView(LoginView):
    template_name = 'order/login.html'

class LogoutInterfaceView(LogoutView):
    template_name = 'order/logout.html'

def create_order(request):
    if request.method == "POST":
        email = request.POST.get("email")  # Get email from form
        product_name = request.POST.get("product_name")
        product_price = request.POST.get("product_price")
        quantity = request.POST.get("quantity")

        try:
            user = User.objects.get(email=email)
            Orders.objects.create(email=email, product_name=product_name, product_price=product_price, quantity=quantity)
            messages.success(request, "Order created successfully!")
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist!")

        return redirect("order_list")

    return render(request, "order/orders_form.html")

# def order_list(request):
#     orders = Orders.objects.values("email", "product_name", "product_price", "quantity")
#     return render(request, "order/orders_list.html", {"orders": orders})

class OrderListView(LoginRequiredMixin, ListView):
    model = Orders
    template_name = "order/orders_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Orders.objects.filter(email=self.request.user.email)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Orders
    fields = ["product_name", "product_price", "quantity"]
    template_name = "order/orders_update.html"
    success_url = reverse_lazy("order_list")

    def test_func(self):
        """Ensure the user can only edit their own orders"""
        order = self.get_object()
        return order.email == self.request.user.email

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Orders
    template_name = "order/orders_confirm_delete.html"
    success_url = reverse_lazy("order_list")

    def test_func(self):
        """Ensure the user can only delete their own orders"""
        order = self.get_object()
        return order.email == self.request.user.email

class UserEmailListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """Return all user emails (only for super admins)."""
        emails = User.objects.values_list("email", flat=True)
        return Response({"emails": list(emails)}, status=200)

class UserOrdersView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """Retrieve orders for the given list of email addresses (Super Admins Only)"""
        emails = request.data.get("emails", [])

        if not isinstance(emails, list) or not all(isinstance(email, str) for email in emails):
            return Response({"error": "Invalid email list format"}, status=status.HTTP_400_BAD_REQUEST)

        orders = Orders.objects.filter(email__in=emails).values("email", "product_name", "product_price", "quantity")

        return Response({"orders": list(orders)}, status=status.HTTP_200_OK)
