from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pickle
# Create your views here.

def index(request):
    return render(request,'project.html')

def predict(request):
    
    if request.method == 'POST':
        model = pickle.load(open('static/SVM_pipeline.pkl', 'rb'))
        features = []
        features.append(request.POST.get('founded_at'))
        features.append(request.POST.get('funding_rounds'))
        features.append(request.POST.get('total_funding_usd'))
        features.append(request.POST.get('milestones'))
        features.append(request.POST.get('relationships'))
        features = list(map(float, features))
        features = np.array(features).reshape(1, len(features))
        prediction = model.predict(features)

        if prediction == 1:
            result = 'operating'
        elif prediction == 2:
            result = 'acquired'
        elif prediction == 3:
            result = 'closed'
        elif prediction == 4:
            result = 'ipo'
        else:
            result = 'error'
        
        
    return render(request,'project.html',{'prediction':result})