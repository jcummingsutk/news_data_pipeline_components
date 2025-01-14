Please forgive the lack of detail in this readme!

Contains the code to run my news data pipeline every 15 minutes

A data pipeline via google cloud workflow first runs the containerized microservice defined in news_data_pipeline_components/load/. This writes news articles from rss feeds to a mongodb collection. 

The workflow then runs the transform microservice. The containerized microservice in news_data_pipeline_components/transform/ filters for the articles not already in my news database, finds out which articles are text articles (as opposed to video), then summarizes the article via langchain and OpenAI.