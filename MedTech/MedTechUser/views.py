from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from nltk.stem.lancaster  import LancasterStemmer
# import codecs
import csv
from . models import *
import stringdist
from django.db.models import Q
import random

count = 0

def home(request):
    global count
    return render(request, 'MedTechUser/index3.html', {'count':0})
    # if request.is_ajax():


def analyze_and_reply(message):
    if message is not None:
        print(message)
        reply = 'REPLY THIS'
        return reply

def sendMessage(request):
    context = ''
    if request.is_ajax():
        message = (request.POST.get('message', None))
        print(message.split(','))
        reply = analyze_and_reply(request.POST.get('message', None))
        # print (reply)
        
        context = { 'reply': reply }
        res = JsonResponse(context, status=200)
        res['Access-Control-Allow-Origin']="*"
        return res
    else:
        context = { 'error': 'ERROR MESSAGE' }
        res = JsonResponse(context, status=400)
        return res

def StemData(input):
    all_words = input.split(' ')
    stemmed_string = ''
    for word in all_words:
        st = LancasterStemmer()
        stemmed_string += str(st.stem(word))
    return stemmed_string  

def all_possible_string(feeling, original):
    if len(feeling) >= 3:
        dummy = feeling[:2]
        # print(dummy)
        for i in range(3,len(feeling)):
            dummy += feeling[i]
            # print (dummy[::-1])
            feeling_model = AllFeelings()
            feeling_model.name = original
            feeling_model.permuterm = dummy[::-1]
            feeling_model.save()
        all_possible_string(feeling[1:], original)
    else:
        return

def insertData(request):
    if request.method == 'GET':
        return render(request, 'MedTechUser/home.html')
    if request.method == 'POST':
        csvfile = request.FILES.get('data_file', False)
        for row in csvfile:
            stemmed = StemData(str(row)[2:-3])
            # print(stemmed, stemmed[-1:])
            all_possible_string(stemmed[::-1], str(row)[2:-3])

def all_string(symptom, final_results):
    # print(final_results)
    if len(symptom) >= 3:
        dummy = symptom[:3]
        results = AllFeelings.objects.filter(Q(permuterm__contains=dummy[::-1])|Q(permuterm=dummy[::-1])|Q(permuterm__startswith=dummy[::-1])|Q(permuterm__endswith=dummy[::-1]))
        final_results.extend(results)
        print(dummy)
        for i in range(3,len(symptom)):
            dummy += symptom[i]
            print(dummy)
            results = AllFeelings.objects.filter(Q(permuterm__contains=dummy[::-1])|Q(permuterm=dummy[::-1])|Q(permuterm__startswith=dummy[::-1])|Q(permuterm__endswith=dummy[::-1]))
            print(results)
            final_results.extend(results)
            # print("final_results", final_results)            
        returned_result = all_string(symptom[1:], final_results)
        return returned_result

    else:
        return final_results


def query_feeling(request):
    if request.method == 'GET':
        feeling = request.GET.get('feeling')
        stemmed_data = StemData(feeling)
        print(stemmed_data)
        final_results = []
        results = all_string(stemmed_data[::-1], final_results)
        final = list()
        feeling_result = list()
        for result in results:
            if str(result.name) not in feeling_result:
                final.append({'feeling':result.name})
                feeling_result.append(result.name)
        print(len(final))
    return HttpResponse(final)
    # return render(request, 'MedTechUser/feeling_reslt.html' ,{'final':final, })