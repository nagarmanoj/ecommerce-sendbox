FROM python:3.11

WORKDIR /app

RUN chmod 777 /app

RUN sudo mkdir /workspace

RUN sudo chmod 777 /workspace

COPY requirements.txt .

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . . 

EXPOSE 8011 

CMD ["python", "manage.py","runserver","0.0.0.0:8011"]
