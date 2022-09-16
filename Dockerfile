FROM python:3.9-alpine
COPY  app app
RUN pip install --no-cache-dir -r app/requirements.txt
EXPOSE 8000
WORKDIR app
CMD ["python3", "-m", "gunicorn", "-b", "0.0.0.0:8000", "--timeout", "600", "app:app"]