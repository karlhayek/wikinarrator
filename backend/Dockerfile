FROM python:3.10-slim-bullseye

# Install Python packages
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# For development, Jupyter remote kernel
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

# Copy app project ('/backend') into container
COPY . /app

# Run the app
WORKDIR /app/app
CMD uvicorn main:app --host 0.0.0.0 --port 8000 --log-level warning

# docker build -t bdf-backend .
# docker run -it --rm -p 8000:8000 bdf-backend