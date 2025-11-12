FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

COPY src/ ./src/

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

EXPOSE 5000

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "src.app:create_app()"]
