FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app/
ADD app /app

RUN pip install --trusted-host pypi.python.org -r /app/requirements.txt

EXPOSE 5000

# Corrected CMD to properly run Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "3", "app:app"]