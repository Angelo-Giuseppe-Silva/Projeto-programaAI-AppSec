FROM python:3.13.7-slim

ENV PHYTONDONTWRITEBYTECODE=1 \
PYTHONUNBEFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV FLASK_APP=wsgi.py \
FLASK_ENV=development

EXPOSE 5000

CMD ["flask" , "run" , "--host=0.0.0.0" , "--port=5000"]
