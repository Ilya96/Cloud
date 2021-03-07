from django.urls import path
from cloud_manager.views import *

urlpatterns = [
    path('', menu, name='menu'),
    path('upload', upload, name='upload'),
    path('download', download, name='download'),
    path('delete', delete, name='delete'),
]
