FROM python:3.9
WORKDIR /app
COPY . /app
VOLUME /data
RUN pip install -r requirements.txt
EXPOSE 3000
CMD [ "flask", "run", "--host=0.0.0.0", "--port=3000" ]