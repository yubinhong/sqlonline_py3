FROM frolvlad/alpine-python3:latest
RUN apk update && apk add sqlite && rm -rf /var/cache/apk
RUN pip3 install Django==4.0.3 PyMySQL==1.0.2
ADD . /opt/sqlonline/
WORKDIR /opt/sqlonline
RUN python3 manage.py makemigrations && python3 manage.py migrate
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]