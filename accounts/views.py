from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import Group
from accounts.forms import CustomUserCreationForm


def signup_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        role = form.cleaned_data['role']
        user = form.save()
        group_mapping = {
            'tech': 'Techspec',
            'manager': 'Manager',
            'customer': 'Customer'
        }
        group_name = group_mapping.get(role)
        if group_name:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        return redirect(reverse('login'))
    return render(request, 'registration/signup.html', {'form': form})


def main_view(request):
    return render(request, 'main.html')
