FROM python:3.11

COPY ./main.py              /config/main.py
COPY ./requirements.txt     /config/requirements.txt
RUN pip install --no-cache-dir -r /config/requirements.txt

COPY ./brony_meetup_bot     /app/brony_meetup_bot


CMD ["python", "main.py"]
