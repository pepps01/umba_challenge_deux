FROM python:3.11


COPY requirements.txt requirements.txt
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /src/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app", "--workers=5"]