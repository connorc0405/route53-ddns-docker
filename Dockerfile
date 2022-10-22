FROM ubuntu:jammy

RUN apt-get update && apt-get install -y curl unzip groff less python3

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

COPY change.json /change.json
COPY script.py /script.py

ENTRYPOINT ["python3", "-u", "/script.py"]
