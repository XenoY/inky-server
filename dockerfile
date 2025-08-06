# Basis-Image mit Python
FROM python:3.12-slim

# Chromium und weitere Tools installieren
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    fonts-dejavu \
    fonts-noto \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis
WORKDIR /app

# Python-Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projektdateien kopieren
COPY . .

# Port für Flask (falls du 6669 nutzt)
EXPOSE 6669

# Startbefehl
CMD ["python", "app.py"]