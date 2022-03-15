FROM python:3.9-slim-bullseye

RUN mkdir -p /backend
WORKDIR /backend

# Install Python packages
RUN pip install poetry
COPY poetry.lock ./pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy app project ('./backend') into container
COPY ./ ./

# Run the app
# CMD uvicorn main:app --host 0.0.0.0 --port 8000 --log-level warning --app-dir ./app

# ENTRYPOINT ["uvicorn", "main:app"]
# CMD ["--host", "0.0.0.0", "--port", "8000", "--log-level", "warning", "--app-dir", "./app"]