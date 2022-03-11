import os
import datetime

from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper

from .list_report import ListImportToExcel, today, month_names
from .staffing_report import ImportToExcel
from .attestation_report import AttestationImportToExcel


def get_excel(report):
    if report == 'staffing':
        file = ImportToExcel()

    elif report == 'list':
        file = ListImportToExcel()

    print(report)
    file.make_excel()

    return file



def download_stuffing_report(request):

    path = f'media/excel/staffing_reports'
    for file in os.listdir(path):
        os.remove(f'{path}/{file}')



    file = ImportToExcel()
    file.make_excel()
    the_file = f'media/excel/staffing_reports/Укомплектованность на {datetime.datetime.now().strftime("%d.%m.%Y")}.xlsx'
    filename = os.path.basename(the_file)

    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = f'attachment; filename=%D0%A3%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%82%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C%20%D0%BD%D0%B0%20{datetime.datetime.now().strftime("%d.%m.%Y")}.xlsx'


    return response


def download_list_report(request):
    path = f'media/excel/list_reports'
    for file in os.listdir(path):
        os.remove(f'{path}/{file}')

    file = ListImportToExcel()
    file.make_excel()
    the_file = f'media/excel/list_reports/Список работников филиала ЯВГСО на {today.day} {month_names[today.month - 1]} {today.year} года.xlsx'


    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = f'attachment; filename=%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2%20%D1%84%D0%B8%D0%BB%D0%B8%D0%B0%D0%BB%D0%B0%20%D0%AF%D0%92%D0%93%D0%A1%D0%9E%20%D0%BD%D0%B0%20{datetime.datetime.now().strftime("%d.%m.%Y")}.xlsx'


    return response


def download_attestation_report(request):
    path = f'media/excel/attestation_reports'
    for file in os.listdir(path):
        os.remove(f'{path}/{file}')

    file = AttestationImportToExcel()
    file.make_excel()
    the_file = f'media/excel/attestation_reports/Аттестующиеся {today.day}.{today.month}.{today.year}.xlsx'


    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = f'attachment; filename=%D0%90%D1%82%D1%82%D0%B5%D1%81%D1%82%D1%83%D1%8E%D1%89%D0%B8%D0%B5%D1%81%D1%8F%20{datetime.datetime.now().strftime("%d.%m.%Y")}.xlsx'


    return response

def export_db(request):
    the_file = 'db.sqlite3'

    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    response['Content-Length'] = os.path.getsize(the_file)
    response[
        'Content-Disposition'] = f'attachment; filename=db.sqlite3'

    return response