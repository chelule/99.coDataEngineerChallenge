# Kafka

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
 


*Note that in this dev, only one partition is used due to limited resources.*
