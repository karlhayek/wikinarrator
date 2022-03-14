FROM python:3.9-bullseye

RUN mkdir -p /backend
WORKDIR /backend

# Install Python packages
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app project ('./backend') into container
COPY ./ ./

# Run the app
# CMD uvicorn main:app --host 0.0.0.0 --port 8000 --log-level warning --app-dir ./app

# ENTRYPOINT ["uvicorn", "main:app"]
# CMD ["--host", "0.0.0.0", "--port", "8000", "--log-level", "warning", "--app-dir", "./app"]