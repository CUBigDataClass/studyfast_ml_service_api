FROM python:3.6

# Setup the app structure in the container
RUN mkdir /app
WORKDIR /app
ADD . /app

# Install requirements and run
RUN pip install -r requirements.txt
CMD ["gunicorn","-t","1000","-w","1","-b","0.0.0.0:80","--threads","1","server:app"]
