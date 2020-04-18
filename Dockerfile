FROM python:3.6-alpine
RUN pip install pipenv
WORKDIR /home/app
COPY . /home/app
RUN chmod +x entrypoint.sh  
RUN pipenv --python pipenv --python /usr/local/bin/python && pipenv install
EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]