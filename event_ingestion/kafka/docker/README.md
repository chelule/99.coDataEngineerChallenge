`docker-compose -f docker-compose-kafka.yml up -d`

create schema

`docker exec -it ksql-cli ksql http://ksql-server:8088`

`CREATE STREAM source_json (Event_Type VARCHAR, Event_Version VARCHAR, User_ID VARCHAR, Listing_ID VARCHAR, Server_Time VARCHAR, Device_Type VARCHAR) WITH (KAFKA_TOPIC='events', VALUE_FORMAT='JSON');`

`CREATE STREAM target_json WITH (KAFKA_TOPIC='events_avro',REPLICAS=1,PARTITIONS=1,VALUE_FORMAT='AVRO') AS SELECT *, SUBSTRING(Server_Time, 0, 10) as Server_Date FROM source_json;`

`curl -X POST -H 'Content-Type:application/json' --data @"./s3-parquet-connector.json" http://localhost:8083/connectors/`

### kafka topic

- topics is a stream of data
- similar to a table in database, but without all the constraints
- defined by its name
- topics are split in partitions

### kafka partition

- each partition is ordered
- each message within a partition gets an incremental id, called offset
- order is only guaranteed within a partition
- once the data are written to a partition, it cannot be changed. (immutability)
- data is randomly assigned to a partition unless a key is provided
- more partition, more throughput/parallelism

### how to partition

- more partitions lead to higher throughput
    - producer and broker writes to different partition and can be done in fully parallel
    - consumer are given a single partition's data to one consumer thread
    - degree of parallelism is bounded by the number of partition consumed
    - rough formula for picking the number of partition is based on throughput
        - measure the throughput achievable on a single partition, p for production nad c for consumption. let t be your target throughput
        - then we need at least max(t/p, t/c) partitions
        - productions throughput depends on : 
            - batching size
            - compression codec
            - type of acknowledgement
            - replication factor, etc
        - consumption throughput depends on how fast consumer logic can process each message.
- messages with key
    - kafka deterministically maps the message to a partition based on the hash of the key
    - if the number of partition changes certain message with key may not goes to the same partition and will breaks the order.

in this dev, only one partition is used.


### s3 partition 
need to partition topic for high throughput. We have several event. good to partition on that. 
 - but partition on event means that analytical pattern are assumed to be by event. 
 - partition by date as well since query are often date based
