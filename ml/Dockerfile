FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY generate_rules.py /app/

COPY data /app/data/

ENV DATASET_PATH=/app/data/2023_spotify_ds1.csv
ENV MODEL_PATH=/app/data/model.pkl

CMD ["python", "generate_rules.py"]
