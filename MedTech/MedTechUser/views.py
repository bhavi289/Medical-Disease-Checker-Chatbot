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
    TempSymptomsToDisease.objects.all().delete()
    TempxAllFeelings.objects.all().delete()
    TopDiseases.objects.all().delete()
    return render(request, 'MedTechUser/home.html', {'count':0})
    # if request.is_ajax():

def home2(request):
    global count
    TempSymptomsToDisease.objects.all().delete()
    TempxAllFeelings.objects.all().delete()
    TopDiseases.objects.all().delete()
    return render(request, 'MedTechUser/index3.html', {'count':0})


def analyze_and_reply(message):
    if message is not None:
        print(message)
        reply = 'REPLY THIS'
        return reply

def most_common(lst):
    return max(set(lst), key=lst.count)

def sendMessage(request):
    context = ''
    import itertools
    import operator

    if request.is_ajax():
        message = (request.POST.get('message', None))
        count = (request.POST.get('count', None))
        reply = ""
        print(message, count)
        if str(count) == '1':
            for part in message.split(','):
                print(part)
                global bs
                bs = SymptomsToDisease.objects.filter(Q(body_part__contains=part)|Q(body_part=part)|Q(body_part__startswith=part)|Q(body_part__endswith=part))
                for b in bs:
                    TempSymptomsToDisease(symptom = b.symptom, body_part=b.body_part, disease=b.disease).save()
            reply = "Great! I've identified the body parts - "+str(message)+". Now tell me how are you feeling in general?"
        elif count == '2':
            l = query_feeling(message)
            reply = "Let me know if you're feeling anything else like Dizziness or Nausea or Fever or Heavy.."
            # print ("l is ", l)
            for q in l:
                print (q)
                TempxAllFeelings(name = q['name'], disease = q['disease']).save()
        elif count == '3':
            try:
                x = TempSymptomsToDisease.objects.all()
                y = TempxAllFeelings.objects.all()
                li = []
                for i in x:
                    for j in y:
                        if i.disease == j.disease:
                            li.append(i.disease)
                print (li)
                top=[]
                most = most_common(li)
                top.append(most)

                li = [x for x in li if x != most]
                most = most_common(li)
                top.append(most)

                li = [x for x in li if x != most]
                most = most_common(li)
                top.append(most)
                
                print(top)

                for t in top:
                    TopDiseases(disease = t).save()

                tsd = TempSymptomsToDisease.objects.filter(disease = top[0])[0]
                reply = "Are you having "+ str(tsd.symptom)
            except:
                reply = "I'm sorry I dont seem to know your diseaese"
    
        elif count == '4':
            print("here")
            from textblob import TextBlob
            text = message
            blob = TextBlob(text)
            td = TopDiseases.objects.all()
            for sentence in blob.sentences:
                print(sentence.sentiment.polarity)
            print (message)
            if message.strip(' ')=="yes":
                print(len(td))
                print(td.last().disease)
                reply = str("you have") + str(td.last().disease)
                sp = Specialist.objects.filter(disease=td.last().disease)[0]
                if(sp):
                    reply += ". You must contact a " + sp.doctor
                    import webbrowser
                    webbrowser.open('https://www.google.co.in/search?q='+sp.doctor+'+near+me')
                    # print (reply)
                td.last().delete()
            else:
                tsd = TempSymptomsToDisease.objects.filter(disease = td.last().disease)[0]
                td.last().delete()
                reply = "Ok Do you have " + tsd.symptom
        
        elif count == '5':
            print("here")
            from textblob import TextBlob
            text = message
            blob = TextBlob(text)
            td = TopDiseases.objects.all()
            for sentence in blob.sentences:
                print(sentence.sentiment.polarity)
            if message.strip(' ')=="yes":
                print(len(td))
                print(td.last().disease)
                reply = str("you have") + str(td.last().disease)
                if(sp):
                    reply += ". You must contact a " + sp.doctor
                    import webbrowser
                    webbrowser.open('https://www.google.co.in/search?q='+sp.doctor+'+near+me')
                td.last().delete()
            else:
                tsd = TempSymptomsToDisease.objects.filter(disease = td.last().disease)[0]
                td.last().delete()

                reply = "Ok Do you have " + tsd.symptom
        
        elif count == '6':
            print("here")
            from textblob import TextBlob
            text = message
            blob = TextBlob(text)
            td = TopDiseases.objects.all()
            for sentence in blob.sentences:
                print(sentence.sentiment.polarity)
            if message.strip(' ')=="yes":
                print(len(td))
                print(td.last().disease)
                reply = str("you have") + str(td.last().disease)
                if(sp):
                    reply += ". You must contact a " + sp.doctor
                    import webbrowser
                    webbrowser.open('https://www.google.co.in/search?q='+sp.doctor+'+near+me')
                td.last().delete()
            else:
                reply = "I'm Sorry im not able to understand your disease. please try again"



            
                

                
        context = { 'reply': reply }
        print(context)
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
            print (row)
            row = str(row).split(',')

            Specialist(disease = row[0][2:], doctor = row[1]).save()
            # print(row[0], row[1], row[2])
            # instance = SymptomsToDisease()
            # instance.symptom = str(row[2])
            # instance.body_part = str(row[1])
            # instance.disease = str(row[0])
            # instance.save()
        return HttpResponse("done")
        
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
        #     count += 1
        # return HttpResponse("success")

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


def query_feeling(feeling):
    # if request.method == 'GET':
    st = LancasterStemmer()
    # feeling = request.GET.get('feeling')
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
            final.append({'name':result.name, "disease":result.disease})
            feeling_result.append(result.name)
    print(len(final))
    return (final)
    # return render(request, 'MedTechUser/feeling_reslt.html' ,{'final':final, })