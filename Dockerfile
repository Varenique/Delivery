FROM python:3.7.3

ENV PATH_FOR_INITIAL_DATA=None

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn==20.0.4


EXPOSE 5000
COPY . /app
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]

