# 🛍️ Shopping Assistant MCP Server

**Полнофункциональный MCP сервер для поиска товаров в популярных магазинах ОАЭ с полностью автономной установкой!**

![MCP Server](https://img.shields.io/badge/MCP-Server-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)

## ⚡ **Автономная установка за 30 секунд!**

### 🚀 **Один клик - полная установка:**

```bash
# macOS/Linux
./setup.sh

# Windows  
setup.bat

# Любая ОС
python3 setup.py
```

**Что происходит автоматически:**
- ✅ **Проверка Python 3.8+**
- ✅ **Создание виртуального окружения** 
- ✅ **Установка всех зависимостей**
- ✅ **Безопасная настройка Claude Desktop**
- ✅ **Сохранение существующих MCP серверов**
- ✅ **Автоматический backup конфигурации**
- ✅ **Тестирование функциональности**

### 🧹 **Полная очистка одной командой:**

```bash
python3 cleanup.py
```

**Безопасно удаляет:**
- ❌ MCP сервер из Claude Desktop
- ❌ Виртуальное окружение
- ❌ Cache файлы

**Сохраняет:**
- ✅ Другие MCP серверы
- ✅ Исходный код проекта  
- ✅ Backup файлы

---

## 🛍️ **40+ товаров в 5 магазинах ОАЭ**

### 📱 **Electronics (20+ товаров)**
- **Смартфоны:** iPhone 15 Pro Max/Pro, Samsung Galaxy S24 Ultra/+, Google Pixel 8 Pro
- **Ноутбуки:** MacBook Pro 14, MacBook Air 15, Dell XPS 13, HP Spectre x360  
- **Игры:** PlayStation 5/Digital, Xbox Series X/S, Nintendo Switch OLED
- **Аудио:** AirPods Pro 2, Sony WH-1000XM5, Bose QuietComfort 45
- **ТВ:** Samsung QLED 4K, LG OLED

### 🏠 **Appliances (5+ товаров)**
- Dyson V15 Detect, Samsung Smart Холодильник, Nespresso машины

### 👕 **Clothing (4+ товара)**  
- Nike Air Max 270, Adidas Ultraboost 22, Levi's джинсы

### 💄 **Beauty (3+ товара)**
- La Mer, Charlotte Tilbury, Fenty Beauty

### 🥑 **Groceries (4+ товара)**
- Органические продукты, премиум ингредиенты

### 🏃 **Sports (2+ товара)**
- Wilson теннисная ракетка, Yeti бутылки

---

## 🏪 **5 крупных магазинов ОАЭ:**

| Магазин | Описание | Товаров | Доставка |
|---------|----------|---------|----------|
| **Carrefour** | Сеть гипермаркетов | 23 локации | От 51 AED |
| **Noon** | E-commerce платформа | 25 локаций | От 119 AED |
| **Amazon AE** | Онлайн маркетплейс | По всей стране | От 50 AED |
| **Sharaf DG** | Ритейлер электроники | 15 локаций | От 75 AED |
| **LuLu Hypermarket** | Розничная сеть | 18 локаций | От 89 AED |

---

## 🔧 **3 основных инструмента**

### 1. `search_products` - Поиск товаров
```
• Поиск по названию, бренду, категории
• Фильтрация по цене и рейтингу  
• Детальные спецификации
• Информация о наличии
```

### 2. `compare_prices` - Сравнение цен
```
• Сравнение цен во всех магазинах
• Лучшие предложения и скидки
• Информация о доставке
• Рейтинги и отзывы
```

### 3. `get_store_info` - Информация о магазинах
```
• Детали о каждом магазине
• Категории товаров
• Условия доставки
• Контактная информация
```

---

## 💬 **Примеры запросов Claude**

После установки просто спросите Claude:

- **"Find iPhone 15"** - покажет все модели iPhone
- **"Compare prices for PlayStation 5"** - сравнит цены во всех магазинах
- **"Show me Nike shoes under 500 AED"** - отфильтрует по цене
- **"What laptops are available at Noon?"** - поиск в конкретном магазине
- **"Tell me about Carrefour store"** - информация о магазине

---

## 🔒 **Безопасность**

- ✅ **Автоматический backup** всех конфигураций
- ✅ **Сохранение существующих** MCP серверов
- ✅ **Восстановление одним кликом**: `python3 setup.py --restore`
- ✅ **Никакой потери данных** при установке/удалении

---

## 📋 **Системные требования**

**Минимальные:**
- Python 3.8+
- 50 MB свободного места
- Claude Desktop

**Поддерживаемые ОС:**
- 🍎 macOS 10.15+
- 🪟 Windows 10+
- 🐧 Linux (Ubuntu, CentOS, Fedora)

---

## 🆘 **Устранение неполадок**

### Команды для решения проблем:
```bash
# Восстановить из backup
python3 setup.py --restore

# Переустановка
python3 cleanup.py && python3 setup.py

# Тест сервера
python3 test_server.py

# Ручной запуск сервера
python3 shopping_mcp_server.py
```

### Частые проблемы:

❌ **"Python not found"**
- Установить Python 3.8+ с [python.org](https://python.org/downloads/)

❌ **"Claude не видит сервер"**
- Перезапустить Claude Desktop
- Проверить: `python3 setup.py --restore`

❌ **"Permission denied"**
- `chmod +x setup.sh cleanup.py`

---

## 🛠️ **Полезные команды**

```bash
# Полная переустановка
python3 cleanup.py && python3 setup.py

# Запуск сервера вручную
python3 shopping_mcp_server.py

# Активация окружения (создается автоматически)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Показать конфигурацию Claude
python3 -c "from setup import get_claude_config_path; print(get_claude_config_path())"

# Проверить статус серверов
python3 -c "import json; print(json.load(open('путь_к_конфигу'))['mcpServers'].keys())"
```

---

## 📁 **Структура проекта**

```
MCP_LOCAL/
├── 🐍 shopping_mcp_server.py    # Основной MCP сервер
├── ⚙️ setup.py                  # Полная автоматическая установка
├── 🧹 cleanup.py                # Полная очистка системы
├── 🔧 test_server.py            # Тесты функциональности
├── 📦 requirements.txt          # Python зависимости
├── 🍎 setup.sh                  # macOS/Linux установка
├── 🪟 setup.bat                 # Windows установка  
├── 📚 README.md                 # Этот файл
├── ⚡ QUICKSTART.md             # Быстрый старт
└── 📁 venv/                     # Виртуальное окружение (авто)
```

---

## 🎯 **Основные возможности**

### ✅ **Что работает:**
- Поиск товаров по 40+ позициям
- Сравнение цен в 5 магазинах
- Фильтрация по категориям, ценам, рейтингам
- Подробные спецификации товаров
- Информация о наличии и доставке
- Автономная установка и удаление
- Безопасное сохранение конфигураций

### 🔜 **Планируется:**
- Интеграция с реальными API магазинов
- Уведомления о изменении цен
- Персональные рекомендации
- Список желаний

---

## 📞 **Поддержка**

**Если что-то не работает:**

1. **Переустановка:** `python3 cleanup.py && python3 setup.py`
2. **Backup восстановление:** `python3 setup.py --restore`
3. **Проверка тестов:** `python3 test_server.py`
4. **Ручной запуск:** `python3 shopping_mcp_server.py`

**Логи:** Все ошибки сохраняются в терминал для диагностики

---

💡 **Совет:** Скрипты установки 100% безопасны - они создают backup перед любыми изменениями!

🎉 **Наслаждайтесь покупками с Shopping Assistant MCP Server!** 