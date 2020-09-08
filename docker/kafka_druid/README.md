# Kafka
Here we describe the Kafka implementation.

## Start the cluster

`docker-compose -f docker-compose-kafka-druid.yml up -d`

## Create topic
Either create events topic through Kafdrop or start the API for events ingestion as `KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"`

## Create schema in KSql
Data incoming in is in json format. But usually Data Analyst would need to read it in Parquet format. Parquet format is column based which is more suitable for data manipulation and queries. Hence KSql is used to translate raw json to avro, and uses the existing S3 Connector to produce data to S3.
1. Log into Ksql shell.
    
    `docker exec -it ksql-cli ksql http://ksql-server:8088`
2. Create json stream.

    `CREATE STREAM source_json (Event_Type VARCHAR, Event_Version VARCHAR, User_ID VARCHAR, Listing_ID VARCHAR, Server_Time VARCHAR, Device_Type VARCHAR) WITH (KAFKA_TOPIC='events', VALUE_FORMAT='JSON');`
3. Create avro stream.

    `CREATE STREAM target_json WITH (KAFKA_TOPIC='events_avro',REPLICAS=1,PARTITIONS=1,VALUE_FORMAT='AVRO') AS SELECT *, SUBSTRING(Server_Time, 0, 10) as Server_Date FROM source_json;`

## Configure S3-Sink Connector
Note that you need to provide S3 credential in docker-compose-kafka.yml.

    `curl -X POST -H 'Content-Type:application/json' --data @"./s3-parquet-connector.json" http://localhost:8086/connectors/`

There is a need to partition stream data for high throughput and low latency. We have several events and good to partition on that given that Data Analyst query are mostly based on events for such stream data.
 - Note that partition on event means that analytical pattern on events are assumed to be by event. Example, the total number of clicks on ListingView.
 - Partition by date as well since query are often date based. Example, today total number of click on ListingView VS yesterday total number of clicks on ListingView.
 
## Kafka Configuration
Look into how to configure Kafka for high throughput and low latency.

### Kafka topics
- Topics is a stream of data.
- Similar to a table in database, but without all the constraints.
- Defined by its name.
- Topics are split in partitions.

### Kafka partition

- Each partition is ordered.
- Each message within a partition gets an incremental id, called offset.
- Order is only guaranteed within a partition.
- Once the data are written to a partition, it cannot be changed. (immutability)
- Data is randomly assigned to a partition unless a key is provided. When a key is provided, it deterministically map a key to a partition. 
- More partition, more throughput/parallelism.

### How to partition

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


*Note that in this dev, only one partition is used due to limited resources.*



