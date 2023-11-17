FROM python:3.8-slim

WORKDIR /api

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5001

CMD ["python", "__init__.py"]