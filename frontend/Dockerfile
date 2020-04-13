FROM python:3.6

ADD . /pyarcade

ENV PYTHONPATH=/pyarcade
ENV TERM=xterm

WORKDIR /pyarcade

RUN pip install -r requirements.txt

CMD python pyarcade/start.py
