FROM python:3.9-alpine
COPY  app app
RUN apk add build-base
RUN pip3 install -r app/requirements.txt

EXPOSE 5000
ENV FLASK_APP=app/app \
    SECRET_KEY=7superHesloJakCyp
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]