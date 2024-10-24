from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .backtesting import simple_moving_average_strategy
from .serializers import BacktestSerializer

class BacktestView(APIView):
    def post(self, request):
        serializer = BacktestSerializer(data=request.data)
        if serializer.is_valid():
            stock_symbol = serializer.validated_data['stock_symbol']
            initial_investment = serializer.validated_data['initial_investment']
            short_window = serializer.validated_data['short_window']
            long_window = serializer.validated_data['long_window']

            results = simple_moving_average_strategy(stock_symbol, initial_investment, short_window, long_window)
            if "error" in results:
                return Response({"error": results["error"]}, status=status.HTTP_404_NOT_FOUND)

            return Response(results, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
