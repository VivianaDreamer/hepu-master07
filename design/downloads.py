import csv
import openpyxl
import pandas as pd
from django.http import HttpResponse
from django.template.loader import render_to_string

# VRB from weasyprint import HTML

def _load_response(type:str,filename:str='download') -> HttpResponse:
    """
    Genera internamente la respuesta HTTP.\n
    Type = 'csv' o 'excel'
    """
    if type == 'csv':
        response = HttpResponse(content_type='text/csv')
    elif type == 'excel':
        response = HttpResponse(content_type='text/msexcel')
    response['Content-Disposition'] = "attachment;filename={}".format(filename)
    return response

def render_to_csv(data:list,filename="download.csv",horizontal=True):
    """
    Renderiza un archivo csv con la información solicitada por el usuario.\n
    Devuelve un HTTPResponse.\n
    Variables:\n
    data = información a renderizar en formato lista. P.e: [1,2,3,4,5]\n
    filename = nombre del archivo resultante\n
    horizontal = indica la orientación de los datos en el archivo descargable (horizontal(True) o vertical(False))\n
    """
    response = _load_response('csv',filename)
    writer = csv.writer(response)
    if horizontal:
        writer.writerow(data)
    else:
        for i in data:
            writer.writerow([i])
    return response

def render_dict_to_csv(data:str,filename="download.csv"):
    """
    Renderiza un archivo csv con la información solicitada por el usuario.\n
    Devuelve un HTTPResponse.\n
    Variables:\n
    data = información a renderizar en formato dict.\n
    filename = nombre del archivo resultante\n
    """
    response = _load_response('csv',filename)
    writer = csv.writer(response)
    for i,j in data.items():
        writer.writerow([i,j])
    return response

def render_dataframe_to_csv(data:pd.DataFrame,filename="download.csv"):
    """
    Renderiza un archivo csv con la información solicitada por el usuario.\n
    Devuelve un HTTPResponse.\n
    Variables:\n
    data = información a renderizar en formato DATAFRAME\n
    filename = nombre del archivo resultante\n
    """
    response = _load_response('csv',filename)
    data.to_csv(response)
    return response

def render_to_excel(data:str, filename="download.xls"):
    """
    Renderiza un archivo excel con la información solicitada por el usuario.\n
    Devuelve un HTTPResponse.\n
    Variables:\n
    data = información a renderizar en formato lista. P.e: [1,2,3,4,5]\n
    filename = nombre del archivo resultante\n
    """
    book = openpyxl.Workbook()
    sheet = book.active
    for i in data:
        sheet.append([i])
    response = _load_response('excel',filename)
    book.save(response)
    return response

def render_dict_to_excel(data:dict, filename="download.xls"):
    """
    Renderiza un archivo excel con la información solicitada por el usuario.\n
    Devuelve un HTTPResponse.\n
    Variables:\n
    data = información a renderizar en formato dict.\n
    filename = nombre del archivo resultante\n
    """
    book = openpyxl.Workbook()
    sheet = book.active
    for i,j in data.items():
        sheet.append([i,j])
    response = _load_response('excel',filename)
    book.save(response)
    return response

def render_dataframe_to_excel(data:pd.DataFrame, filename="download.xls"):
    """
    Renderiza un archivo excel con la información solicitada por el usuario.\n
    Devuelve un HTTPResponse.\n
    Variables:\n
    data = información a renderizar en formato lista. P.e: [1,2,3,4,5]\n
    filename = nombre del archivo resultante\n
    """
    response = _load_response('excel',filename)
    data.to_excel(response)
    return response

def render_to_pdf(data):
    html = render_to_string("design/resume.html", {'design':data})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"
  # VRB  HTML(string=html).write_pdf(response)
    return response