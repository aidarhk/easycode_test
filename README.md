# Telegram Birthday Bot 🎉

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Supported-green)](https://docker.com)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-orange)](https://aiogram.dev)

**Тестовое задание: Telegram-бот для управления днями рождения с напоминаниями за 3 дня.**

## ✨ Функционал


- ✅ `/add Имя ДД.ММ` — добавить день рождения
- ✅ `/list` — список всех ДР пользователя  
- ✅ `/delete Имя` — удалить запись
- ✅ `/help` — справка по командам
- ✅ Автоматические напоминания за **3 дня** до ДР
- ✅ Валидация дат (ДД.ММ, ДД/ММ)
- ✅ Per-user SQLite база данных

## 📦 Быстрый старт (локально)

1. Подготовка
```bash
echo "BOT_TOKEN=your_token_here" > .env
```
2. Создай .env:

```bash
BOT_TOKEN=your_bot_token_here
```

3. Запуск
```bash
docker-compose up -d --build
```
