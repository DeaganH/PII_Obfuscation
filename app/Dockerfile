FROM python:3.10-slim

RUN mkdir /app

WORKDIR /app/
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

# Corrected CMD to properly run Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "3", "app:app"]