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
        """
        The post method constructs the FileUploadForm object using the data sent in the request, checks its validity,
        then if valid it saves the uploaded file to the IMAGES_DIR and kicks off a make_thumbnails task while grabbing
        the task id and status to pass to the template, or returns the form with its errors to the home.html template


        :param request:
        :return:
        """
        form = FileUpload(request.POST, request.FILES)

        context = {}
        if form.is_valid():
            file_path = os.path.join(settings.IMAGES_DIR, request.FILES['image_file'].name)

            with open(file_path, 'wb+') as fp:
                for chunk in request.FILES['image_file']:
                    fp.write(chunk)

            task = make_thumbnails.delay(file_path, thumbnails=[(128, 128)])

            context['task_id'] = task.id
            context['task_status'] = task.status

            return render(request, 'home.html', context)


class TaskView(View):
    """
    This VIEW will be used via an AJAX request to check the status of the make_thumbnails task. Here you will notice
    that I have imported the current_app object from the celery package and used it to retrieve the task's AsyncResult
    object associated with the task_id from the request. I create a response_data dictionary of the task's status and id
    then if the status indicates the task has executed successfully I fetch the results by calling the get() method of
    the AsynchResult object assigning it to the results key of the response_data to be returned as JSON to the HTTP
    requester.
    """

    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse(response_data)



