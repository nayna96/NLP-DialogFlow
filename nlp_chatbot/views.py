from django.shortcuts import render
from . import ml
from django.http import JsonResponse, HttpResponse
import json
from json import dumps
import os

unique_values = ml.get_unique_values()
datapath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))

def home(request):
    #unique_values_json = dumps(unique_values)
    #ml.write_json(unique_values_json)
    return render(request, "index.html")

def dashboard(request):
    with open(datapath + '/insights.json') as f:
        data = json.load(f)
    
    univariate_insights = data["univariate"]
    bivariate_insights = data["bivariate"]

    cols = list(unique_values.keys())
    cols= [col.replace("_", " ") for col in cols]

    return render(request, "dashboard.html", {
        'cols': cols,
        'univariate_insights': univariate_insights,
        'bivariate_insights': bivariate_insights
    })

def aiml_models(request):
    return render(request, "aiml_models.html")

def webhook(request):
    if request.method == "POST":
        req = request.get_json(silent=True, force=True)
        
        sum = 0
        
        query_result = req.get('queryResult')
        #num1 = int(query_result.get('parameters').get('number'))
        #num2 = int(query_result.get('parameters').get('number1'))
        description = query_result.get('parameters').get('description')
        num1 = 3
        num2 = 4
        
        sum = str(num1 + num2)
            
        return{ 
            "fulfillmentMessages": 
            [
                {"text": 
                    {
                        "text": 'The sum of the two numbers is: ' + sum
                    } 
                }
            ]
        }
    else:
        return HttpResponse("GET request")
