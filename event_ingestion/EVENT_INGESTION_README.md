# Event Ingestion

Moving events stream from mobile application to S3.

## *How would you build the data pipeline, while satisfying the high throughput, low latency requirement of the event ingestion API.*


## Plan of attack (Overview, more can be found in the respective directory)

1. Generate fake streaming data which post to API endpoint. 
    - Generate fake events data through Faker.
    - POST it to the API endpoint.
    - mobile_app_event.py 
2. API to receive HTTP request from mobile_app_event.py.
    - In api directory. Built with flask.
    - Receive the event data and POST to Kafka REST Proxy.  
    - Logger for debugging purposes.
    - Tested in local, required to deploy on AWS API Gateway to handle hundreds of thousands of concurrent API calls, traffic management, CORS support, authorization and access control, throttling, monitoring, and API version management.
3. Kafka REST Proxy 
    - RESTful interface to Kafka cluster.
    - API gateway would POST event data to Kafka REST Proxy
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


## Why Kafka

Kafka is a event streaming platform that provides high throughput, scalability, fault-tolerant and high availability. With Kafka, lots of functionality has already been provided.

### Distributed
Multiple types of setup.
- Single Node Single Broker (used here for dev purpose)
- Single Node Multi Broker 
- Multi Node Multi Broker

### Scalable
- Each partition can be hosted on a different Broker, which means that a single topic can be scaled horizontally across multiple Brokers.  

### Fault tolerant
- Able to replicate topics/partition across Broker.

### High Performance (How?)
#### Kafka topics
- Topics is a stream of data.
- Similar to a table in database, but without all the constraints.
- Defined by its name.
- Topics are split in partitions.

#### Kafka partition

- Each partition is ordered.
- Each message within a partition gets an incremental id, called offset.
- Order is only guaranteed within a partition.
- Once the data are written to a partition, it cannot be changed. (immutability)
- Data is randomly assigned to a partition unless a key is provided. When a key is provided, it deterministically map a key to a partition. 
- More partition, more throughput/parallelism.

#### How to partition

- More partitions lead to higher throughput.
    - Producer and Broker writes to different partition and can be done in fully parallel.
    - Consumer are given a single partition's data to one consumer thread.
    - Degree of parallelism is bounded by the number of partition consumed.
    - Rough formula for picking the number of partition is based on throughput.
        - Measure the throughput achievable on a single partition, *p* for production and *c* for consumption. let *t* be your target throughput.
        - Then we need *at least max(t/p, t/c)* partitions.
        - Production throughput depends on : 
            - Batching size.
            - Compression codec.
            - Type of acknowledgement.
            - Replication factor, etc.
        - Consumption throughput depends on how fast consumer logic can process each message.
- Messages with key
    - Kafka deterministically maps the message to a partition based on the hash of the key
    - If the number of partition change, certain message with key may not goes to the same partition and will breaks the order.
    - Hence it is better to determine the number of partition based on a future throughput and add more Broker overtime to the cluster and proportionally move a subset of existing partitions to the new Broker.
    
- More partition may increase end-to-end latency
    - Here, latency is defined by when a message is POST to the Kafka REST Proxy to when the message is read by the S3 connector.
    - Kafka only exposes a message to a consumer after it has been committed (message is replicated to all the in-sync replicas).
    - Time to commit a message can be significant in the latency.
    - Roughly limit the number of partitions per Broker to 100 * (number of broker) * (replication factor)




 
