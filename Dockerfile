FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
COPY ./app /app
COPY ./requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
