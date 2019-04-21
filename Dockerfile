FROM python:3.6

# Setup the app structure in the container
RUN mkdir /app
WORKDIR /app
ADD . /app

# Install requirements and run
RUN pip install -r requirements.txt
CMD ["uwsgi","--http","0.0.0.0:5000","--module","server:app","--processes","10"]
