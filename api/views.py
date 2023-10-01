import json
from django.http import JsonResponse, HttpRequest
from django.core.serializers import serialize
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from robots.models import Robot


@csrf_exempt
def robots_api(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        return get_robots(request)
    elif request.method == 'POST':
        return create_robot(request)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


def get_robots(request: HttpRequest) -> JsonResponse:
    robots = Robot.objects.all()
    serialized_robots = serialize('python', robots)
    response_data = {'robots': serialized_robots}
    return JsonResponse(response_data)


def create_robot(request: HttpRequest) -> JsonResponse:
    body = json.loads(request.body)

    if not body:
        return JsonResponse({'error': 'Request body is missing'}, status=400)

    try:
        model = body['model']
        version = body['version']
        created = body['created']
    except (KeyError, ValueError):
        return JsonResponse({'error': 'Invalid format data'}, status=400)

    serial = f'{model}-{version}'

    robot_data = {
        'serial': serial,
        'model': model,
        'version': version,
        'created': created,
    }

    robot = Robot(**robot_data)
    try:
        robot.full_clean()
        robot.save()
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    response_data = {
        'message': f'New robot {robot.serial} has been created with id {robot.id}',
    }
    return JsonResponse(response_data, status=201)


def update_robot(request: HttpRequest, robot_id: int) -> JsonResponse:
    body = json.loads(request.body)

    if not body:
        return JsonResponse({'error': 'Request body is missing'}, status=400)

    try:
        robot = Robot.objects.get(id=robot_id)
    except Robot.DoesNotExist:
        return JsonResponse({'error': f'Robot with id {robot_id} does not exist'}, status=404)

    try:
        model = body['model']
        version = body['version']
        created = body['created']
    except (KeyError, ValueError):
        return JsonResponse({'error': 'Invalid data format'}, status=400)

    serial = f'{model}-{version}'

    robot.serial = serial
    robot.model = model
    robot.version = version
    robot.created = created

    try:
        robot.full_clean()
        robot.save()
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    response_data = {
        'message': f'Robot {robot.serial} with id {robot.id} has been updated',
    }
    return JsonResponse(response_data)


def delete_robot(request: HttpRequest, robot_id: int) -> JsonResponse:
    try:
        robot = Robot.objects.get(id=robot_id)
    except Robot.DoesNotExist:
        return JsonResponse({'error': f'Robot with id {robot_id} does not exist'}, status=404)

    robot.delete()

    response_data = {
        'message': f'Robot with id {robot_id} has been deleted',
    }
    return JsonResponse(response_data)
