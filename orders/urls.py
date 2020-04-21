from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderPageView.as_view(), name='orders'),
    path('charge/', views.charge, name='charge'),
]
