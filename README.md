

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервиса
uvicorn main:app --reload

# Или запуск через docker
docker build -t review-app .
docker run -d -p 8000:8000 --name my-review-app review-app


