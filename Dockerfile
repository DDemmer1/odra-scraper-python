FROM ubuntu

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
COPY . /app
EXPOSE 8081
ENTRYPOINT [ "python3" ]

CMD ["-m", "flask", "run", "--host=0.0.0.0", "--port=80"]