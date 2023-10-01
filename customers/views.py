from django.shortcuts import render, HttpResponse
from customers.models import Customer


def customers_list(request):
    if not request.user.groups.filter(name='Manager'):
        return HttpResponse("You don't have permission to view customers")
    customers = Customer.objects.all()
    return render(
        request, 'customers/customers_list.html', {'customers': customers}
    )
