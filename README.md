## Инструкция по запуску тестового задания

### 1. Установка зависимостей

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/DieSunn/Webapp-for-cash-flow-management.git
   cd -Webapp-for-cash-flow-management
   ```

2. Создайте и активируйте виртуальное окружение:
   
   Windows:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   Linux:
   ```
   python3 -m venv venv
   venv\bin\activate
   ```

4. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

---

### 2. Настройка базы данных

1. Откройте файл `webapp/settings.py` и убедитесь, что параметры подключения к базе данных корректны (по умолчанию используется SQLite).

2. Примените миграции для создания таблиц:
   ```
   python manage.py migrate
   ```

---

### 3. Запуск веб-сервиса

1. Запустите локальный сервер Django:
   ```
   python manage.py runserver
   ```

2. Откройте браузер и перейдите по адресу:
   ```
   http://127.0.0.1:8000/
   ```

---

**Проект
