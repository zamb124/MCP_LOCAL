# 🚀 Quick Start: Shopping Assistant MCP Server

## ⚡ AUTOMATIC SETUP - 30 Seconds!

**Полностью автономная установка - создает окружение, устанавливает пакеты, настраивает Claude Desktop!**

### 🍎 **macOS/Linux:**
```bash
./setup.sh
```

### 🪟 **Windows:**
```batch
setup.bat
```

### 🐍 **Manual (any OS):**
```bash
python3 setup.py
```

## ✅ **Что делает автоматическая установка:**
- ✅ **Проверяет Python 3.8+**
- ✅ **Создает виртуальное окружение**
- ✅ **Устанавливает все зависимости**
- ✅ **Безопасно сохраняет существующие MCP серверы**
- ✅ **Настраивает Claude Desktop автоматически**
- ✅ **Создает резервные копии конфигурации**
- ✅ **Тестирует функциональность**

---

## 🧹 ПОЛНАЯ ОЧИСТКА

### Удалить всё одной командой:
```bash
python3 cleanup.py
```

**Что удаляет cleanup.py:**
- ❌ **MCP сервер из конфигурации Claude Desktop**
- ❌ **Виртуальное окружение (venv/)**  
- ❌ **Python cache файлы**

**Что сохраняет:**
- ✅ **Другие MCP серверы в Claude Desktop**
- ✅ **Исходные файлы проекта**
- ✅ **Резервные копии конфигурации**

---

## 🔧 Требования

**Минимальные требования:**
- Python 3.8+ 
- Около 50 MB свободного места
- Claude Desktop

**Поддерживаемые системы:**
- 🍎 macOS 10.15+
- 🪟 Windows 10+
- 🐧 Linux (Ubuntu, CentOS, Fedora)

---

## 🆘 Решение проблем

### Основные команды:
```bash
# Восстановить конфигурацию из backup
python3 setup.py --restore

# Тестировать сервер
python3 test_server.py

# Полная очистка
python3 cleanup.py

# Переустановка
python3 cleanup.py && python3 setup.py
```

### Частые проблемы:

❌ **"Python not found"**
```bash
# Установить Python 3.8+ с https://www.python.org/downloads/
# На macOS: brew install python@3.11
# На Ubuntu: sudo apt install python3 python3-venv python3-pip
```

❌ **"Claude doesn't see server"**
- Перезапустить Claude Desktop
- Проверить: `python3 setup.py --restore`

❌ **"Permission denied"**
```bash
chmod +x setup.sh cleanup.py
```

❌ **"Import errors"**
- Виртуальное окружение создается автоматически
- Если проблемы: `python3 cleanup.py && python3 setup.py`

---

## 🛍️ **40+ Products Available!**

После установки просто спросите Claude:
- **"Find iPhone 15"** - Множество моделей iPhone со спецификациями
- **"Compare prices for PlayStation 5"** - Сравнение цен PS5 vs Xbox
- **"Show me Nike shoes"** - Спортивная обувь
- **"Search for Samsung TVs under 3000 AED"** - Фильтрация по цене
- **"What laptops are available?"** - MacBook, Dell, HP варианты
- **"Tell me about Noon store"** - Информация о магазинах

## 📊 **Полный каталог:**

### 📱 **Electronics (20+ товаров)**
- **Смартфоны:** iPhone 15 Pro Max/Pro, Samsung Galaxy S24 Ultra/+, Google Pixel 8 Pro
- **Ноутбуки:** MacBook Pro 14, MacBook Air 15, Dell XPS 13, HP Spectre x360
- **Игры:** PlayStation 5/Digital, Xbox Series X/S, Nintendo Switch OLED
- **Аудио:** AirPods Pro 2, Sony WH-1000XM5, Bose QuietComfort 45
- **ТВ:** Samsung QLED 4K, LG OLED

### 🏠 **Appliances (5+ товаров)**
- **Уборка:** Dyson V15 Detect
- **Кухня:** Samsung Smart Холодильник, машины Nespresso
- **Стирка:** LG стиральная машина, Bosch посудомойка

### 👕 **Clothing (4+ товара)**
- **Обувь:** Nike Air Max 270, Adidas Ultraboost 22
- **Одежда:** Levi's 501 джинсы, Calvin Klein футболки

### 💄 **Beauty (3+ товара)**
- **Уход за кожей:** La Mer, Charlotte Tilbury
- **Макияж:** Fenty Beauty тональный крем

### 🥑 **Groceries (4+ товара)**
- **Свежие продукты:** Органические авокадо, свежий лосось
- **Кладовая:** Премиум оливковое масло, рис басмати

### 🏃 **Sports (2+ товара)**
- **Оборудование:** Wilson теннисная ракетка, Yeti бутылка

## 🏪 **5 крупных магазинов ОАЭ:**
- **Carrefour** - Сеть гипермаркетов
- **Noon** - Электронная торговая площадка  
- **Amazon AE** - Онлайн магазин
- **Sharaf DG** - Ритейлер электроники
- **LuLu Hypermarket** - Розничная сеть

## 🔒 **Функции безопасности:**
- ✅ **Автоматический backup** существующих конфигураций
- ✅ **Сохраняет** все существующие MCP серверы
- ✅ **Восстановление одним кликом** если что-то пошло не так
- ✅ **Никакой потери данных** во время установки

---

💡 **Совет:** Автоматические скрипты **100% безопасны** - они делают backup всего перед изменениями!

## 📝 Полезные команды

```bash
# Полная переустановка
python3 cleanup.py && python3 setup.py

# Запуск сервера вручную
python3 shopping_mcp_server.py

# Активация виртуального окружения (создается автоматически)
source venv/bin/activate  # macOS/Linux
# или
venv\Scripts\activate  # Windows

# Деактивация виртуального окружения
deactivate

# Тест конкретных функций
python3 -c "from test_server import test_search_products; import asyncio; asyncio.run(test_search_products())"

# Показать локацию конфигурации Claude
python3 -c "from setup import get_claude_config_path; print(get_claude_config_path())"
```

## 🛍️ Что доступно?

- **40+ товаров** в 6 категориях
- **5 крупных магазинов** в ОАЭ
- **Сравнение цен в реальном времени**
- **Подробные спецификации товаров**
- **Информация о магазинах и отзывы**

### Примеры товаров:
- **Электроника:** iPhone 15 Pro Max, Samsung Galaxy S24, MacBook Pro, PlayStation 5
- **Одежда:** Nike Air Max, Adidas Ultraboost, Levi's джинсы
- **Красота:** La Mer крем, Fenty тональный крем
- **Техника:** Dyson V15, Samsung холодильник
- **И многое другое!**

---

💡 **Совет:** Сохраните этот файл для быстрого доступа к командам! 