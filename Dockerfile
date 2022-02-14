# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN python -m pip install gunicorn==20.1.0

WORKDIR /bulker-django-backend
COPY . /bulker-django-backend

# Create a directory for static files
RUN mkdir -p /bulker-django-backend/assets
RUN mkdir -p /bulker-django-backend/static

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /bulker-django-backend
USER appuser

# Collect static files in a new directory
RUN python manage.py collectstatic

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "bulker.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
# CMD ["sh", "-c", "python manage.py collectstatic && gunicorn bulker.wsgi:application --bind 0.0.0.0:8000"]