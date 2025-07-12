# Сервис для анализа отзывов

Сервис для анализа тональности отзывов с двумя вариантами запуска:

## Ветки репозитория

1. `main` - базовая версия с обычным запуском
2. `dockerfile-feature` - версия с Docker-контейнеризацией

## Как переключаться между ветками

```bash
# Клонировать репозиторий
git clone https://github.com/MargaritaUlko/review_test_task.git
cd test

# Переключиться на нужную ветку:

# Для обычного запуска (main):
git checkout main

# Для Docker-версии:
git checkout dockerfile-feature

##Запуск в ветке main (обычный)
pip install -r requirements.txt
uvicorn main:app --reload

##Запуск в ветке dockerfile-feature
docker build -t review-app .
docker run -d -p 8000:8000 --name my-review-app review-app
