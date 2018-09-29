FROM python:3.6-alpine

# basic flask environment
RUN pip install flask

RUN mkdir /app
RUN chmod -R 777 /app
WORKDIR /app
COPY ./src/* /app/

EXPOSE 5050

# exectute start up script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]
