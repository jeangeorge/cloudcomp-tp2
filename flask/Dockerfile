FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/
COPY templates /app/templates
COPY static /app/static

EXPOSE 5000

ENV MODEL_PATH=/app/data/model.pkl
ENV PORT=5000

CMD ["python", "app.py"]
