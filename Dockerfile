FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 443
EXPOSE 4433/udp

CMD ["python","-m","schuaro"]