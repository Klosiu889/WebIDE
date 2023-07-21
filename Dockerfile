# Prepare environment
FROM python:3.11.4-slim

# Install Node.js and SDCC
RUN apt-get update
RUN apt-get install nodejs -y
RUN apt-get install sdcc -y

# Prepare App
COPY . /app
WORKDIR /app
EXPOSE 8000

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Prepare database
WORKDIR /app/Backend
RUN python manage.py makemigrations
RUN python manage.py migrate

# Run Tests
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
