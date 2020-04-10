FROM python:3.6

ADD . /backend

ENV PYTHONPATH=/backend

WORKDIR /backend

COPY requirements.txt /backend

RUN pip install -r requirements.txt

EXPOSE 80

CMD python manage.py makemigrations
CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:80
