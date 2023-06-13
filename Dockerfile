FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install -r /code/requirements.txt

RUN pip install python-multipart

pip install "uvicorn[standard]" gunicorn

COPY . /code

CMD ["gunicorn", "main:app","--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]