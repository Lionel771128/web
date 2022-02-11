# Python server's Dockerfile

FROM python:3.8

# 設定映像檔的Metadata資訊，例如：作者、EMail、映像檔的說明等
LABEL maintainer="lionel771128" e-mail='123@123.com'

# 設定環境變數
# Setting PYTHONUNBUFFERED to a non empty value ensures
# that the python output is sent straight to terminal (e.g. your container log)
# without being first buffered and that you can see the output of your application
# (e.g. django logs) in real time.
# This also ensures that no partial output is held in a buffer somewhere
# and never written in case the python application crashes.
# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file/59812588
ENV PYTHONUNBUFFERED 1

RUN mkdir /web
WORKDIR /web
COPY . /web
# COPY ./server_run.sh /server_run.sh
RUN pip install -r requirements.txt
RUN chmod +x /web/server_run.sh

# ENTRYPOINT ["./server_run.sh"]
#CMD ["~/server_run.sh"]
# CMD ["python", "manage.py", "migrate"]
#RUN python manage.py migrate
#RUN python manage.py runserver



