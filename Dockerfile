FROM python:3.6

# Install requirements
RUN pip install -r requirements.txt

# Setup the app structure in the container
RUN mkdir /app
WORKDIR /app
ADD . /app
# Run
CMD ["uwsgi","--http","0.0.0.0:5000","--module","server:app","--processes","2"]
