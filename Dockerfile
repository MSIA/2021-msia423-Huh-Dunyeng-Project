FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y python3-pip python3-dev git gcc dos2unix g++

WORKDIR .

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

RUN dos2unix app/boot.sh && apt-get --purge remove -y dos2unix
RUN chmod +x app/boot.sh

EXPOSE 5000

CMD ["./app/boot.sh"]
ENTRYPOINT ["python3"]
