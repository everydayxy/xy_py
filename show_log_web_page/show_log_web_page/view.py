from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from . import main


aaa = main.main_function()


def show_log(request):
    log_data_dict = aaa.log_generate()
    print(aaa.log_generate())
    return render(request, 'index.html',{'data':log_data_dict})
