FROM python:3.8-slim-buster
COPY app.py receive.py publisher_parse_filename_as_msg.py requirements.txt app/
WORKDIR /app
# Setting ARG Variables
ARG BASE_URL_ARG
ARG RABBITMQ_USER_ARG
ARG RABBITMQ_PASSWORD_ARG
# Setting Environment Variables
ENV BASE_URL=$BASE_URL_ARG RABBITMQ_USER=$RABBITMQ_USER_ARG RABBITMQ_PASSWORD=$RABBITMQ_PASSWORD_ARG
RUN pip install -r requirements.txt
CMD ["python", "app.py"]