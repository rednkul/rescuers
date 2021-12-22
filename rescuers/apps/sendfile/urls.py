from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import download_stuffing_report, download_list_report

app_name = 'sendfile'

urlpatterns = [
                path('stuffing_excel/', login_required(download_stuffing_report), name='download_stuffing_report'),
                path('list_excel/', login_required(download_list_report), name='download_list_report'),
                ]