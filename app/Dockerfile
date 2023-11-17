FROM python:3.8-slim as base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "__init__.py"]

#### https://dev.to/pacheco/dockerize-a-flask-app-and-debug-with-vscode-34i1
# Debug image reusing the base
FROM base as debug

RUN pip install debugpy
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1