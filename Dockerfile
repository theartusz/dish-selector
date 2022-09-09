FROM python:3.9-alpine
COPY  app app
WORKDIR app
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD [ "python3", "-m", "gunicorn", "-b", "0.0.0.0:8000", "app:app" ]