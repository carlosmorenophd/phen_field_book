FROM python:3.9.18-bullseye

WORKDIR /app

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

RUN apt-get update && apt-get install -y p7zip

COPY app/ .

RUN mkdir -p /wirk
RUN mkdir -p /wirk/files
RUN chown -R 777 /wirk


CMD ["python", "-u",  "main.py"]