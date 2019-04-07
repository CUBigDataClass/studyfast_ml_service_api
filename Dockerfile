FROM python:3.6

# Setup the app structure in the container
RUN mkdir /app
WORKDIR /app
ADD . /app

# Install requirements and run
RUN pip install -r requirements.txt
CMD ["python", "server.py"]