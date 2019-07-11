from django.shortcuts import render


def test(request):
    data_1 = [1,2,3,4]
    return render(request, 'test.html',{'data': data_1})

