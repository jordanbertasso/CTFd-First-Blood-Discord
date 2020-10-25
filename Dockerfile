FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ctfd-first-blood-discord/ ./

CMD ["python", "-u", "main.py"]
