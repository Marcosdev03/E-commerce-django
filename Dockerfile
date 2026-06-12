FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV IMPORT_LEGACY_SQLITE=true

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]
CMD ["gunicorn", "loja.wsgi:application", "--bind", "0.0.0.0:8000"]
