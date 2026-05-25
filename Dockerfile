FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Отключаем буферизацию логов Python (чтобы сразу видеть логи в панели JustRun)
ENV PYTHONUNBUFFERED=1

# Копируем список зависимостей
COPY requirements.txt .

# Обновляем pip и устанавливаем библиотеки
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы и папки проекта
COPY . .

# Команда запуска. 
# ВНИМАНИЕ: Если твой главный файл называется bot.py, app.py или run.py — замени main.py на него!
CMD ["python", "main.py"]