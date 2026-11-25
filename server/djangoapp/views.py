import json
import requests
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .models import CarMake, CarModel
from .restapis import get_request, post_review, analyze_review_sentiments

@csrf_exempt
@require_POST
def login_user(request):
    try:
        data = json.loads(request.body)
        user = authenticate(request, username=data["userName"], password=data["password"])
    except (ValueError, KeyError, TypeError):
        return JsonResponse({"status":"Invalid request"}, status=400)
    if user is None:
        return JsonResponse({"status":"Invalid credentials"}, status=401)
    login(request,user)
    return JsonResponse({"userName":user.username,"status":"Authenticated"})

@csrf_exempt
def logout_request(request):
    logout(request)
    return JsonResponse({"status":"Logged out"})

@csrf_exempt
@require_POST
def registration(request):
    try:
        data=json.loads(request.body)
        username=data["userName"].strip()
        email=data["email"].strip()
        if not username or not email:
            raise ValueError("Username and email are required")
        user=User(username=username,first_name=data["firstName"],last_name=data["lastName"],email=email)
        validate_password(data["password"],user)
        user.set_password(data["password"])
        user.save()
        login(request,user)
        return JsonResponse({"userName":username,"status":"Authenticated"},status=201)
    except (ValueError,KeyError,TypeError,ValidationError,IntegrityError):
        return JsonResponse({"status":"Invalid registration","message":"Check the supplied fields, password and username."},status=400)

def backend_response(key,endpoint):
    try:
        return JsonResponse({key:get_request(endpoint)})
    except requests.RequestException:
        return JsonResponse({"error":"Backend service unavailable"},status=502)

@require_GET
def get_dealerships(request,state=None):
    from urllib.parse import quote
    endpoint="fetchDealers" if not state or state=="All" else "fetchDealers/"+quote(state,safe="")
    return backend_response("dealers",endpoint)

@require_GET
def get_dealer_reviews(request,dealer_id):
    try:
        reviews=get_request(f"fetchReviews/dealer/{dealer_id}")
        for review in reviews:
            try:
                result=analyze_review_sentiments(review.get("review",""))
                review["sentiment"]=result.get("sentiment","neutral")
            except requests.RequestException:
                review["sentiment"]="unavailable"
        return JsonResponse({"reviews":reviews})
    except requests.RequestException:
        return JsonResponse({"error":"Backend service unavailable"},status=502)

@require_GET
def get_dealer_details(request,dealer_id):
    return backend_response("dealer",f"fetchDealer/{dealer_id}")

@require_GET
def get_cars(request):
    cars=[{"CarMake":m.car_make.name,"CarModel":m.name,"CarType":m.type,"CarYear":m.year} for m in CarModel.objects.select_related("car_make").all()]
    return JsonResponse({"CarModels":cars,"CarMakes":list(CarMake.objects.values("id","name","description"))})

@require_GET
def analyze_review(request,text):
    try:
        return JsonResponse(analyze_review_sentiments(text))
    except requests.RequestException:
        return JsonResponse({"error":"Sentiment service unavailable"},status=502)

@csrf_exempt
@require_POST
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error":"Login required"},status=401)
    try:
        data=json.loads(request.body)
        data["name"]=request.user.username
        result=post_review(data)
        return JsonResponse({"status":"success","review":result},status=201)
    except (ValueError,TypeError):
        return JsonResponse({"error":"Invalid review"},status=400)
    except requests.RequestException:
        return JsonResponse({"error":"Backend service unavailable"},status=502)
