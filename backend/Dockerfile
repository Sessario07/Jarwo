FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY api/ ./api/
COPY core/ ./core/
COPY models/ ./models/
COPY repositories/ ./repositories/
COPY services/ ./services/
COPY scripts/ ./scripts/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
