from django.urls import path

from .views import download_file

app_name = 'sendfile'

urlpatterns = [
                path('stuffing_excel/', download_file, name='get_document'),
                ]