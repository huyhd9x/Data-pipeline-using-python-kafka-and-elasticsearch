# Data-pipeline-using-python-kafka-and-elasticsearch

This project contains 2 files (before the README.md).

SourceCode.py is a combination of both scraping data code and Kafka procedure code to stream data to Elasticsearch (data lake).

real_estate_chotot.json: The data file was downloaded from elasticsearch(data lake).

Scrapping data on Jupyter Notebook

Real estate properties data is pulled from chotot.vn using python.

![image](https://user-images.githubusercontent.com/103510278/163196084-af7434fd-0043-4704-9b6a-599c4eb84bff.png)

Kafka Streaming

Then the data is passed through Kafka.

![image](https://user-images.githubusercontent.com/103510278/163199344-f197a5cd-14fa-4bec-aa28-289d93b0c7c3.png)

Elasticsearch

Data has been uploaded to Elasticsearch.

![image](https://user-images.githubusercontent.com/103510278/163203525-e513fd28-c906-42ff-a3d3-4d5a3d3eb2c7.png)
