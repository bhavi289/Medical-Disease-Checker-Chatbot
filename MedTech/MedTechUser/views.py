from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def home(request):
    return render(request, 'MedTechUser/home.html')

def sendMessage(request):
    context = ''
    if request.is_ajax():
        reply = 'REPLY HERE'
        context = { 'reply': 'REPLY HERE' }
        res = JsonResponse(context, status=200)
        res['Access-Control-Allow-Origin']="*"
        return res
    else:
        context = { 'error': 'ERROR MESSAGE' }
        res = JsonResponse(context, status=400)
        return res