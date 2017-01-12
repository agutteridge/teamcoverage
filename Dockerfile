FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy sample app
COPY ./app /app
