from django.contrib import admin
from .models import StockData

@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'date', 'open_price', 'close_price', 'high_price', 'low_price', 'volume')
    search_fields = ('symbol',)
