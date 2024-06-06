FROM python:3.12.2-slim-bullseye

WORKDIR /app

# Set environment variables
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTCODE 1
ENV PYTHONUNBUFFERED 1
ENV COLUMNS 80

RUN apt-get update --fix-missing && apt-get install --no-install-recommends --yes software-properties-common 
RUN apt-get install --yes python3-dev  
RUN apt-get install --yes libpq-dev gcc
RUN apt-get install --yes postgresql-server-dev-all 
RUN apt-get install --yes git 
RUN apt-get install --yes netcat 
RUN apt-get install --yes vim
RUN apt-get autoremove && apt-get clean

RUN pip install --upgrade pip setuptools wheel

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./entrypoint.sh . 
RUN sed -i 's/\r$//g' ./entrypoint.sh

COPY . .

ENTRYPOINT [ "./entrypoint.sh" ]