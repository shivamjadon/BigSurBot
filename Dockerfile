FROM kenhv/kensurbot:alpine

RUN git clone -b main https://github.com/pratyakshm/bigsurbot /root/userbot
RUN chmod 777 /root/userbot
WORKDIR /root/userbot/

CMD ["python3","-m","userbot"]
