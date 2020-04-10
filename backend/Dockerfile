FROM python:3.6

ADD . /backend

ENV PYTHONPATH=/backend

WORKDIR /backend

COPY requirements.txt /backend

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
