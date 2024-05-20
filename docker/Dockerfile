FROM python:3.12-alpine as poetry-base
RUN apk add --no-cache git
ENV POETRY_HOME="/opt/poetry"
RUN python -m venv ${POETRY_HOME} \
    && ${POETRY_HOME}/bin/pip install --no-cache-dir poetry

FROM poetry-base as builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN ${POETRY_HOME}/bin/poetry export -f requirements.txt --without-hashes -o requirements.txt \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.12-alpine as runner
WORKDIR /app
COPY . .
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
CMD ["python", "src/main.py"]
