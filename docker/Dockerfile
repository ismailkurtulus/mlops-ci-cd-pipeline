FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src
COPY db /app/db
COPY data /app/data
COPY scripts /app/scripts

RUN python /app/scripts/init_db.py

EXPOSE 8000
ENV DB_PATH=/app/db/app.db

CMD ["uvicorn", "src.service:app", "--host", "0.0.0.0", "--port", "8000"]
