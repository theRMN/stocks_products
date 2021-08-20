FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt .
COPY entrypoint.sh .

RUN chmod +x /usr/src/app/entrypoint.sh
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]


