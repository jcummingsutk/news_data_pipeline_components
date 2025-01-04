FROM python:3.12-slim-bookworm

WORKDIR /project

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY news_data_pipeline_components news_data_pipeline_components

ENTRYPOINT ["python", "-m", "news_data_pipeline_components.load.main"]