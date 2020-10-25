FROM python:3.9

WORKDIR /app

COPY requirements.txt ctfd-first-blood-discord/ ./

RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]
