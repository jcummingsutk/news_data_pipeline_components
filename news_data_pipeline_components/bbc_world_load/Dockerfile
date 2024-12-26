FROM python:3.12-slim-bookworm

WORKDIR /project

RUN pip install --upgrade pip

COPY news_data_pipeline_components/bbc_world_load news_data_pipeline_components/bbc_world_load

COPY news_data_pipeline_components/shared_code news_data_pipeline_components/shared_code

COPY news_data_pipeline_components/__init__.py __init__.py

ENTRYPOINT ["python", "-m", "news_data_pipeline_components.bbc_world_load.main"]