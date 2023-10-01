from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from robots.models import Robot
from robots.forms import RobotForm


@login_required
def robots_list(request):
    allowed_groups = ['Manager', 'Techspec']
    user_groups = request.user.groups.values_list('name', flat=True)

    if any(group in allowed_groups for group in user_groups):
        robots = Robot.objects.all()
        return render(request, 'robots/robots_list.html', {'robots': robots})
    else:
        return HttpResponseForbidden(
            "You don't have permission to view robots", status=403
        )


@login_required
def add_robot(request):
    if not request.user.groups.filter(name='Techspec'):
        return HttpResponseForbidden(
            "You don't have permission to add robots", status=403
        )
    if request.method == 'POST':
        form = RobotForm(request.POST)
        if form.is_valid():
            robot = form.save(commit=False)
            robot.serial = f'{robot.model}-{robot.version}'
            robot.save()
            return redirect('main')
    else:
        form = RobotForm()
    return render(request, 'robots/add_robot.html', {'form': form})
