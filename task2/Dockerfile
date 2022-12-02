FROM python:3.10.4-alpine3.15
WORKDIR /pythonapp
COPY src/python .
RUN apk add curl gcc libc-dev g++ \
    && pip install -r requirements.txt
CMD ["python", "-m", "flask", "run"]