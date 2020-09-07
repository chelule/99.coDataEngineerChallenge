# Event Ingestion

Moving events stream from mobile application to S3.
## Plan of attack (Overview, more can be found in the respective directory)

1. Generate fake streaming data which post to API endpoint. 
    - Generate fake events data through Faker.
    - POST it to the API endpoint.
    - mobile_app_event.py 
2. API to receive HTTP request from mobile_app_event.py.
    - In api directory. Built with flask.
    - Receive the event data and POST to Kafka REST Proxy.  
    - Logger for debugging purposes.
    - Tested in local, required to deploy on AWS API Gateway.
3. Kafka REST Proxy 
    - RESTful interface to Kafka cluster.
    - Setup and tested in local with Docker.
4. Kafka Cluster
    - Message brokering systems.
    - Horizontal scalable.
    - Fault tolerant.
    - Able to tune for throughput and latency. 
    - Setup and tested in local with Docker.
    - Information can be found at ./kafka directory
5. Kafka Connector (Consumer)
    - Uses Kafka S3 connector to write events data to S3.
    - Partition according to predicted/assumed query pattern.
    - Store data as parquet for data manipulation and queries.
    


 
