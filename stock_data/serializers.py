from rest_framework import serializers

class BacktestSerializer(serializers.Serializer):
    stock_symbol = serializers.CharField(max_length=10)
    initial_investment = serializers.FloatField()
    short_window = serializers.IntegerField(default=50)
    long_window = serializers.IntegerField(default=200)
