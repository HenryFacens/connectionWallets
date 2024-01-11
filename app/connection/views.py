from django.views import View
from django.shortcuts import render
from django.http import JsonResponse

class Home(View):

    def get(self, request):
        return render(request, 'home/login.html')
    
    def post(self, request):
        return JsonResponse({'message': 'Hello, AJAX!'})