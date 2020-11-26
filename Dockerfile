FROM python:3

ARG ARG_DF_PRIVATE_KEY

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN touch service/db/default.db

ENV DEBUG=0
ENV HTTP_HOST=0.0.0.0
ENV HTTP_PORT=5000
ENV DB_PATH=service/db/default.db
ENV DF_PRIVATE_KEY=$ARG_DF_PRIVATE_KEY

CMD ["python", "./service/main.py"]
