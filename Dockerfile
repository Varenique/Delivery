FROM python:3

ENV PATH_FOR_INITIAL_DATA=None

# set a directory for the app
WORKDIR /app

# copy all the files to the container
COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 5000

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]
# run the command
#ENTRYPOINT ["python", "./app.py"]
