FROM python:3.10.8-bullseye
RUN mkdir -p /usr/src/app/mlops2
WORKDIR /usr/src/app/mlops2
RUN python -m venv venv
COPY requirements.txt ./
RUN venv/bin/pip install --no-cache-dir -r ./requirements.txt
COPY app /usr/src/app/mlops2/app
COPY *.py /usr/src/app/mlops2/
COPY boot.sh /usr/src/app/mlops2/
COPY .env /usr/src/app/mlops2/
RUN chmod +x /usr/src/app/mlops2/boot.sh
ENV FLASK_APP run.py
ENTRYPOINT ["./boot.sh"]
EXPOSE 5050