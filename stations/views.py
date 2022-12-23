import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    """Пагинатор, который читает CSV, делает список, создает объект класса Paginator и формирует context"""
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    stations_list = []  # пустой список для заполнения словарями с данными станций

    with open(BUS_STATION_CSV, encoding='utf-8') as file:
        station_file = csv.DictReader(file)  # открываем как словарь
        for row in station_file:
            station_dict = {
                'Name': row.get('Name'),
                'Street': row.get('Street'),
                'District': row.get('District')
            }
            stations_list.append(station_dict)  # наполняем списко выше

    page_num = int(request.GET.get('page', 1))  # получаем параметр для взятия нужной страницы пагинатора

    paginator = Paginator(stations_list, 10)  # создаем объект, что будет выводить по 10 записей
    page = paginator.get_page(page_num)  # строка для получения запрашиваемой страницы
    context = {
        'bus_stations': stations_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
