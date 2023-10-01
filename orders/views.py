from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from orders.models import Order
from orders.forms import OrderForm
from customers.models import Customer


@login_required
def orders_list(request):
    if request.user.groups.filter(name='Manager'):
        orders = Order.objects.all()
        return render(request, 'orders/orders_list.html', {'orders': orders})
    elif request.user.groups.filter(name='Customer'):
        try:
            customer = Customer.objects.get(email=request.user.email)
            orders = Order.objects.filter(customer=customer)
            return render(
                request, 'orders/orders_list.html', {'orders': orders}
            )
        except ObjectDoesNotExist:
            return HttpResponse("You haven't orders")
    else:
        return HttpResponseForbidden(
            "You don't have permissions to view orders", status=403
        )


@login_required
def create_order(request):
    if not request.user.groups.filter(name='Customer'):
        return HttpResponse("You don't have permission to create orders")
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            customer, created = Customer.objects.get_or_create(
                email=request.user.email
            )
            order.customer = customer
            order.save()
            success_message = f'Order {order.id} created!'
            messages.success(request, success_message)
            return redirect('orders_list')
    else:
        form = OrderForm(initial={'customer': request.user.email})
    return render(request, 'orders/create_order.html', {'form': form})
