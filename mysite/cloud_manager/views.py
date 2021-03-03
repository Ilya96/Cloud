from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def menu(request):
    # return HttpResponse('{% load cloud_manager_tags %}\n\n{% show_menu  %}')
    return render(request, 'cloud_manager/main.html')


def upload(request):
    return render(request, 'cloud_manager/upload.html')


def download(request):
    return render(request, 'cloud_manager/download.html')


def delete(request):
    return render(request, 'cloud_manager/delete.html')
