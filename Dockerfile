FROM python:3.9-alpine3.13 
LABEL maintainer="aleksandrsalmanov7@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./vpn_pet /vpn_pet 

WORKDIR /vpn_pet 
EXPOSE 8000 
