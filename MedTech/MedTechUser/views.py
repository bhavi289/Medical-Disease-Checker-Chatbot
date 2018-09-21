from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def home(request):
    return render(request, 'MedTechUser/home.html')

def analyze_and_reply(message):
    if message is not None:
        print(message)
        reply = 'REPLY THIS'
        return reply

def sendMessage(request):
    context = ''
    if request.is_ajax():
        reply = analyze_and_reply(request.POST.get('message', None))
        context = { 'reply': reply }
        res = JsonResponse(context, status=200)
        res['Access-Control-Allow-Origin']="*"
        return res
    else:
        context = { 'error': 'ERROR MESSAGE' }
        res = JsonResponse(context, status=400)
        return res