"""testing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insert_trip', views.insert_trip, name='insert_trip'),
    path('insert_trip_value', views.insert_trip_value, name='insert_trip_value'),
    path('delete_trip/<int:trip_id>', views.delete_trip, name='delete_trip'),
    path('expand/<int:trip_id>/', views.trip_expand, name='trip_expand'),
    path('expand/<int:trip_id>/insert_trans_value', views.insert_trans_value, name='insert_trans_value'),
    path('expand/<int:trip_id>/delete_trans/<int:trans_id>', views.delete_trans, name='delete_trans'),
    path('expand/<int:trip_id>/analysis_trans', views.analysis_trans, name='analysis_trans'),
]
