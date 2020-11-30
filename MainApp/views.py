from django.shortcuts import render

from MainApp.google_api import get_drive_files_list
# Create your views here.


def home(request):
    # get_drive_files_list()
    return render(request, 'home/index.html')
