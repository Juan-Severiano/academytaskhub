from django.shortcuts import render
from .models import ItemList
from datetime import datetime


def home(request):
    data_atual = datetime.today()
    item_list = ItemList.objects.filter(due_date__lte=data_atual).order_by('-due_date')
    item_list_today = ItemList.objects.filter(due_date=data_atual).order_by('-due_date')
    item_list_past = ItemList.objects.filter(due_date__lt=data_atual).order_by('-due_date')
    return render(request, 'pages/home.html', context={
        'item_list': item_list,
        'atual_date': data_atual,
        'item_list_past':item_list_past,
        'item_today': item_list_today,
    })