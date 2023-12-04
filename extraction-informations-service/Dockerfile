FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# COPY ./app /app

# RUN pip install -r /app/requirements.txt

COPY requirements.txt /composite/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /composite/requirements.txt \
    && rm -rf /root/.cache/pip

COPY app/ /app/


CMD ["uvicorn","main:app","--reload","--host","0.0.0.0","--port","8000"]


