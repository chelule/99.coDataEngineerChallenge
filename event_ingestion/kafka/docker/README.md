`docker-compose -f docker-compose-kafka.yml up -d`

create schema
`docker exec -it ksql-cli ksql http://ksql-server:8088`

`CREATE STREAM source_json (Event_Type VARCHAR, Event_Version VARCHAR, User_ID VARCHAR, Listing_ID VARCHAR, Server_Time VARCHAR, Device_Type VARCHAR) WITH (KAFKA_TOPIC='events', VALUE_FORMAT='JSON');`

`CREATE STREAM target_json WITH (KAFKA_TOPIC='events_avro',REPLICAS=1,PARTITIONS=1,VALUE_FORMAT='AVRO') AS SELECT * FROM source_json;`



, TIMESTAMP='Server_Time', TIMESTAMP_FORMAT='yyyy-MM-dd''T''HH:mm:ssX'