FROM python:3.9.6

COPY ./requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "daily/manage.py", "runserver", "0.0.0.0:8000"]