FROM python:3.6

# Setup the app structure in the container
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app

# Install requirements
RUN pip install -r requirements.txt

ADD . /app
# Run
CMD ["uwsgi","--http","0.0.0.0:5000","--module","server:app","--processes","2"]
