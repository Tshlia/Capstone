from django.shortcuts import render
from .models import WaterLevel
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    latest_data = WaterLevel.objects.order_by('-timestamp').first()
    context = {
        'data': latest_data
    }
    return render(request, 'am_app/index.html', {'data': latest_data})

# def dashboard(request):
#     measurements = WaterLevel.objects.all().order_by('-timestamp')[:20]
#     return render(request, 'am_app/dashboard.html', {'measurements': measurements})

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
