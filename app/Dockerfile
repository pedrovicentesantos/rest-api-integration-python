FROM python:3.7.6-alpine

EXPOSE 5000

ADD . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]