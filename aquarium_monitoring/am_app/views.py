from django.shortcuts import render
from .models import WaterLevel
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timezone import localtime

def index(request):
    # latest_data = WaterLevel.objects.order_by('-timestamp').first()
    latest_data = WaterLevel.objects.latest('timestamp')
    context = {
        'data': latest_data
    }
    return render(request, 'am_app/index.html', {'data': latest_data})

def get_latest_data(request):
    try:
        latest_data = WaterLevel.objects.latest('timestamp')
        data = {
            'distance': latest_data.distance,
            'ph_value': latest_data.ph_value,
            'tds_value': latest_data.tds_value,
            'timestamp': localtime(latest_data.timestamp).strftime('%B %d, %Y, %I:%M %p')
        }
        return JsonResponse(data)
    except WaterLevel.DoesNotExist:
        return JsonResponse({'error': 'No data available'}, status=404)


@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            WaterLevel.objects.create(
                distance=float(data['distance']),
                ph_value=float(data['ph']),
                tds_value=float(data['tds'])
            )
            # distance = float(data.get('distance_cm'))
            # WaterLevel.objects.create(distance_cm=distance)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
