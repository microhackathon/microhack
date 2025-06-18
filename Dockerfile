FROM python:3.11

ENV PYTHONUNBUFFERED=1

ARG BUILD_ENVIRONMENT=dev

WORKDIR /microhack

COPY requirements-common.txt requirements-common.txt
COPY requirements-${BUILD_ENVIRONMENT}.txt requirements-${BUILD_ENVIRONMENT}.txt
RUN pip install --no-cache-dir --upgrade -r /microhack/requirements-${BUILD_ENVIRONMENT}.txt

COPY . .
CMD ["python", "run.py"]