FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/
COPY templates /app/templates
COPY static /app/static

EXPOSE 52034

ENV MODEL_PATH=/app/data/model.pkl
ENV PORT=52034

CMD ["python", "app.py"]
