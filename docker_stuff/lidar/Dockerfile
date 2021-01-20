FROM ubuntu

#ubuntu setup
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install python3 -y

#run the pythonscript
FROM python:3
WORKDIR /usr/src/app
COPY . .
CMD ["test.py"]
ENTRYPOINT ["python3"]
