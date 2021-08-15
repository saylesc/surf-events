FROM python:stretch

COPY backend /usr/local/surfevents-backend

WORKDIR /usr/local/surfevents-backend

RUN pip install -r requirements.txt
RUN source ./setup.sh

ENTRYPOINT ["flask", "run"]