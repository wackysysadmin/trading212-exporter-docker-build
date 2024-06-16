FROM python:alpine3.20

COPY ./ /

RUN pip install -r requirements.txt

EXPOSE 5001

ENTRYPOINT ["python", "main.py"]
