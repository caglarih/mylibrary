FROM python:slim

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./ /app/

WORKDIR /app/

CMD ["bash", "/app/entrypoint.sh"]
