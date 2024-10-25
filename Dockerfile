FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED 1
CMD ["gunicorn", "stock_data.wsgi:application", "--bind", "0.0.0.0:8000"]
