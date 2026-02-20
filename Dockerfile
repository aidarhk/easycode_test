FROM python:3.11-slim

WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

RUN useradd --create-home --shell /bin/bash botuser
RUN chown -R botuser:botuser /app
USER botuser

EXPOSE 8080

CMD ["python", "bot.py"]
