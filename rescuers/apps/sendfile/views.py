import os
import datetime

from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper

from .services import ImportToExcel


def get_excel():
    file = ImportToExcel()
    file.make_excel()

    return file


def download_file(request):
    get_excel()
    the_file = f'media/excel/reports/Укомплектованность на {datetime.datetime.now().strftime("%d.%m.%Y")}.xlsx'
    filename = os.path.basename(the_file)

    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = f'attachment; filename=%D0%A3%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%82%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C%20%D0%BD%D0%B0%20{datetime.datetime.now().strftime("%d.%m.%Y")}.xlsx'


    return response
