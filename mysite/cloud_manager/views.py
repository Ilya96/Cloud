import glob
import mimetypes
import os

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
import hashlib

# Create your views here.


fs = FileSystemStorage()


def menu(request):
    # return HttpResponse('{% load cloud_manager_tags %}\n\n{% show_menu  %}')
    return render(request, 'cloud_manager/main.html')


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('document')
        if not uploaded_file:
            return render(request, 'cloud_manager/upload.html')
        else:
            fs.save(uploaded_file.name, uploaded_file)
            md5 = hashlib.md5()
            # sha1 = hashlib.sha1()
            with open('media/' + uploaded_file.name, 'rb') as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    md5.update(data)
                    # sha1.update(data)
            if not fs.exists(str(md5.hexdigest())[0:2] + '/' + str(md5.hexdigest()) + '.' + uploaded_file.name.split('.')[-1]):
                fs.save(str(md5.hexdigest())[0:2] + '/' + str(md5.hexdigest()) + '.' + uploaded_file.name.split('.')[-1], uploaded_file)
            fs.delete(uploaded_file.name)
            # return HttpResponse(f'<h1>{md5.hexdigest()}, {sha1.hexdigest()} </h1>')
            return HttpResponse(f'<h1>File uploaded successfully!</h1> <h2>Your file hash:</h2> <h3> {str(md5.hexdigest())} </h3>')
    else:
        return render(request, 'cloud_manager/upload.html')


def download(request):
    if request.method == 'POST':
        uploaded_text = request.POST.get('text')
        file_path = glob.glob('media/' + uploaded_text[0:2] + '/' + uploaded_text + '.' + '*')
        if not uploaded_text:
            return render(request, 'cloud_manager/download.html')
        elif len(uploaded_text) < 2:
            return HttpResponse(f'<h1>Hash length must be >= 2</h1>')
        elif len(file_path):
            fp = open(file_path[0], "rb")
            response = HttpResponse(fp.read())
            fp.close()
            file_type = mimetypes.guess_type(file_path[0])
            if file_type is None:
                file_type = 'application/octet-stream';
            response['Content-Type'] = file_type
            response['Content-Length'] = str(os.stat(file_path[0]).st_size);
            response['Content-Disposition'] = f"attachment; filename={uploaded_text}.{file_path[0].split('.')[-1]}"
            return response
        else:
            return HttpResponse(f'<h1>Such file not exists!</h1>')
    else:
        return render(request, 'cloud_manager/download.html')


def delete(request):
    if request.method == 'POST':
        uploaded_text = request.POST.get('text')
        file_path = glob.glob('media/' + uploaded_text[0:2] + '/' + uploaded_text + '.' + '*')
        if not uploaded_text:
            return render(request, 'cloud_manager/delete.html')
        elif len(uploaded_text) < 2:
            return HttpResponse(f'<h1>Hash length must be >= 2</h1>')
        elif len(file_path):
            fs.delete(uploaded_text[0:2] + '/' + uploaded_text + '.' + file_path[0].split('.')[-1])
            return HttpResponse(f'<h1>File has been deleted!</h1>')
        else:
            return HttpResponse(f'<h1>Such file not exists!</h1>')
    else:
        return render(request, 'cloud_manager/delete.html')
