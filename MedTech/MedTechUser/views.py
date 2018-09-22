from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from nltk.stem.lancaster  import LancasterStemmer
# import codecs
import csv
from . models import *
import stringdist
from django.db.models import Q
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
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
    # all_words = input.split(' ')
    word_tokens = word_tokenize(input)
    stemmed_string = ''
    # nltk.download('stopwords')
    # nltk.download('punkt')
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend([',','!','.','@','`','~','#', '$', '%', '^', '&', '*', '(', ')', '-','_','=','+','[','{','}',']',';',':','<','>','/','?'])

    # filtered_sentence = [w for w in word_tokens if not w in stopwords]
    st = LancasterStemmer()
    for word in word_tokens:
        stemmed_word = st.stem(word)
        if stemmed_word not in stopwords:
            stemmed_string += stemmed_word
    return stemmed_string  

def all_possible_string(feeling, original, disease):
    if len(feeling) >= 3:
        dummy = feeling[:3]
        # print(dummy)
        for i in range(3,len(feeling)):
            dummy += feeling[i]
            # print (dummy[::-1])
            feeling_model = AllFeelings()
            feeling_model.name = original
            feeling_model.permuterm = dummy[::-1]
            feeling_model.disease = disease
            feeling_model.save()
        all_possible_string(feeling[1:], original, disease)
    else:
        return

def insertData(request):
    if request.method == 'GET':
        return render(request, 'MedTechUser/home.html')
    if request.method == 'POST':
        csvfile = request.FILES.get('data_file', False)
        count = 0
        for row in csvfile:
            row = str(row)[2:-3].split('|')
            print(row[0], row[1], row[2])
            instance = SymptomsToDisease()
            instance.symptom = str(row[2])
            instance.body_part = str(row[1])
            instance.disease = str(row[0])
            instance.save()
        #     array = str(row).split('|')
        #     # print(array[0].replace("b'", ''), " ---> ", array[1].replace("\r\n'", ''))
        #     sym = str(array[1]).split(',')
        #     for i in range(0,len(sym)):
        #         if i == len(sym)-1:
        #             body_part = AllBodyParts()
        #             body_part.permuterm = str(sym[i])[:-5]
        #             # print(str(sym[i])[:-5])
        #             body_part.name = str(array[0]).replace("b'", '')
        #             body_part.save()
        #         else:
        #             body_part = AllBodyParts()
        #             body_part.permuterm = str(sym[i])
        #             # print(sym[i])
        #             body_part.name = str(array[0]).replace("b'", '')
        #             body_part.save()
        # return HttpResponse("success")
            # row = str(row)[2:-3].split('|')
            # feeling_model = AllFeelings()
            # feeling_model.name = str(row[1])
            # feeling_model.disease = str(row[0])
            # feeling_model.save()
            # print(count)
            # # stemmed = StemData(str(row[1]))
            # # # print(stemmed, stemmed[-1:])
            # # all_possible_string(stemmed[::-1], str(row[1]), str(row[0]))
            count += 1
        return HttpResponse("success")

def all_string(symptom, final_results):
    # print(final_results)
    if len(symptom) >= 3:
        dummy = symptom[:3]
        results = AllFeelings.objects.filter(Q(name__contains=dummy[::-1])|Q(name=dummy[::-1])|Q(name__startswith=dummy[::-1])|Q(name__endswith=dummy[::-1]))
        final_results.extend(results)
        print(dummy)
        for i in range(3,len(symptom)):
            dummy += symptom[i]
            print(dummy)
            results = AllFeelings.objects.filter(Q(name__contains=dummy[::-1])|Q(name=dummy[::-1])|Q(name__startswith=dummy[::-1])|Q(name__endswith=dummy[::-1]))
            print(results)
            final_results.extend(results)
            # print("final_results", final_results)            
        returned_result = all_string(symptom[1:], final_results)
        return returned_result

    else:
        return final_results


def query_feeling(request):
    if request.method == 'GET':
        st = LancasterStemmer()
        feeling = request.GET.get('feeling')
        word_tokens = word_tokenize(feeling)
        stemmed_string = ''
        # nltk.download('stopwords')
        # nltk.download('punkt')
        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.extend([',','!','.','@','`','~','#', '$', '%', '^', '&', '*', '(', ')', '-','_','=','+','[','{','}',']',';',':','<','>','/','?'])
        query = ''
        for word in word_tokens:
            if word not in stopwords:
                query += st.stem(word)
        stemmed_data = query
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