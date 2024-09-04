from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def clear_modal_data(request):
  if request.method == 'POST':
    request.session.pop('modal_data', None)
    return JsonResponse({'status': 'success'})
  return JsonResponse({'status': 'error'}, status=400)