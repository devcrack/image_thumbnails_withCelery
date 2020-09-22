# Python
import os
# Celery
from celery import current_app

# Django
from django import forms
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.shortcuts import render

# Create your views here.

from .task import make_thumbnails

class FileUpload(forms.Form):
    image_file = forms.ImageField(required=True)


class HomeView(View):

    def get(self, request):
        form = FileUpload()
        return render(request, 'home.html', {'form': form})

    def post(self, request):
        form = FileUpload(request.POST, request.FILES)

        context = {}
        if form.is_valid():
            file_path = os.path.join(settings.IMAGES_DIR, request.FILES['images_file'].name)

            with open(file_path, 'wb+') as fp:
                for chunk in request.FILES['images_file']:
                    fp.write(chunk)

            task = make_thumbnails.delay(file_path, thumbnails=[(128, 128)])

            context['task_id'] = task.id
            context['task_status'] = task.status

            return render(request, 'home.html', context)




