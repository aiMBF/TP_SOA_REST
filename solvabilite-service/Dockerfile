FROM python:3

WORKDIR /app

COPY requirements.txt /solvabilite/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /solvabilite/requirements.txt \
    && rm -rf /root/.cache/pip

COPY app/ /app/


CMD ["uvicorn","main:app","--reload","--host","0.0.0.0","--port", "8000"]

