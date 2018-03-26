FROM python:3.5

RUN mkdir /project
COPY requirements.txt /project
WORKDIR /project
RUN pip install -r requirements.txt

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
EXPOSE 8080 8080

COPY . /project
RUN chown -R uwsgi .
