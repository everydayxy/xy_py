from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def register_page(request):
    return render(request, 'register/register_index.html')