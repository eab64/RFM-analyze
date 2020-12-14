# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pandas as pd
from .forms import UserForm
from django.shortcuts import render
from .models import Information, Additional
from .resources import InformationResource, AdditionalResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
import sqlalchemy
import numpy as np
from django_excel_response import ExcelResponse
import sqlite3
from django.shortcuts import render
from .forms import UserForm, UploadFileForm
from io import BytesIO
import io
import openpyxl

def simple_upload(request):
    if request.method == 'POST':
        information_resource = InformationResource()
        additional_resource = AdditionalResource()
        dataset = Dataset()
        new_client = request.FILES['myfile']
        imported_data = dataset.load(new_client.read(), format = 'xlsx')
        for data in imported_data:
            value1 = Information(
                data[1],
                data[2],
                data[3],
                data[6],
                data[9],
            )
            try:
                value1.save()
            except ValueError:
                print('WRONG number')
            except ValidationError as e:
                print(e)
        for data2 in imported_data:
            value2 = Additional(
                data2[1],
                data2[3],
                data2[11],
                data2[16],
            )
            try:
                value2.save()
            except ValueError:
                print('WRONG number')
            except ValidationError as e:
                print(e)
    return render(request, 'upload.html')


def unload(request) -> HttpResponse:
    if request.method == "POST":
        form = request.POST.get("date")
        con = sqlalchemy.create_engine(
            'sqlite:////Users/Yeldos/PycharmProjects/no_related/no_relates/db.sqlite3')  # Connect to db
        df = pd.read_sql("SELECT * FROM myapp_information WHERE Visit_count>0", con)
        df_data = pd.read_sql("SELECT * FROM myapp_additional WHERE Visit_status='Клиент пришёл' and Visit_data <" + "'"+ form + "'"+"", con)
        df_sum = df[['Number','Visit_count','Income']].groupby(by='Number').sum()#Сложение income и visits_number
        df_sum.reset_index(inplace=True)
        df_by_data = df_data[['Number','Visit_data']].groupby(by='Number').max()
        merged = pd.merge(df_sum, df_by_data[['Visit_data']], on='Number', how='inner')
        # day = '2020-12-01 13:15:00'
        merged["days"] = (pd.to_datetime(merged["Visit_data"]).sub(pd.Timestamp(form)).dt.days) * -1
        conditions = [(merged["days"] <= np.percentile(merged["days"], 33)),  # Меньше 109
                      (merged["days"] <= np.percentile(merged["days"], 66)),  # Меньше 209
                      (merged["days"] >= np.percentile(merged["days"], 66))  # Больше 209
                      ]
        values = ['3', '2', '1']
        conditions2 = [(merged["Visit_count"] == 1),
                       (merged["Visit_count"] == 2) | (merged["Visit_count"] == 3),
                       (merged["Visit_count"] >= 4)
                       ]
        values2 = ['1', '2', '3']
        conditions3 = [(merged["Income"] <= 20000),  # Меньше чем 20000
                       (merged["Income"] >= 80000),  # Больше чем 80000
                       (merged["Income"] > 20000) | (
                               merged["Income"] < 80000)
                       ]
        values3 = ['1', '3', '2']

        merged["R"] = np.select(conditions, values)
        merged["F"] = np.select(conditions2, values2)
        merged["M"] = np.select(conditions3, values3)
        merged["RFM"] = merged["R"] + merged["F"] + merged["M"]
        conditions4 = [(merged["RFM"] == '333'),
                       (merged["RFM"] == '121') | (merged["RFM"] == '122') | (merged["RFM"] == '211') | (
                               merged["RFM"] == '212') | (merged["RFM"] == '221') | (merged["RFM"] == '231') | (
                               merged["RFM"] == '222') | (merged["RFM"] == '321'),
                       (merged["RFM"] == '113'),
                       (merged["RFM"] == '112') | (merged["RFM"] == '131'),
                       (merged["RFM"] == '111'),
                       (merged["RFM"] == '311') | (merged["RFM"] == '312'),
                       (merged["RFM"] == '132') | (merged["RFM"] == '133') | (merged["RFM"] == '232') | (
                               merged["RFM"] == '233') | (merged["RFM"] == '332') | (merged["RFM"] == '232') | (
                               merged["RFM"] == '322') | (merged["RFM"] == '331'),
                       (merged["RFM"] == '123') | (merged["RFM"] == '213') | (merged["RFM"] == '223') | (
                               merged["RFM"] == '313') | (merged["RFM"] == '323')
                       ]
        values4 = ['ЯДРО', 'Стандарт', 'Сонные киты', 'Сони', 'Потерянные', 'Новички', 'Лояльные', 'Киты']
        merged["LABEL"] = np.select(conditions4, values4)
        with BytesIO() as b:
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            merged.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            filename = 'test'
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
            return response
    else:
        userform = UserForm()
        return render(request, "index.html", {"form": userform})

def deleteRecord(request):
    try:
        sqliteConnection = sqlite3.connect('/Users/Yeldos/PycharmProjects/no_related/no_relates/db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        sql_delete_information = """DELETE from myapp_information"""
        sql_delete_additional = """DELETE from myapp_additional"""
        cursor.execute(sql_delete_information)
        cursor.execute(sql_delete_additional)
        sqliteConnection.commit()
        print("Record deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return HttpResponseRedirect("/")


def index(request):
    if "GET" == request.method:
        return render(request, '/Users/Yeldos/PycharmProjects/no_related/no_relates/templates/downloading.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        df = pd.read_excel(excel_file, sheet_name='Sheet 1')  # Прочитали Эксель
        df.insert(0, "id", '')  # Добавили столбец id
        df = df.rename(columns={'Клиент': 'Name', 'Телефон': 'Number', 'Выручка, ₸': 'Income',
                                'Количество посещений': 'Visit_number',
                                'Дата': 'Visit_data', 'Статус визита': 'Visit_status'})
        for i in range(0, len(df.Number)):  # Добавление номера всем операциям
            if isinstance(df['Number'][i], float):
                df['Number'][i] = df['Number'][i - 1]
            else:
                continue
        with BytesIO() as b:
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            filename = 'test'
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
            return response
        return render(request, 'upload.html')
        return HttpResponseRedirect("/")