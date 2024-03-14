FROM ubuntu:22.04
WORKDIR /usr/src/app
RUN apt-get update && apt-get install python3 python3-pip -y
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
RUN mkdir -p logs
CMD ["gunicorn", "app:app"]