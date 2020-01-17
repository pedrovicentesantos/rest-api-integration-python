FROM python:3.7.6-alpine

EXPOSE 5000

WORKDIR /app

ADD . /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]