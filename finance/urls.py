from django.urls import path
from . import views

urlpatterns = [
    path('backtest/', views.backtest_view, name='backtest'),
]
