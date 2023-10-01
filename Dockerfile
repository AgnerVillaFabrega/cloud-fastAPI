FROM python:3.11-slim

ENV PIP_SISABLE_PIP_VERSION_CHACK=1
ENV PYTHONBUFFERED=1

RUN apt-get update && apt-get install -y libmagic1

WORKDIR /code

COPY requirements.txt .
RUN python -m venv venv

RUN /bin/bash -c "source venv/bin/activate"
RUN pip install -r requirements.txt

COPY ./app /code/app

EXPOSE 80

CMD [ "uvicorn","app.main:app","--reload","--host","0.0.0.0","--port","80" ]