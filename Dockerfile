FROM python:3.12-slim
WORKDIR /app
EXPOSE 8080

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

RUN pip install poetry

# コンテナ内にコピー
COPY . /app

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# コンテナを起動したときに実行されるコマンド
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]